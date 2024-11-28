from WebServer.types import Callable, List, RequestMethod, Dict, Tuple
from WebServer.config import HOST, PORT, DEBUG, BASE_DIR
from WebServer.http.request import Request
from WebServer.http.response import Response

from abc import ABC, abstractmethod
from dataclasses import dataclass
from colorama import init, Fore

import datetime
import threading
import atexit

import socket
import os

__all__ = ["AbstractBase"]
init(True)

_HandleType = Callable[[Request, Response], None]


@dataclass
class _RouteRecordType(object):
    handler: _HandleType
    methods: List[RequestMethod]


@dataclass
class _ErrorRecordType(object):
    handler: _HandleType


class AbstractBase(ABC):
    def __init__(self) -> None:
        self._routes: Dict[str, _RouteRecordType] = {}
        self._error_handlers: Dict[int, _ErrorRecordType] = {}

    def route(
        self, path: str, methods: List[RequestMethod] | None = None
    ) -> Callable[[_HandleType], _HandleType]:
        def wrapper(handler: _HandleType) -> _HandleType:
            route = _RouteRecordType(handler, methods or ["GET"])
            self._routes[path] = route
            return handler

        return wrapper

    def error_route(self, status_code: int) -> Callable[[_HandleType], _HandleType]:
        def wrapper(handler: _HandleType) -> _HandleType:
            route = _ErrorRecordType(handler)
            self._error_handlers[status_code] = route
            return handler

        return wrapper

    def log(self, *messages) -> None:
        date = datetime.datetime.now()
        date = f"{date:[%d of %B, %Y %I:%M:S %p]}"
        if DEBUG:
            print(f"{date:<30}", *messages)

    @abstractmethod
    def handleClient(self, client: socket.socket) -> None:
        raise NotImplementedError("Abstract method must be implemented in child class.")

    def send(
        self,
        client: socket.socket,
        status: Tuple[int, str],
        data: str | bytes,
        content_type: str = "",
    ) -> int:
        if isinstance(data, str):
            response = (
                "HTTP/1.1 %s %s\r\nContent-Type: %s\r\n\r\n" % (*status, content_type)
                + data
            )
            response = response.encode()
        else:
            response = (
                "HTTP/1.1 %s %s\r\nContent-Type: %s\r\n\r\n" % (*status, content_type)
            ).encode() + data
        try:
            status_ = client.send(response)
            client.close()
            return status_
        except OSError as e:
            self.log(f"{Fore.RED}OSError: {Fore.LIGHTRED_EX}{repr(e)}")
            return 0

    def render_error(
        self,
        status: Tuple[int, str],
        response: Response,
        request: Request,
        client: socket.socket,
    ) -> int:
        status_code, status_text = status
        error_template = (
            BASE_DIR
            / "WebServer"
            / "Templates"
            / "Errors"
            / (str(status_code) + ".html")
        )
        temp = self._error_handlers.get(status_code, None)
        if temp:
            temp.handler(request, response)

        if os.path.exists(error_template):
            with open(error_template) as file:
                data = file.read().replace("{{ pathname }}", request.path)
                return self.send(client, status, data, "text/html")
        data = {
            404: "URL '%s' Not Found" % request.path,
            405: "Method [%s] on '%s' Not Allowed" % (request.method, request.path),
        }.get(status_code, "%s - %s" % status)
        return self.send(client, status, data)

    def run(
        self,
        callback: Callable[[socket.socket, str, int], None] | None = None,
        post_callback: Callable[[socket.socket], None] | None = None,
    ) -> None:
        def _close(server: socket.socket) -> None:
            try:
                server.close()
            except OSError:
                ...

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        server.settimeout(1)

        post_callback = post_callback if post_callback else _close
        atexit.register(lambda: post_callback(server))

        (
            callback(server, HOST, PORT)
            if callback
            else print("Server listening on http://%s:%s" % (HOST, str(PORT)))
        )

        try:
            while True:
                try:
                    client_socket, _ = server.accept()
                    client_socket.settimeout(60)
                    threading.Thread(
                        target=self.handleClient, args=(client_socket,)
                    ).start()
                except TimeoutError:
                    ...
        except KeyboardInterrupt:
            _close(server)
            exit(0)
