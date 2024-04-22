from WebServer import WebServer, Request, Response


app = WebServer(True)


# Setting up routing
@app.route("/", methods=["GET"])
def index(response: Response, request: Request) -> None:
    response.render("index")


@app.route("/about", methods=["GET"])
def about(response: Response, request: Request) -> None:
    response.render("about")


@app.route("/contact", methods=["GET"])
def contact(response: Response, request: Request) -> None:
    response.render("contact")


@app.route("/test/<name>/<userid>")
def test_name(res: Response, req: Request):
    print(req.user_parameters)
    res.send("Received")


@app.route("/users", methods=["POST"])
def test(response: Response, request: Request) -> None:
    response.send(
        [
            {"name": "Sachin Acharya", "age": 24},
            {"name": "Nancy Jewel Mc.Donie", "age": 24},
            {"name": "Peyton List", "age": 23},
        ],
        jsonify=True,
    )


@app.error_route(404)
def handle_404(response: Response, request: Request):
    response.send("<title>Response 404</title><h1>404: Not Found</h1>")

if __name__ == "__main__":
    app.run()
