import json

DB_PATH = "./data/db.json"

# Load data from db.json
def load_db() -> list:
    try:
        with open(DB_PATH, "r") as file:
            data = json.load(file)
            items = []
            for item in data["inventory"]:
                items.append(item)
        return items
    
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return []

# Save data to db.json
def save_db(items: list):
    data = {
        "inventory": items
    }

    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)