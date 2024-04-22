from dataclasses import dataclass
from typing import Literal, Any, TypedDict

__all__ = ['ContentType']

@dataclass
class ContentType:
    HTML: str = "text/html"
    CSS: str = "text/css"
    JAVASCRIPT: str = "application/javascript"
    JSON: str = "application/json"
    OCTSTREAM: str = "application/octet-stream"  # ? For Binary

    def get(
        self,
        key: Literal["HTML", "CSS", "JAVASCRIPT", "JSON", "OCTSTREAM"],
        default: str = "application/octet-stream",
    ) -> Any:
        return getattr(self, key, default)
    