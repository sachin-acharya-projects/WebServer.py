from socket import socket

from Server.Types import Tuple
from .Base import BaseServer
from .Utils.Request import create_request_object, Request
from .Utils.Response import Response
from .Utils.utils import ContentType, extract_route_pattern
from .Configurations.Settings import STATIC_DIRS, BASE_DIR
import re
import os

__all__ = ["WebServer"]


class WebServer(BaseServer):
    def __init__(self, debug: bool = True) -> None:
        super().__init__()
        self._isDebug = debug

    def __log(self, *messages) -> None:
        return super()._BaseServer__log(*messages)

    def __send(
        self, client: socket, status: Tuple[int, str], data: str, content_type: str = ""
    ) -> int:
        return super()._BaseServer__send(client, status, data, content_type)

    def handleClient(self, client: socket) -> None:
        user_requests = client.recv(1024).decode()
        request = create_request_object(user_requests)

        if not request.method or not request.path:
            client.close()
            return

        if self._isDebug:
            self.__log(request.method, request.path)

        # Handling Routing
        for route, route_info in self._routes.items():
            route_ = extract_route_pattern(route, request.path)
            if isinstance(route_, dict):
                if not request.method in route_info["methods"]:
                    self.__send(
                        client,
                        (405, "Not Allowed"),
                        "Method '%s' on route '%s' not allowed"
                        % (request.method, request.path),
                    )
                    return

                response = Response(client)
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
                    self.__send(
                        client,
                        (b"200", b"OK"),
                        file.read(),
                        self._ContentType.get(attr.upper()).encode(),
                    )
                    return

        #! Handle Error Condition
        data = "File Not '%s' Found" % request.path.rstrip("/")
        self.__send(client, (404, "Not Found"), f"File '{data}' Not Found", "")
