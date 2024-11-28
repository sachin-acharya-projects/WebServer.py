from WebServer import WebServer, Request, Response

app = WebServer(True)


@app.route("/", methods=["GET"])
def index(_: Request, response: Response):
    response.render("index.html", name="Sachin Acharya")


@app.route("/about", methods=["GET"])
def about(_: Request, response: Response):
    response.render("about.html")


@app.route("/contact", methods=["GET"])
def contact(_: Request, response: Response):
    response.render("contact.html")


@app.route("/test/<name>/<userid>")
def test_name(request: Request, response: Response):
    print(request.user_parameters)
    response.send("Received")


@app.route("/users", methods=["GET", "POST"])
def get_users(_: Request, response: Response):
    response.send(
        [
            [
                {"name": "Sachin Acharya", "age": 24},
                {"name": "Nancy Jewel Mc.Donie", "age": 24},
                {"name": "Peyton List", "age": 23},
            ]
        ],
        None,
        {
            "Authorization": "Dickie",
            "Content-Type": "text/plain"
        }
    )


if __name__ == "__main__":
    app.run()