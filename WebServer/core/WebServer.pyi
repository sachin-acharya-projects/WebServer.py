from ..Base import ServerBase

__all__ = ["WebServer"]


class WebServer(ServerBase):
    def __init__(self, debug: bool = True) -> None: ...