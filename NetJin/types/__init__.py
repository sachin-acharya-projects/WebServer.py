from typing import (
    Literal,
    Tuple,
    Callable,
    NoReturn,
    Self,
    TypedDict,
    TypeVar,
    Union,
    List,
    Any,
    Dict,
)

__all__ = [
    "Literal",
    "Tuple",
    "Callable",
    "NoReturn",
    "Self",
    "TypedDict",
    "TypeVar",
    "Union",
    "List",
    "Any",
    "Dict",
    "RequestMethod",
]

RequestMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "UPDATE"]
