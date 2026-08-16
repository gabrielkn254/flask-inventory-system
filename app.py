from flask import Flask, request, jsonify
from utils import save_db, load_db, search_product

app = Flask(__name__)

# home
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Inventory System"}), 200

# fetch all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    items = load_db()

    return jsonify({"inventory": items}), 200

# add a new item
@app.route("/inventory", methods=["POST"])
def add_item():
    # get data from request
    data = request.get_json(silent=True) or {}

    # check if all required fields are there
    required = ["name", "quantity", "price"]
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error" : f"missing_fields: {missing}"}), 400

    # validate price & quantity values
    try:
        quantity = int(data["quantity"])
        price = float(data["price"])
    except (TypeError, ValueError):
        return jsonify({"error" : "Quantity & price must be numbers"}), 400

    if quantity < 0 or price < 0:
        return jsonify({"error" : "Quantity & price cannot be negative"}), 400

    # load db, create & append item object, save db, reload db for response
    try:
        openfood_product = search_product(name = str(data["name"]).strip())
        print(str(openfood_product))
    
        items = load_db()
        item = {
            "id": len(items) + 1,
            "barcode": openfood_product.get("barcode"),
            "name": str(data["name"]).strip(),
            "quantity": quantity,
            "price": price,
            "image_url": openfood_product.get("image_url"),
            "categories": openfood_product.get("categories"),
            "brands": openfood_product.get("brand"),
            "ingredients": openfood_product.get("ingredients")
        }
        
        items.append(item)
        save_db(items)

        updated_items = load_db()
        return jsonify({"Item successfully added!": item, "inventory":updated_items}), 201
    
    except Exception as exc:
        return jsonify({"Error" : f"External API request failed: {exc}"}), 502

# Fetch a single item by ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    # load db & get item
    items = load_db()
    item = next((i for i in items if i["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item), 200

# update a item by ID
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    # load db & get item
    items = load_db()
    item = next((i for i in items if i["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    # get & validate data
    data = request.get_json(silent=True) or {}

    allowed_fields = {"barcode", "name", "quantity", "price", "image_url", "categories", "brands", "ingredients"}
    unknown_fields = set(data) - allowed_fields

    if unknown_fields:
        return jsonify({"error": f"Invalid fields provided: {unknown_fields}"}), 400
    
    if "quantity" in data:
        try:
            quantity = int(data["quantity"])
        except (TypeError, ValueError):
            return jsonify({"error": "Quantity must be an integer"}), 400
        if quantity < 0:
            return jsonify({"error": "Quantity cannot be nagative"}), 400
        item["quantity"] = quantity

    if "price" in data:
        try:
            price = float(data["price"])
        except (TypeError, ValueError):
            return jsonify({"error": "Quantity must be a number"}), 400
        if price < 0:
            return jsonify({"error": "Price cannot be nagative"}), 400
        item["price"] = price

    for each in items:
        if each["id"] == item["id"]:
            each["quantity"] = item["quantity"]
            each["price"] = item["price"]

            for field in allowed_fields - {"quantity", "price"}:
                if field in data:
                    each[field] = str(data[field].strip())
            item = each

    save_db(items)
    return jsonify({"Updated Item": item, "message": "Item was successfully updated"}), 200





# Delete a product by ID
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    # load db
    items = load_db()

    # get item
    item = next((i for i in items if i["id"] == item_id), None)

    if item is None:
        return jsonify({
            "error": "item not found"}), 404

    # delete item
    items.remove(item)
    for index, each in enumerate(items, start=1):
        each["id"] = index

    # updated db
    save_db(items)
    return jsonify({
        "message": "Item deleted successfully",
        "item": item}), 200

# Discover an item in openfoodfacts
@app.route("/api/item", methods=["GET"])
def api_item():
    barcode = request.args.get("barcode", "").strip()
    name = request.args.get("name", "").strip()

    if not barcode and not name:
        return jsonify({"error": "Provide either barcode or name"}), 400

    try:
        product = search_product(barcode=barcode, name=name)
    except Exception as exc:
        return jsonify({"error" : f"External API request failed: {exc}"}), 502

    if not product:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404

    return jsonify({"source": "OpenFoodFacts", "product": product})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)