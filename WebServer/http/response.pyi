import socket
from typing import Any, Dict, List
from jinja2 import Template

__all__ = ["Response"]


class Response:
    """Http Response Object. This is the class that can be used to send response back to the client."""
    def __init__(self, client: socket.socket) -> None: ...

    def render(self, template: str | Template | List[str | Template], **context: Any) -> int:
        """Render HTML (Jinja) template file. This method pre-renders the
        HTML file and serve it making loading of webpages faster.

        Args:
            template (str): Name of the template to be rendered. Directory
                is obtained from TEMPLATE_DIRS const of setings.py file. This settngs.py
                file in the workspace is prioritized over the modules settings.py file.
        """
        ...

    def end(self, status: int) -> int:
        """Respond with blank message

        Args:
            status (int): Http Status for the response.

        Returns:
            int: Amount of bytes sent.
        """
        ...

    def send(
        self,
        data: Any,
        status: int | None = None,
        headers: Dict[str, str] | None = None,
    ) -> int:
        """Send response back to the client.

        Args:
            content (Any): Data or Message that is to be responded back to client.
            status (int): Http status code for response.
            headers (Dict[str, str] | None, optional): Http Response Headers. Defaults to None.

        Returns:
            int: Amount of bytes transfered to the client.
        """
        ...

    def add_header(
        self, headers: Dict[str, str], header: str, value: str, force: bool = False
    ) -> Dict[str, str]:
        """Add header with value to the headers dictionary. This is simple logic that adds header
        if given key is not already present in the dictionary.

        Args:
            headers (Dict[str, str]): Http Headers that will be sent to the client.
            header (str): Http Header that is to be added to given dictionary of headers.
            value (str): Value for the 'header'.
            force (bool, optional): Make sure the value of header is updated if the key already exists. Defaults to False.
        """
        ...

    def set(self, key: str, value: Any) -> None:
        "Set attribute to the response class"
        ...

    def get(self, key: str, default: Any) -> Any:
        "Get attribute from the response class"
        ...
