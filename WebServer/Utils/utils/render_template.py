from ...Configurations.Settings.Settings import TEMPLATES, BASE_DIR
import os


__all__ = ["render_template"]


def render_template(filename: str) -> str:
    """Render Template from template folder

    Args:
        filename (str): HTML filename with or without extensions

    Raises:
        FileNotFoundError: If HTML file doesn't exists.

    Returns:
        str: HTML Content #! (Optimize)
    """
    if not filename.lower().endswith(".html") or not filename.lower().endswith(".htm"):
        filename += ".html"

    if os.path.exists(filename) and os.path.isfile(filename):
        with open(BASE_DIR / filename) as file:
            return file.read()
    raise FileNotFoundError(f"File '{BASE_DIR / filename}' doesn't exists.")
