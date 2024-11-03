from colorama import Fore, init
from typing import Any
import socket
import os
import json


try:
    exec("from settings import VIEWS")
except:
    from WebServer.config.settings import VIEWS

init(True)
__all__ = ["Response"]

class Response:
    def __init__(self, client: socket.socket) -> None:
        self.__client = client

    def render(
        self, filename: str, status_code: int = 200, status_text: str = ""
    ) -> int:
        """Render Template from template folder

        Args:
            filename (str): HTML filename with or without extensions

        Raises:
            FileNotFoundError: If HTML file doesn't exists.

        Returns:
            int: Amount of content trasmitted
        """
        if not filename.lower().endswith(".html") or not filename.lower().endswith(
            ".htm"
        ):
            filename += ".html"

        filename = os.path.join(os.getcwd(), VIEWS, filename)
        # filename = BASE_DIR / TEMPLATES / filename
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename) as file:
                return self.send(file.read(), status_code, status_text)
        raise FileNotFoundError(f"File '{filename}' doesn't exists.")

    def send(
        self,
        content: str | dict,
        status_code: int = 200,
        status_text: str = "OK",
        content_type: str = "text/html",
        jsonify: bool = False,
    ) -> int:
        """Send HTML content back to client

        Args:
            content (str): HTML Content to send
            status_code (int, optional): StatusCode to transmit. Defaults to 200.
            status_text (str, optional): Status Text. Defaults to "OK".
            content_type (str, optional): Content Type of Message. Defaults to "text/html".
            jsonify (bool, optional): Convert message into JSON object. Defaults to False.

        Returns:
            int: Amount of content transmitted.
        """
        if jsonify:
            content = json.dumps(content, indent=4)
            if content_type.lower() == "text/html":
                content_type = "application/json"

        response = "HTTP/1.1 %s %s\r\n%s\r\n\r\n%s" % (
            status_code,
            status_text,
            content_type,
            content,
        )

        try:
            status = self.__client.send(response.encode())
            self.__client.close()
            return status
        except OSError as e:
            print(f"{Fore.RED}OSError: {Fore.LIGHTRED_EX}{repr(e)}")
            return 0

    def set(self, key: str, value: Any) -> None:
        "Set attribute"
        setattr(self, key, value)

    def get(self, key: str, default: Any) -> Any:
        "Get attribute"
        return getattr(self, key, default)
