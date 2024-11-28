from pathlib import Path
from typing import List

__all__ = [
    "BASE_DIR",
    "HOST",
    "PORT",
    "DEBUG",
    "ALLOWED_HOST",
    "TEMPLATE_DIRS",
    "STATIC_DIRS",
    "PUBLIC_DIR",
    "MEDIA_DIR",
]

BASE_DIR = Path(__file__).resolve().parent.parent

# Server Configurations
HOST: str = "127.0.0.1"
PORT: int = 5500
DEBUG: bool = True
ALLOWED_HOST: List[str] = []

# Views and Static
TEMPLATE_DIRS: str | List[str] = "views"
STATIC_DIRS: List[str] = ["static"]
PUBLIC_DIR: str = "public"
MEDIA_DIR: str = "media"
