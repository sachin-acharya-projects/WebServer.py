from NetJin.utils import extract_route_pattern
from NetJin.http.response import Response
from NetJin.http.request import Request, create_request_object  # type: ignore
from NetJin.types import Callable, List, RequestMethod, Dict, Tuple
from NetJin.config import STATIC_DIRS, BASE_DIR, HOST, PORT, DEBUG

import socket
from dataclasses import dataclass
from colorama import init, Fore
import datetime
import threading
import atexit
import mimetypes
import os

__all__ = ["WebServer"]
init(True)

_HandleType = Callable[[Request, Response], None]


@dataclass
class _RouteRecordType(object):
    handler: _HandleType
    methods: List[RequestMethod]


@dataclass
class _ErrorRecordType(object):
    handler: _HandleType

class WebServer(object):
    def __init__(self, debug: bool = True) -> None:
        self._routes: Dict[str, _RouteRecordType] = {}
        self._error_handlers: Dict[int, _ErrorRecordType] = {}
        self._isDebug = debug
    
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
    
    def handleClient(self, client: socket.socket) -> None:
        user_requests = client.recv(1024).decode()
        request = create_request_object(user_requests)

        if not request.method or not request.path:
            client.close()
            return

        if self._isDebug:
            self.log(request.method, request.path)

        # Handling Routing
        for route, route_info in self._routes.items():
            route_ = extract_route_pattern(route, request.path)
            if isinstance(route_, dict):
                response = Response(client)
                if request.method not in route_info.methods:
                    temp = self._error_handlers.get(405, None)
                    if temp:
                        temp.handler(request, response)
                        return

                    self.send(
                        client,
                        (405, "Not Allowed"),
                        "Method '%s' on route '%s' not allowed"
                        % (request.method, request.path),
                    )
                    return

                if not request.user_parameters:
                    request.user_parameters = route_
                else:
                    request.user_parameters.update(route_)

                route_info.handler(request, response)
                return

        # Handling Static Content
        for static in STATIC_DIRS:
            filename = os.path.join(static, request.path.lstrip("/"))
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, "rb") as file:
                    mimetype, _ = mimetypes.guess_type(filename)
                    if mimetype is None:
                        mimetype = ""
                    #! Change static serve; add cache control for static
                    self.send(client, (200, "OK"), file.read(), mimetype)
                    return

        #! Handle Error Condition (Make user configurable)
        temp = self._error_handlers.get(404, None)
        if temp:
            response = Response(client)
            temp.handler(request, response)
            return

        filepath = BASE_DIR / "views" / "errors" / "NotFound.html"
        with open(filepath) as file:
            self.send(
                client,
                (404, "Not Found"),
                file.read().replace("{{ pathname }}", request.path),
                "text/html",
            )
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
            / "views"
            / "errors"
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