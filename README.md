# WebServer.py - Simple Python Web Server Implementation

## Overview

`WebServer.py` is a lightweight web server implemented in Python using sockets. It provides a simple implementation of the HTTP protocol, allowing users to build and run web applications with ease.

## Features

-   **Routing**: Easily define routes for different URLs and HTTP methods.
-   **Request Handling**: Handle incoming HTTP requests and process them accordingly.
-   **Response Rendering**: Render HTML templates for generating dynamic content and return other responses as well.
-   **Error Handling**: Customizable error handling for managing HTTP errors.

## Getting Started

1. **Installation**: Clone or download the `WebServer.py` file into your project directory.

    ```powershell
    pip install WebServer
    ```

2. **Usage**:

    - Import the `WebServer`, `Request`, and `Response` classes into your Python script.
    - Define routes using the `@app.route()` decorator, specifying the URL path and supported HTTP methods.
    - Implement functions to handle each route, receiving `Response` and `Request` objects as parameters.
    - Optionally, define error routes using `@app.error_route()` for custom error handling.

3. **Example**:

    ```python
    from WebServer import WebServer, Request, Response

    app = WebServer(True)

    """Notes
    response.render("name"), will by-default look for name.html in root/templates directory, which can be changed from Settings.py file.

    Also, by-default, statics files (CSS, JS, Images, etc) are looked in root/statics folder. This is also configurable in Settings.py file.
    """

    # Define routes
    @app.route("/", methods=["GET"])
    def index(response: Response, request: Request) -> None:
        response.render("index")

    @app.route("/about", methods=["GET"])
    def about(response: Response, request: Request) -> None:
        response.render("about")

    # Run the server
    if __name__ == "__main__":
        app.run()
    ```

    [More Examples](./example)

4. **Run**: Execute your Python script to start the web server.

5. **Access**: Open your web browser and navigate to `http://localhost:8000` (default) to access your web application.

## Dependencies

-   No external dependencies. Uses only Python's built-in `socket` module.

## Contribution

Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or support, please contact [acharyaraj.webserver@gmail.com](mailto:acharyaraj.webserver@gmail.com) or [GitHub profile](https://github.com/sachin-acharya-projects/).
