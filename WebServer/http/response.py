from http import HTTPStatus
from jinja2 import (
    Environment,
    FileSystemLoader,
    ChoiceLoader,
    Template,
    TemplateNotFound,
)
from colorama import Fore, init
from typing import Any, Dict, List
import socket
import json

TEMPLATE_DIRS = None
try:
    exec("from settings import TEMPLATE_DIRS")
except ModuleNotFoundError:
    from WebServer.config.settings import TEMPLATE_DIRS

init(True)

__all__ = ["Response"]

if TEMPLATE_DIRS is None or isinstance(TEMPLATE_DIRS, str):
    template_loader = FileSystemLoader(TEMPLATE_DIRS if TEMPLATE_DIRS else "templates")
else:
    template_loader = ChoiceLoader(
        [FileSystemLoader(template) for template in TEMPLATE_DIRS]
    )
env = Environment(loader=template_loader)


class Response:
    def __init__(self, client: socket.socket) -> None:
        self.__client = client

    def render(self, template: str | Template | List[str | Template], **context: Any) -> int:
        try:
            _template = env.get_or_select_template(template)
            rendered_html = _template.render(context)
            return self.send(
                rendered_html, 200, {"Content-Type": "text/html; charset=utf-8"}
            )
        except TemplateNotFound:
            return self.send("File Not Found", 404, headers={"Connection": "close"})

    def end(self, status: int) -> int:
        return self.send("", status, headers={"Connection": "close"})

    def send(
        self,
        content: Any,
        status: int | None = None,
        headers: Dict[str, str] | None = None,
    ) -> int:
        headers = headers or {}
        status = status or 200

        data: str = content
        if isinstance(content, str):
            self.add_header(headers, "Content-Type", "text/plain; charset=utf-8")
        else:
            try:
                data = json.dumps(content)
                if isinstance(content, (dict, list)):
                    self.add_header(
                        headers, "Content-Type", "application/json; charset=utf-8"
                    )
            except (TypeError, ValueError):
                self.add_header(headers, "Content-Type", "text/plain; charset=utf-8")
                data = "Cannot parse data"
        try:
            status_phrase = HTTPStatus(status).phrase
        except ValueError:
            status_phrase = "Unknown Status Code"

        response = self.__prepare_response(
            data.encode(), f"{status} {status_phrase}", headers
        )
        try:
            # status_ = self.__client.sendall(response)
            status_ = self.__client.send(response)
            # self.__client.close()
            return status_
        except OSError as e:
            print(f"{Fore.RED}OSError: {Fore.LIGHTRED_EX}{repr(e)}")
            return 0

    def add_header(
        self, headers: Dict[str, str], header: str, value: str, force: bool = False
    ) -> Dict[str, str]:
        keys = [key.lower() for key in headers.keys()]
        if force:
            headers[header] = value
        elif header.lower() not in keys:
            headers[header] = value
        return headers

    def __prepare_response(
        self,
        content: bytes,
        status: str = "200 OK",
        headers: Dict[str, str] | None = None,
    ) -> bytes:

        headers = headers or {
            "X-Content-Type-Options": "nosniff",
            "Connection": "keep-alive",
        }

        header_response = "\r\n".join(f"{key}: {value}" for key, value in headers.items())
        content_length = len(content)

        response = (
            f"HTTP/1.1 {status}\r\n"
            f"Content-Length: {content_length}\r\n"
            f"{header_response}\r\n\r\n"
        )
        print(response.rstrip(), "\n")
        response = response.encode()

        if isinstance(content, str):
            content = content.encode()
        return response + content

    def set(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def get(self, key: str, default: Any) -> Any:
        return getattr(self, key, default)
