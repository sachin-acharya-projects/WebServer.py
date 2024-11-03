from pathlib import Path
from typing import List

__all__ = [
    "BASE_DIR",
    "DEBUG",
    "HOST",
    "PORT",
    "ALLOWED_HOST",
    "VIEWS",
    "STATIC_DIRS",
]


BASE_DIR = Path(__file__).resolve().parent.parent

# Server Configurations
HOST: str = "127.0.0.1"
PORT: int = 5500

DEBUG: bool = True
ALLOWED_HOST: List[str] = []


# Views and Static
VIEWS: str = "views"
STATIC_DIRS: List[str] = ["static"]


PUBLIC_DIR: str = "public"

MEDIA_DIR: str = "media"