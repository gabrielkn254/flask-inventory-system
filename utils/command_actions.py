import requests
import json

# api requests

def api_request(method, base_url, path, payload=None):
    url = f"{base_url}{path}"

    # make a request
    try:
       response = requests.request(method, url, json=payload)
    except requests.RequestException as exc:
        print(f"API connection error: {exc}")
        return None

    # get body
    try:
        body = response.json()
    except ValueError:
        body = {"message": response.text}

    if not response.ok:
        print(f"Error {response.status_code}: {body}")
        return None

    return body

# COMMANDS ACTIONS
# command: list
def command_list(args):
    result = api_request("GET", args.url, "/inventory")
    if result is not None:
        print(json.dumps(result, indent=2))
        return

# command: view
def command_view(args):
    result = api_request("GET", args.url, f"/inventory/{args.id}")
    if result is not None:
        print(json.dumps(result, indent=2))
        return

# command: add
def command_add(args):
    payload = {
        "name":args.name,
        "quantity": args.quantity,
        "price": args.price
    }

    result = api_request("POST", args.url, "/inventory", payload)
    if result is not None:
        print(json.dumps(result, indent=2))

# command: update
def command_update(args):
    payload = {}

    if args.name is not None:
        payload["name"] = args.name
    if args.price is not None:
        payload["price"] = args.price
    if args.quantity is not None:
        payload["quantity"] = args.quantity
    if args.barcode is not None:
        payload["barcode"] = args.barcode
    if args.image is not None:
        payload["image_url"] = args.image
    if args.categories is not None:
        payload["categories"] = args.categories
    if args.brands is not None:
        payload["brands"] = args.brands
    if args.ingredients is not None:
        payload["ingredients"] = args.ingredients

    if not payload:
          print("Provide --price or --quantity")
          return

    result = api_request("PATCH", args.url, f"/inventory/{args.id}", payload)
    if result is not None:
        print(json.dumps(result, indent=2))

# command: delete
def command_delete(args):
    result = api_request("DELETE", args.url, f"/inventory/{args.id}")
    if result is not None:
        print(json.dumps(result, indent=2))
        return

# command: search
def command_search(args):
    query = f"barcode={args.barcode}" if args.barcode else f"name={args.name}"
    result = api_request("GET", args.url, f"/api/item?{query}")
    if result is not None:
        print(json.dumps(result, indent=2))
        return