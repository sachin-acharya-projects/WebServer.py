from ..Types import *
from ..Configurations.Settings.Settings import HOST, PORT, DEBUG
from ..Utils.Request import Request
from ..Utils.Response import Response
import socket
import datetime
import threading
import sys
from dataclasses import dataclass
from colorama import Fore, init
from abc import ABC, abstractmethod

__all__ = ["BaseServer"]

init(autoreset=True)


class _RouteRecordType(TypedDict):
    handler: Callable[[Response, Request], None]
    methods: List[RequestType]


class _ErrorRecordType(TypedDict):
    handler: Callable[[int], str]


@dataclass
class _ContentType:
    HTML: str = "text/html"
    CSS: str = "text/css"
    JAVASCRIPT: str = "application/javascript"
    JSON: str = "application/json"
    OCTSTREAM: str = "application/octet-stream"  # ? For Binary

    def get(
        self,
        key: Literal["HTML", "CSS", "JAVASCRIPT", "JSON", "OCTSTREAM"],
        default: str = "application/octet-stream",
    ) -> str:
        return getattr(self, key, default)


class BaseServer(ABC):
    def __init__(self) -> None:
        self._routes: Dict[str, _RouteRecordType] = {}
        self._error_handers: Dict[str, _ErrorRecordType] = {}
        self._ContentType = _ContentType()

    def route(
        self, path: str, methods: List[RequestType] | None = None
    ) -> Callable[[Response, Request], None]:
        def wrapper(
            func: Callable[[Response, Request], None]
        ) -> Callable[[Response, Request], None]:
            self._routes[path] = {"handler": func, "methods": methods or ["GET"]}
            return func

        return wrapper

    def error_route(self, status_code: int) -> Callable[[int], int]:
        def wrapper(func: Callable[[int], int]) -> Callable[[int], int]:
            self._error_handers[status_code] = {"handler": func(status_code)}
            return func

        return wrapper

    def __log(self, *messages) -> None:
        date = datetime.datetime.now()
        date = f"{date:[%d of %B, %Y %I:%M:S %p]}"
        if DEBUG:
            print(f"{date:<30}", *messages)

    @abstractmethod
    def handleClient(self, client: socket.socket) -> None:
        raise Exception("Not Implemented")

    def __send(
        self,
        client: socket.socket,
        status: Tuple[int, str],
        data: str,
        content_type: str = "",
    ) -> int:
        # status_code, status_text = status
        
        if isinstance(data, str):
            response = "HTTP/1.1 %s %s\r\nContent-Type: %s\r\n\r\n" % (*status, content_type) + data
            response = response.encode()
        else:
            response = (
                "HTTP/1.1 %s %s\r\nContent-Type: %s\r\n\r\n".encode() % (*status, content_type) + data
            )
        try:
            status = client.send(response)
            client.close()
            return client
        except OSError as e:
            self.__log(f"{Fore.RED}OSError: {Fore.LIGHTRED_EX}{repr(e)}")
            return 0

    def run(self) -> None:
        import atexit

        def close(server: socket.socket) -> None:
            try:
                server.close()
            except OSError:
                ...

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        atexit.register(lambda: close(server))
        print("Server listening on http://%s:%s" % (HOST, str(PORT)))

        while True:
            try:
                try:
                    client_socket, _ = server.accept()
                    threading.Thread(
                        target=self.handleClient, args=(client_socket,)
                    ).start()
                except SystemExit:
                    ...
            except KeyboardInterrupt:
                server.close()
                break
