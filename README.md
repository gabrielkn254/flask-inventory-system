# Summative Lab: Flask Inventory Management System

A small inventory management system built with Flask and python. That helps an employee view inventory, add products, edit price and stock, delete products, search OpenFoodFacts by barcode or product name with ease.

## Features
- Flask REST API with CRUD operations.
- JSON array/list used as simulated storage.
- OpenFoodFacts integration for product lookup by barcode or name.
- Browser-based administrator portal.
- CLI client for interacting with the API.
- Pytest unit tests with `pytest & unittest.mock`.

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
│   └── command_actions.py
│   └── db_operations.py
│   └── external_api.py
└── tests/
    ├── conftest.py
    ├── test_app.py
    ├── test_cli.py
    └── test_external_api.py
```
