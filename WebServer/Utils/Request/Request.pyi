from ...types import RequestType
from typing import TypedDict, Literal, Union, Dict
from dataclasses import dataclass, field


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

    def __post_init__(self): ...