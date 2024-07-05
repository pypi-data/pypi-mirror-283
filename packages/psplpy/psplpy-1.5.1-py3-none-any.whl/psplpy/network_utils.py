import errno
import multiprocessing
import socket
import threading
import time
from abc import abstractmethod, ABC
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Callable
import requests
from serialization_utils import CompressSerializer


def _find(func: Callable, try_ports: list[int] = None, exclude_ports: list[int] = None,
          try_range: tuple[int, int] = None) -> int | None:
    ports = (try_ports or []) + list(range(*try_range))
    exclude_ports = exclude_ports or []
    for port in ports:
        if port not in exclude_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    result = func(s, port)
                    if result is not None:
                        return result
            except socket.error:
                continue


def find_running_port(host: str = '127.0.0.1', try_ports: list[int] = None, exclude_ports: list[int] = None,
                      try_range: tuple[int, int] = None, timeout: float = 0.5) -> int | None:
    def _test(s: socket.socket, port: int):
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        if result == 0:
            return port

    return _find(_test, try_ports, exclude_ports, try_range)


def find_free_port(host: str = '127.0.0.1', try_ports: list[int] = None, exclude_ports: list[int] = None,
                   try_range: tuple[int, int] = (1024, 65536)) -> int | None:
    def _test(s: socket.socket, port: int):
        s.bind((host, port))
        return port

    return _find(_test, try_ports, exclude_ports, try_range)


class ClientSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, client_socket: socket.socket = None,
                 client_host: str = None, client_port: int = 12345):
        self.host = host
        self.port = port
        self.client_host = client_host
        self.client_port = client_port
        self.client_socket = client_socket

        self._length_bytes = 5

        if self.client_socket:
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)

    def connect(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)
        # use the certain address of the client to connect the server
        if self.client_host and self.client_port:
            self.client_socket.bind((self.client_host, self.client_port))
        self.client_socket.connect((self.host, self.port))

    def _get_length(self, data: bytes) -> bytes:
        # for 5 bytes unsigned int, the max data length is 2**40 - 1, namely about 1tb
        bytes_result = len(data).to_bytes(self._length_bytes, byteorder='big')
        return bytes_result

    def _recv_length(self) -> int:
        byte_result = self.client_socket.recv(self._length_bytes)
        return int.from_bytes(byte_result, byteorder='big')

    def send(self, data: bytes):
        return self.client_socket.sendall(self._get_length(data) + data)

    def recv(self) -> bytes:
        length = self._recv_length()
        data = bytearray()
        while len(data) < length:
            data += self.client_socket.recv(length - len(data))
        return bytes(data)

    def recvf(self, output_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(output_path, 'wb') as f:
            while True:
                data = self.client_socket.recv(bufsize)
                if not data:
                    break
                f.write(data)

    def sendf(self, input_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(input_path, 'rb') as f:
            while True:
                data = f.read(bufsize)
                if not data:
                    break
                self.client_socket.send(data)

    def close(self) -> None:
        return self.client_socket.close()


class ServerSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, backlog: int = 64):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(backlog)
        self.server_socket.setblocking(False)

    def accept(self) -> tuple[ClientSocket, Any] | tuple[None, None]:
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                return ClientSocket(client_socket=client_socket), addr
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    time.sleep(0.01)
                    continue
                elif e.errno == errno.EBADF:
                    return None, None
                else:
                    raise e

    def handle(self, handler: Callable, *args, **kwargs) -> None:
        def _handle():
            while True:
                client_socket, addr = self.accept()
                if not (client_socket and addr):
                    break
                handle_thread = threading.Thread(target=handler, args=(client_socket, addr, *args), kwargs=kwargs)
                handle_thread.daemon = True
                handle_thread.start()

        threading.Thread(target=_handle).start()

    def close(self) -> None:
        self.server_socket.close()


class MpHttpServer(ABC):
    def __init__(self, host: str = '0.0.0.0', port: int = 80, workers: int = 1, timeout: int = 3600,
                 show_info: bool = True, compress_threshold: int = 1024 * 128):
        self.host, self.port, self.workers, self.timeout, self.show_info = host, port, workers, timeout, show_info
        self.compress_threshold = compress_threshold
        self._process_id = 0
        self._lock = multiprocessing.Lock()
        self._s = CompressSerializer(threshold=self.compress_threshold)
        self._result_dict = multiprocessing.Manager().dict()
        self._req_que = multiprocessing.Queue()
        self._start_processes()

    class _RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, mp_server: 'MpHttpServer', *args, **kwargs):
            self.mp_server = mp_server
            super().__init__(*args, **kwargs)

        def log_message(self, format, *args):
            if self.mp_server.show_info:
                super().log_message(format, *args)

        def _fetch_result(self, process_id: int) -> dict:
            t_start = time.time()
            while time.time() - t_start < self.mp_server.timeout:
                if self.mp_server._result_dict.get(process_id) is not None:
                    return self.mp_server._result_dict.pop(process_id)
                time.sleep(0.01)

        def _put_data(self, data: dict) -> list:
            process_ids = []
            for sub_data in data:
                with self.mp_server._lock:
                    sub_data['_process_id'] = self.mp_server._process_id
                    process_ids.append(self.mp_server._process_id)
                    self.mp_server._process_id += 1
                self.mp_server._req_que.put(sub_data)
            return process_ids

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = self.mp_server._s.load_pickle(post_data)

            process_ids = self._put_data(data)
            results = []
            for process_id in process_ids:
                results.append(self._fetch_result(process_id))

            response = self.mp_server._s.dump_pickle(results)
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    @staticmethod
    def get_data(req_que: multiprocessing.Queue) -> dict:
        return req_que.get()

    @staticmethod
    def put_result(result: Any, result_dict, data) -> None:
        result_dict[data['_process_id']] = result

    @abstractmethod
    def main_process(self, req_que: multiprocessing.Queue, result_dict):
        ...

    def _start_processes(self):
        for _ in range(self.workers):
            multiprocessing.Process(target=self.main_process, args=(self._req_que, self._result_dict)).start()

    def run_server(self):
        httpd = HTTPServer((self.host, self.port),
                           lambda *args, **kwargs: self._RequestHandler(self, *args, **kwargs))
        if self.show_info:
            print(f"Starting server on port {self.port}...")
        httpd.serve_forever()


class MpHttpClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 80, compress_threshold: int = 1024 * 128):
        self.host, self.port, self.compress_threshold = host, port, compress_threshold
        self._s = CompressSerializer(threshold=self.compress_threshold)

    def batch(self, data_list: list | tuple, compress: bool = None) -> list[Any]:
        data = self._s.dump_pickle(data_list, compress=compress)
        resp = requests.post(f'http://{self.host}:{self.port}', data=data)
        return self._s.load_pickle(resp.content)

    def get(self, data: Any, compress: bool = None) -> Any:
        return MpHttpClient.batch(self, [data], compress=compress)[0]
