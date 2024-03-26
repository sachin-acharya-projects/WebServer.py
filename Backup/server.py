from typing import Literal, List, Tuple, Callable, Any, NoReturn
from functools import wraps
import threading
import socket
import re
import os


def render(filename: str) -> str:
    path = os.path.join("template", filename)
    with open(path) as file:
        return file.read()


class WebSocket:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.routes = {}

    def route(
        self, path: str, methods: List[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    ):
        def wrapper(func: Callable[[Any], Tuple[str, int]]):
            self.routes[path] = {"handler": func, "methods": methods}
            return func

        return wrapper

    def handle_client(self, client_socket: socket.socket) -> None:
        request_data = client_socket.recv(1024).decode()
        headers = request_data.split("\r\n")
        request_line = headers[0]
        method, path, _ = request_line.split()
        print(method, path)
        if method != "GET":
            client_socket.close()
            return
        for route, route_info in self.routes.items():
            if re.match(f"^{route}$", path):
                response_body, status_code = route_info["handler"]()
                response = f"HTTP/1.1 {status_code}\r\n\r\n{response_body}".encode()
                client_socket.send(response)
                client_socket.close()
                return
        else:
            filename = os.path.join("static/", path.lstrip("/"))
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, "rb") as file:
                    response = b"HTTP/1.1 200 OK\r\n\r\n" + file.read()
                    client_socket.send(response)
                    client_socket.close()
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
                client_socket.send(response)
                client_socket.close()

        client_socket.close()

    def run(self) -> NoReturn:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on http://{self.host}:{self.port}")

        while True:
            try:
                client_socket, _ = server_socket.accept()
                client_handler = threading.Thread(
                    target=self.handle_client, args=(client_socket,)
                )
                client_handler.start()
            except KeyboardInterrupt:
                client_socket.close()
                server_socket.close()
                break


app = WebSocket("127.0.0.1", 5500)


@app.route(path="/", methods=["GET"])
def index():
    return "<h1>Hello World</h1>", 200


@app.route(path="/home", methods=["GET"])
def home():
    return render("index.html"), 200


@app.route(path="/name", methods=["GET"])
def return_json():
    import json

    obj = {"name": "Sachin Acharya", "age": 24}

    data = json.dumps(obj)
    return data, 200


if __name__ == "__main__":
    app.run()
