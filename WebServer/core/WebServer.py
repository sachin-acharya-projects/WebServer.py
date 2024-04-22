from socket import socket

from ..Base import ServerBase
from ..Utils.Request import create_request_object
from ..Utils.Response import Response
from ..Utils.utils import extract_route_pattern
from ..Configurations.Settings import STATIC_DIRS, BASE_DIR
import os

__all__ = ["WebServer"]


class WebServer(ServerBase):
    def __init__(self, debug: bool = True) -> None:
        super().__init__()
        self._isDebug = debug

    def handleClient(self, client: socket) -> None:
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
                if not request.method in route_info["methods"]:
                    temp = self._error_handers.get(405, None)
                    if temp:
                        temp["handler"](response, request)
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

                route_info["handler"](response, request)
                return

        # Handling Static Content
        for static in STATIC_DIRS:
            filename = os.path.join(static, request.path.lstrip("/"))
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, "rb") as file:
                    attr = os.path.splitext(filename)[1].lstrip(".")
                    self.send(
                        client,
                        (b"200", b"OK"),
                        file.read(),
                        self._ContentType.get(attr.upper()).encode(),
                    )
                    return

        #! Handle Error Condition (Make user configurable)
        temp = self._error_handlers.get(404, None)
        if temp:
            response = Response(client)
            temp["handler"](response, request)
            return

        filepath = BASE_DIR / "WebServer" / "Templates" / "Errors" / "404.html"
        with open(filepath) as file:
            self.send(
                client,
                (404, "Not Found"),
                file.read().replace("{{ pathname }}", request.path),
                self._ContentType.HTML,
            )
