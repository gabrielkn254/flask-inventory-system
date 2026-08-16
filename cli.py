import argparse
from utils import command_list, command_view, command_add, command_update, command_delete

BASE_URL = "http://127.0.0.1:5000"

def cli():
    parser = argparse.ArgumentParser(description = "Inventory Management CLI")
    parser.add_argument("--url", default=BASE_URL, help="Flask API base URL")
    sub = parser.add_subparsers()

    # command: list 
    list_parser = sub.add_parser("list", help="List all items in the inventory")
    list_parser.set_defaults(func=command_list)

    # command: view
    view_parser = sub.add_parser("view", help="View a single item from the inventory")
    view_parser.add_argument("--id", required=True, help="Item id you want to view")
    view_parser.set_defaults(func=command_view)

    # command: add
    add_parser = sub.add_parser("add", help="Add an item to inventory database")
    add_parser.add_argument("--name", required=True, help="Item name")
    add_parser.add_argument("--price", required=True, help="Item price")
    add_parser.add_argument("--quantity", required=True, help="Item quantity")
    add_parser.set_defaults(func=command_add)

    # command: update
    update_parser = sub.add_parser("update", help="Update an item details")
    update_parser.add_argument("--id", required=False, help="Item id to update")
    update_parser.add_argument("--name", required=False, help="Item name to update")
    update_parser.add_argument("--price", required=False, help="Item price  to update")
    update_parser.add_argument("--quantity", required=False, help="Item quantity  to update")
    update_parser.add_argument("--barcode", required=False, help="Item barcode  to update")
    update_parser.add_argument("--category", required=False, help="Item category  to update")
    update_parser.add_argument("--brand", required=False, help="Item brand  to update")
    update_parser.set_defaults(func=command_update)

    # command: delete
    delete_parser = sub.add_parser("delete", help="Delete an item from the inventory database")
    delete_parser.add_argument("--id", required=True, help="Item id you want to delete")
    delete_parser.set_defaults(func=command_delete)

    # create args object
    args = parser.parse_args()

    # handle error with help
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()