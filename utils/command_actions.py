import requests
import json

# api requests

def api_request(method, base_url, path, payload=None):
    url = f"{base_url}{path}"

    # make a request
    try:
       response = requests.request(method, url, json=payload)
    except requests.RequestExeception as exc:
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

    if args.price is not None:
        payload["price"] = args.price
    if args.quantity is not None:
            payload["quantity"] = args.quantity
    if args.barcode is not None:
                payload["barcode"] = args.barcode
    if args.category is not None:
                    payload["category"] = args.category
    if args.brand is not None:
                    payload["brand"] = args.brand

    if not payload:
          print("Provide --price or --quantity")

    result = api_request("PATCH", args.url, f"/inventory/{args.id}", payload)
    if result is not None:
        print(json.dumps(result, indent=2))

# command: delete
def command_delete(args):
    result = api_request("DELETE", args.url, f"/inventory/{args.id}")
    if result is not None:
        print(json.dumps(result, indent=2))
        return