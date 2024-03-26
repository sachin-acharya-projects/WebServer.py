from .Types import *
from .Settings import *
from functools import wraps
import socket
import datetime
import re
import os
import threading
import json
import keyboard
import sys
from dataclasses import dataclass


__all__ = ["render_template", "WebSocket", "jsonify"]


def jsonify(data: dict):
    return json.dumps(data)


def render_template(filename) -> str:
    with open(os.path.join(TEMPLATE_FOLDER, filename)) as file:
        return file.read()


@dataclass
class ContentType:
    HTML: str = "text/html"
    CSS: str = "text/css"
    JAVASCRIPT: str = "application/javascript"
    JSON: str = "application/json"
    OCTSTREAM: str = "application/octet-stream"  # ? For Binary

    def get(
        self,
        key: Literal["HTML", "CSS", "JAVASCRIPT", "JSON", "OCTSTREAM"],
        default: str = "application/octet-stream",
    ) -> Any:
        return getattr(self, key, default)


class WebSocket:
    def __init__(
        self, host: str = "127.0.0.1", port: int = 5500, debug: bool = False
    ) -> None:
        self._host = host
        self._port = port
        self._routes = {}
        self._error_handles = {}
        self._isDebug = debug
        self._ContentType = ContentType()

    def route(self, path: str, methods: List[RequestType] | None = None):
        def wrapper(func: Callable):
            self._routes[path] = {
                "handler": func,
                "methods": methods if methods else ["GET"],
            }
            return func

        return wrapper

    def handleError(self, status_code: int):
        def wrapper(func: Callable):
            self._error_handles[status_code] = {
                "handler": func,
            }

    def __log(self, *message):
        date = datetime.datetime.now()
        date = f"{date:[%d of %B, %Y %I:%M:%S %p]}"
        if self._isDebug:
            print(f"{date:<30}", *message)

    def __handleClient(self, client_socket: socket.socket) -> None:
        user_requests = client_socket.recv(1024).decode()
        if self._isDebug:
            print(user_requests)
            status = re.findall(r"([\w-]+): ([^\n]+)", user_requests)
            # print(dict(status))
        headers = user_requests.split("\r\n")
        request_line = headers[0]
        request_query = request_line.split()
        if not len(request_query) == 3:
            client_socket.close()
            return
        method, path, _ = request_query
        self.__log(method, path)

        if method.lower() != "get":
            client_socket.close()
            return

        # Handle Routing
        for route, route_info in self._routes.items():
            if re.match(f"^{route}$", path):
                if not "GET" in route_info["methods"]:
                    self.__send(
                        403,
                        "Not Allowed",
                        "Method '%s' on route '%s' is not allowed" % (method, path),
                        client_socket,
                    )
                    return

                handler_res = route_info["handler"]()
                status_code = 200
                response_body = handler_res
                if isinstance(handler_res, list) or isinstance(handler_res, tuple):
                    response_body, status_code = handler_res
                response = f"HTTP/1.1 {status_code}\r\nContent-Type: {self._ContentType.HTML}\r\n\r\n{response_body}".encode()
                client_socket.send(response)
                client_socket.close()
                return

        # Handling Static Content
        for static in STATIC_FOLDERS:
            filename = os.path.join(static, path.lstrip("/"))
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, "rb") as file:
                    attr = os.path.splitext(filename)[1].lstrip(".")
                    response = b"HTTP/1.1 200 OK\r\n" + self._ContentType.get(attr.upper()).encode() + b"\r\n\r\n" + file.read()
                    client_socket.send(response)
                    client_socket.close()
                    return

        # Return 404
        if 404 in self._error_handles:
            response = self._error_handles["handler"]
            response = b"HTTP/1.1 404 Not Found\r\n\r\n" + response.encode()
            client_socket.send(response)
            client_socket.close()
            return
        response = b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
        client_socket.send(response)
        client_socket.close()

    def __send(
        self, status_code: int, status_name: str, data: str, client: socket.socket
    ):
        # No ContentType added - change later
        response = "HTTP/1.1 %s %s\r\n\r\n%s" % str(status_code), status_name, data
        client.send(response)
        client.close()

    def run(self) -> NoReturn:
        import atexit

        def close(server):
            try:
                server.close()
            except OSError:
                ...
            sys.exit(0)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self._host, self._port))
        server.listen(5)

        atexit.register(lambda: close(server))
        print("Server listening on http://%s:%s" % (self._host, self._port))

        while True:
            try:
                try:
                    client_socket, _ = server.accept()
                except SystemExit:
                    ...

                # self.__log("Connected to tcp://%s:%s" % _)

                threading.Thread(
                    target=self.__handleClient, args=(client_socket,)
                ).start()
            except KeyboardInterrupt:
                server.close()
                break
