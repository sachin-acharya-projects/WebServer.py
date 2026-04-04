from NetJin import WebServer, Request, Response

app = WebServer(True)


@app.route("/", methods=["GET"])
def index(_: Request, response: Response):
    # Mock data for products
    featured_products = [
        {"id": 1, "name": "GlowBuds Pro", "price": "129.99"},
        {"id": 2, "name": "SkyWatch X", "price": "249.50"},
        {"id": 3, "name": "PowerBeam Pad", "price": "59.00"}
    ]
    response.render("index.html", featured_products=featured_products)


@app.route("/products", methods=["GET"])
def products(_: Request, response: Response):
    # Show all products (using same mock data for now)
    all_products = [
        {"id": 1, "name": "GlowBuds Pro", "price": "129.99"},
        {"id": 2, "name": "SkyWatch X", "price": "249.50"},
        {"id": 3, "name": "PowerBeam Pad", "price": "59.00"},
        {"id": 4, "name": "VisionGlass", "price": "899.99"},
        {"id": 5, "name": "NanoSound Mini", "price": "45.00"}
    ]
    # For now, let's just reuse index.html or create a simple list
    # I'll render index.html with the full list for this example
    response.render("index.html", featured_products=all_products)


@app.route("/products/<int:id>", methods=["GET"])
def product_detail(request: Request, response: Response):
    # Mock single product fetch
    product_id = (request.user_parameters or {}).get('id')
    product = {"name": f"Premium Gadget {product_id}", "price": "199.99", "description": "Highly advanced technology for your daily needs."}
    response.render("product.html", product=product)


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
        }
    )


if __name__ == "__main__":
    app.run()
