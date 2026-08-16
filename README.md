# Summative Lab: Flask Inventory Management System

A small inventory management system built with Flask and python. That helps an employee view inventory, add products, edit price and stock, delete products, search OpenFoodFacts by barcode or product name with ease.

## Features
- Flask REST API with CRUD operations.
- JSON array/list used as simulated storage.
- OpenFoodFacts integration for product lookup by barcode or name.
- Browser-based administrator portal.
- CLI client for interacting with the API.
- Pytest unit tests with `pytest & unittest.mock`.

## Capabilities
1. An employee can add an item to inventory database
2. An employee can view a single item
3. An employee can update an item
4. An employee can delete an item
5. An employee can list the whole invetory
6. Permanent inventory storage

## Technologies Used
### Languages
- Python, Flask

### Package Manager
- Pipenv: Both managing packages and virtual env

### External dependacies
- Requests: to handle API requests
- Pytest --dev: 

### Workflow 
- Git: code workflow managing tool
- Github: store remote repo

## Getting started
To run this program you will need to fork this repo, and install on your local machine.

### Requirements
Python 3.10+ is recommended

### Installation
1. Fork & clone this repo
2. Navigate to the cloned repo
```bash
cd python-project-management-cli-tool
```
3. Install dependecies
```bash
pipenv install
```
4. Run CLI entry
```bash
python main.py
```

### REST API
To run the Flask application
```bash
python app.py
```

#### GET /inventory
Returns all inventory items.
```bash
http://127.0.0.1:5000/inventory
```

#### GET /inventory/<id>
Returns one inventory item.
```bash
http://127.0.0.1:5000/inventory/1
```

#### POST /inventory
Adds an item.
```bash
http://127.0.0.1:5000/inventory
"Content-Type: application/json"
"{"name": "Organic Almond Milk","quantity":10,"price":450,"barcode":"123456"}"
```

#### PATCH /inventory/<id>
Updates one or more fields.
```bash
http://127.0.0.1:5000/inventory/1
"Content-Type: application/json"
{"name": "Organic Almond Milk","quantity":10,"price":450,"barcode":"123456"}
```

#### DELETE /inventory/<id>
Deletes an item.
```bash
http://127.0.0.1:5000/inventory/1
```

#### GET /api/item?name=<name>
Looks up a product by name.
```bash
http://127.0.0.1:5000/api/item?name=coca
```

### CLI usage
Keep Flask running in one terminal, then open another terminal.

List inventory:
```bash
python cli.py list
```

View an item:
```bash
python cli.py view --id 1
```

Update stock:
```bash
python cli.py update --id 1 --quantity 50
```

Update price:
```bash
python cli.py update --id 1 --price 175
```
Delete:
```bash
python cli.py delete --id 1
```

Search by barcode:
```bash
python cli.py search --barcode 5449000000996
```

Search by name:
```bash
python cli.py search --name coca
```

### Testing
Run all tests.
```bash
pytest -v
```

## Project Structure
```text
flask-inventory-system/
├── app.py
├── cli.py
├── .gitignore
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── data/
│   └── db.json
├── utils/
│   └── __innit__.py
│   └── command_actions.py
│   └── db_operations.py
│   └── external_api.py
└── tests/
    ├── conftest.py
    ├── test_app.py
    ├── test_cli.py
    ├── test_command_actions.py
    └── test_external_api.py
```


## License
This project is licensed under the MIT License.