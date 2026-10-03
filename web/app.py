from flask import Flask, render_template, request
import json

app = Flask(__name__)


def load_products():
    with open("data/products.json", "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def home():
    products = load_products()
    return render_template("home.html", products=products)


@app.route("/products")
def products():
    all_products = load_products()

    category = request.args.get("category")
    search = request.args.get("search", "").strip().lower()

    filtered_products = all_products

    if category:
        filtered_products = [
            product for product in filtered_products
            if product["category"].lower() == category.lower()
        ]

    if search:
        filtered_products = [
            product for product in filtered_products
            if search in product["name"].lower()
        ]

    return render_template(
        "products.html",
        products=filtered_products,
        category=category,
        search=search
    )


@app.route("/product/<int:product_id>")
def product(product_id):
    products = load_products()

    selected_product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if selected_product is None:
        return "Producto no encontrado", 404

    return render_template(
        "product.html",
        product=selected_product
    )


@app.route("/cart")
def cart():
    return render_template("cart.html")


if __name__ == "__main__":
    app.run(debug=True)