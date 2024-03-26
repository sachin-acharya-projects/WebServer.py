from urllib.parse import urlparse
from typing import Dict, TypedDict, Literal, Union
from ...Types import RequestType
from dataclasses import dataclass, field
import re


__all__ = ["Request", "create_request_object"]

_Headers = TypedDict(
    "_Headers",
    {
        "sec-ch-ua": str,
        "sec-ch-ua-mobile": str,
        "sec-ch-ua-platform": str,
        "Sec-Fetch-User": str | None,
        "Sec-Fetch-Site": str,
        "Sec-Fetch-Mode": str,
        "Sec-Fetch-Dest": str,
        "Accept": str,
        "User-Agent": str,
        "Referer": str | None,
        "Accept-Encoding": str,
        "Accept-Language": str,
        "Cache-Control": str | None,
        "Upgrade-Insecure-Requests": str | None,
        "Cookie": Dict[str, str],
    },
)


@dataclass
class Request:
    url: str

    # ? Dynamic Fields
    path: str = field(init=False)
    scheme: str = field(init=False)
    netloc: str = field(init=False)
    params: Dict[str, str] = field(init=False)
    queries: Dict[str, str] = field(init=False)
    fragment: Dict[str, str] = field(init=False)

    Host: str
    Connection: Literal["keep-alive", "close"]
    headers: Union[_Headers, Dict[str, str]]
    method: RequestType
    
    user_parameters: Dict[str, str] | None = field(init=False, default=None)

    def __post_init__(self):
        parser = urlparse(self.url)
        self.path = parser.path
        self.scheme = parser.scheme
        self.netloc = parser.netloc
        self.params = dict(re.findall(r";([^=;]+)=([^=;]+)", parser.params))
        self.queries = dict(re.findall(r"([^&=]+)=([^&=]*)", parser.query))
        self.fragment = dict(re.findall(r"#([^#]+)", parser.fragment))


def create_request_object(network_content: str) -> Request:
    network_content_obj: Dict[str, str] = dict(
        re.findall(r"([\w-]+): ([^\n]+)", network_content)
    )
    host = network_content_obj.get("Host", "").rstrip("\r")
    connection = network_content_obj.get("Connection", "").rstrip("\r")
    cookie = dict(
        re.findall(r"([^=;]+)=([^=;]+)", network_content_obj.get("Cookie", ""))
    )

    headers = network_content.split("\r\n")
    request_line = headers[0]
    request_query = request_line.split()

    method, path, _ = request_query if len(request_query) == 3 else (None, "", None)
    try:
        del network_content_obj["Host"]
        del network_content_obj["Connection"]
    except KeyError:
        ...
    return Request(
        Host=host,
        Connection=connection,
        headers={
            **network_content_obj,
            "Cookie": cookie,
            "Cache_Control": network_content_obj.get("Cache-Control", None),
            "Upgrade_Insecure_Requests": network_content_obj.get(
                "Upgrade-Insecure-Requests", None
            ),
            "Referer": network_content_obj.get("Referer", None),
            "Sec_Fetch_User": network_content_obj.get("Sec-Fetch-User", None),
        },
        method=method.upper() if method else "",
        url="http://" + host + path,
    )
