# NetJin - Simple Python Web Server Implementation

## Overview

`NetJin` is a lightweight web server implemented in Python using sockets. It provides a simple implementation of the HTTP protocol, allowing users to build and run web applications with ease.

## Features

-   **Routing**: Easily define routes for different URLs and HTTP methods.
-   **Request Handling**: Handle incoming HTTP requests and process them accordingly.
-   **Response Rendering**: Render HTML templates for generating dynamic content and return other responses as well.
-   **Error Handling**: Customizable error handling for managing HTTP errors.

## Installation

You can install `NetJin` using pip:

```bash
pip install WebServer
```

Alternatively, you can clone or download the repository and include the `NetJin` file in your project directory.

## Usage

1. Import the necessary classes:

    ```python
    from WebServer import WebServer, Request, Response
    ```

2. Create an instance of the `WebServer` class:

    ```python
    app = WebServer(debug=True)
    ```

3. Define routes using the `@app.route()` decorator, specifying the URL path and supported HTTP methods. For example:

    ```python
    @app.route("/", methods=["GET"])
    def home(request: Request, response: response) -> None:
        return response.render("index") # This corresponse to index.html
    ```

4. Implement functions to handle each route, receiving `Response` and `Request` objects as parameters.

5. Run the server:

    ```python
    if __name__ == "__main__":
        app.run()
    ```

## Settings

To configure your project, create a file named `Settings.py` in a directory named `Configurations` at the root of your project. Define the required variables as needed. For example:

```python
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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Turn off (False) for production.
DEBUG: bool = True

# Server Configuration
HOST: str = "127.0.0.1"
PORT: int = 8000
ALLOWED_HOST: List[str] = []

# Path to HTML files
TEMPLATE_DIRS: str | List[str] = "templates"  # BASE_DIR / "templates"
# Path to static folders (Directory for CSS, JS, Image, etc.)
STATIC_DIRS: List[str] = ["statics"]  # BASE_DIR / "statics"
# Path for public directory (where non-static files are located.)
PUBLIC_DIR: str = "public"
# Path where media files are stored.
MEDIA_DIR: str = "media"
```

## Examples

Check out the [example](./example) directory for sample usage and demonstrations.

## Dependencies

-   No external dependencies. Uses only Python's built-in `socket` module.

## Contribution

Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

For any inquiries or support, please contact [acharyaraj.webserver@gmail.com](mailto:acharyaraj.webserver@gmail.com) or visit the [GitHub profile](https://github.com/sachin-acharya-projects/).

```bash
.
├── config/
│   ├── settings.py
│   ├── __init__.py
│   └── other_app_configurations.py
├── static/
│   ├── csses
│   └── javascripts
├── media/
│   ├── images
│   └── videos
├── public/
│   ├── logo
│   ├── robot.txt
│   └── manifest.json
├── views/
│   ├── index.html
│   └── Other HTMLs
└── main.py
```
