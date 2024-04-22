from ..types import Callable, List, RequestType
from ..Utils.Request import Request
from ..Utils.Response import Response

from abc import ABC

import socket

__all__ = ["ServerBase"]

_HandleType = Callable[[Response, Request], None]

class ServerBase(ABC):
    def __init__(self) -> None: ...

    def route(
        self, path: str, methods: List[RequestType] | None = None
    ) -> Callable[[_HandleType], _HandleType]:
        """Create a Route using this decorator.

        Example:
            @route("/", methods=['GET', 'POST'])

            def home(Response response, Request request):
                return request.send("Hello, World!")

        Args:
            path (str): URL Fragment to which, the handler function is executed.
            methods (List[RequestType] | None, optional): Allowed HTTP Methods to which this method is triggered. Defaults to None.

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
