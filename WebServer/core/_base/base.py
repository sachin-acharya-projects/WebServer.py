from WebServer.types import *
from WebServer.config.settings import HOST, PORT, DEBUG, BASE_DIR
from WebServer.http.Request import Request
from WebServer.http.Response import Response

from dataclasses import dataclass
from abc import ABC, abstractmethod
from colorama import init, Fore

import datetime
import threading
import atexit

import socket
import os

__all__ = ["AbstractBase"]
init(autoreset=True)

_HandleType = Callable[[Response, Request], None]


class _RouteRecordType(TypedDict):
    handler: Callable[[Response, Request], None]
    methods: List[RequestMethod]


class _ErrorRecordType(TypedDict):
    handler: Callable[[Response, Request], None]


@dataclass
class _ContentType:
    HTML: str = "text/html"
    CSS: str = "text/css"
    JAVASCRIPT: str = "application/javascript"
    JSON: str = "application/json"
    OCTSTREAM: str = "application/octet-stream"

    def get(
        self,
        key: Literal["HTML", "CSS", "JAVASCRIPT", "JSON", "OCTSTREAM"],
        default: str = "application/octet-stream",
    ) -> str:
        return getattr(self, key, default)


class AbstractBase(ABC):
    def __init__(self) -> None:
        "Base class for WebServer"
        self._routes: Dict[str, _RouteRecordType] = {}
        self._error_handlers: Dict[int, _ErrorRecordType] = {}
        self._ContentType = _ContentType()

    def route(
        self, path: str, methods: List[RequestMethod] | None = None
    ) -> Callable[[_HandleType], _HandleType]:
        """Create a Route using this decorator.

        Example:
            @route("/", methods=['GET', 'POST'])

            def home(Response response, Request request):
                return request.send("Hello, World!")

        Args:
            path (str): URL Fragment to which, the handler function is executed.
            methods (List[RequestMethod] | None, optional): Allowed HTTP Methods to which this method is triggered. Defaults to None.

        Returns:
            Callable[[_HandleType], _HandleType]: Callable method that handles the routing specific operations.
        """

        def wrapper(handler: _HandleType) -> _HandleType:
            self._routes[path] = {"handler": handler, "methods": methods or ["GET"]}
            return handler

        return wrapper

    def error_route(self, status_code: int) -> Callable[[_HandleType], _HandleType]:
        """Handle HTTP Error routing

        Args:
            status_code (int): StatusCode for which this route-handler will be executed.

        Returns:
            Callable[[_HandleType], _HandleType]: Callable handler function.
        """

        def wrapper(handler: _HandleType) -> _HandleType:
            self._error_handlers[status_code] = {"handler": handler}
            return handler

        return wrapper

    def log(self, *messages) -> None:
        """Logs out message on the Console."""
        date = datetime.datetime.now()
        date = f"{date:[%d of %B, %Y %I:%M:S %p]}"
        if DEBUG:
            print(f"{date:<30}", *messages)

    @abstractmethod
    def handleClient(self, client: socket.socket) -> None:
        """Handle incomming TCP request from clients.

        Args:
            client (socket.socket): Client Socket

        Raises:
            NotImplemented: If not implemented, it will raise an exception (NotImplemented).
        """
        raise NotImplementedError("Not Implemented")

    def send(
        self,
        client: socket.socket,
        status: Tuple[int, str],
        data: str,
        content_type: str = "",
    ) -> int:
        """Sends response back to the client.

        Args:
            client (socket.socket): Client socket to which response is to be sent.
            status (Tuple[int, str]): HTTP Status Code to send.
            data (str): Content of data to send.
            content_type (str, optional): ContentType header for response. Defaults to "".

        Returns:
            int: Amount of bytes sent.
        """
        if isinstance(data, str):
            response = (
                "HTTP/1.1 %s %s\r\nContent-Type: %s\r\n\r\n" % (*status, content_type)
                + data
            )
            response = response.encode()
        else:
            response = (
                "HTTP/1.1 %s %s\r\nContent-Type: %s\r\n\r\n".encode()
                % (*status, content_type)
                + data
            )
        try:
            status = client.send(response)
            client.close()
            return client
        except OSError as e:
            self.__log(f"{Fore.RED}OSError: {Fore.LIGHTRED_EX}{repr(e)}")
            return 0

    def render_error(
        self,
        status: Tuple[int, str],
        response: Response,
        request: Request,
        client: socket.socket,
    ) -> int:
        """Handles error_route() pipelining.

        Args:
            status (Tuple[int, str]): StatusCode for which pipelining is to be added.
            response (Response): Response object to send to handler function.
            request (Request): Request object to send to handler function.
            client (socket.socket): Client socket to which response is to be sent.

        Returns:
            int: Amount of bytes sent.
        """
        status_code, status_text = status
        error_template = (
            BASE_DIR
            / "WebServer"
            / "Templates"
            / "Errors"
            / (str(status_code) + ".html")
        )
        temp = self._error_handers.get(status_code, None)
        if temp:
            temp["handler"](response, request)

        if os.path.exists(error_template):
            with open(error_template) as file:
                data = file.read().replace("{{ pathname }}", request.path)
                return self.__send(client, status, data, "text/html")
        data = {
            404: "URL '%s' Not Found" % request.path,
            405: "Method [%s] on '%s' Not Allowed" % (request.method, request.path),
        }.get(status_code, "%s - %s" % status)
        return self.__send(client, status, data)

    def run(
        self,
        callback: Callable[[socket.socket, str, int], None] | None = None,
        post_callback: Callable[[socket.socket], None] | None = None,
    ) -> None:
        """Start the server and subsequently handles incomming requests.

        Args:
            callback (((server: socket, host: str, port: int) -> None) | None, optional): Callback Function. It will be called when server starts listening. Defaults to None.
            post_callback (((server: socket) -> None) | None, optional): Callback function which will be called when server is turn off (intentionally or unintentionally) to release some resources. Defaults to None.
        """

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
                    threading.Thread(
                        target=self.handleClient, args=(client_socket,)
                    ).start()
                except TimeoutError:
                    ...
        except KeyboardInterrupt:
            _close(server)
            exit(0)
