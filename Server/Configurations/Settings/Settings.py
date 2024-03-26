"""Settings.py
#! Change with Caution
This is application wide settings, handling various configuration. Change only when needed and knowingly.
"""

from pathlib import Path
from typing import List

__all__ = [
    "BASE_DIR",
    
    "DEBUG",
    
    "HOST",
    "PORT",
    "ALLOWED_HOST",
    
    "TEMPLATES",
    "STATIC_DIRS",
]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# ? Turn off (False) for production.
DEBUG: bool = True

# Server Configuration
HOST: str = "127.0.0.1"
PORT: int = 8000
ALLOWED_HOST: List[str] = []


# Path to HTML files
TEMPLATES: str = "templates"  # ? BASE_DIR / "templates"
# Path to static folders (Directory for CSS, JS, Image, etc.)
STATIC_DIRS: List[str] = ["statics"]  # ? BASE_DIR / "statics"
