from NetJin.http.response import Response
from NetJin.http.request import Request
from NetJin.types import Callable, List, RequestMethod, Tuple

import socket
from dataclasses import dataclass

__all__ = ["WebServer"]

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
        """Create an instance of a WebServer

        Args:
            debug (bool, optional): Use this for development. Defaults to True.
        """

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
        ...

    def error_route(self, status_code: int) -> Callable[[_HandleType], _HandleType]:
        """Handle HTTP Error routing

        Args:
            status_code (int): StatusCode for which this route-handler will be executed.

        Returns:
            Callable[[_HandleType], _HandleType]: Callable handler function.
        """
        ...

    def log(self, *messages) -> None:
        """Logging out messages to the console."""
        ...

    def send(
        self,
        client: socket.socket,
        status: Tuple[int, str],
        data: str | bytes,
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
        ...

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
        ...

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
        ...
