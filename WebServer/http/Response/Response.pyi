from typing import Any

class Response:
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
        ...

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
        ...

    def set(self, key: str, value: Any) -> None:
        "Add Data (Key-Value pair) to Response Object. Can be useful for sharing data between middlewares."
        ...

    def get(self, key: str, default: Any) -> Any:
        "Get Data from Response Object that might have been added by the previous middlewares."
        ...
