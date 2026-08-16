from unittest.mock import patch
import pytest
from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)

    with app.test_client() as client:
        yield client


# HOME


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Welcome to Inventory System"
    }



# GET ALL INVENTORY


def test_get_inventory(client):
    inventory = [
        {
            "id": 1,
            "barcode": "123456789",
            "name": "Test Product",
            "quantity": 10,
            "price": 100.0,
            "image_url": "test.jpg",
            "categories": "Test",
            "brands": "Test Brand",
            "ingredients": ""
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert data["inventory"] == inventory
    assert len(data["inventory"]) == 1
    assert data["inventory"][0]["name"] == "Test Product"



# ADD ITEM


def test_add_item_success(client):
    existing_inventory = []

    openfood_product = {
        "name": "Test Product",
        "brands": "Test Brand",
        "ingredients": "Milk",
        "categories": "Dairy",
        "image_url": "test.jpg",
        "barcode": "123456789"
    }

    with patch(
        "app.search_product",
        return_value=openfood_product
    ), patch(
        "app.load_db",
        return_value=existing_inventory
    ), patch(
        "app.save_db"
    ) as mock_save:

        response = client.post(
            "/inventory",
            json={
                "name": "Test Product",
                "quantity": 10,
                "price": 100
            }
        )

    assert response.status_code == 201

    data = response.get_json()

    assert "Item successfully added!" in data
    assert "inventory" in data

    mock_save.assert_called_once()


def test_add_item_missing_name(client):
    response = client.post(
        "/inventory",
        json={
            "quantity": 10,
            "price": 100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "missing_fields" in data["error"]
    assert "name" in data["error"]


def test_add_item_missing_quantity(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Test Product",
            "price": 100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "missing_fields" in data["error"]
    assert "quantity" in data["error"]


def test_add_item_missing_price(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Test Product",
            "quantity": 10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "missing_fields" in data["error"]
    assert "price" in data["error"]


def test_add_item_invalid_quantity(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Test Product",
            "quantity": "abc",
            "price": 100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity & price must be numbers"


def test_add_item_invalid_price(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Test Product",
            "quantity": 10,
            "price": "abc"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity & price must be numbers"


def test_add_item_negative_quantity(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Test Product",
            "quantity": -5,
            "price": 100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity & price cannot be negative"


def test_add_item_negative_price(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Test Product",
            "quantity": 10,
            "price": -100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity & price cannot be negative"


def test_add_item_external_api_error(client):
    with patch(
        "app.search_product",
        side_effect=Exception("OpenFoodFacts unavailable")
    ):
        response = client.post(
            "/inventory",
            json={
                "name": "Test Product",
                "quantity": 10,
                "price": 100
            }
        )

    assert response.status_code == 502

    data = response.get_json()

    assert "External API request failed" in data["Error"]



# GET SINGLE ITEM


def test_get_item(client):
    inventory = [
        {
            "id": 1,
            "barcode": "123456789",
            "name": "Test Product",
            "quantity": 10,
            "price": 100.0
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["name"] == "Test Product"
    assert data["quantity"] == 10


def test_get_item_not_found(client):
    inventory = []

    with patch("app.load_db", return_value=inventory):
        response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"



# UPDATE ITEM


def test_update_item(client):
    inventory = [
        {
            "id": 1,
            "barcode": "123456789",
            "name": "Test Product",
            "quantity": 10,
            "price": 100.0,
            "image_url": "old.jpg",
            "categories": "Test",
            "brands": "Test Brand",
            "ingredients": ""
        }
    ]

    with patch(
        "app.load_db",
        return_value=inventory
    ), patch(
        "app.save_db"
    ) as mock_save:

        response = client.patch(
            "/inventory/1",
            json={
                "quantity": 20,
                "price": 150
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Item was successfully updated"
    assert data["Updated Item"]["quantity"] == 20
    assert data["Updated Item"]["price"] == 150

    mock_save.assert_called_once()


def test_update_item_name(client):
    inventory = [
        {
            "id": 1,
            "name": "Old Name",
            "quantity": 10,
            "price": 100.0,
            "barcode": "123456789",
            "image_url": "",
            "categories": "",
            "brands": "",
            "ingredients": ""
        }
    ]

    with patch(
        "app.load_db",
        return_value=inventory
    ), patch(
        "app.save_db"
    ):

        response = client.patch(
            "/inventory/1",
            json={
                "name": "New Name"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["Updated Item"]["name"] == "New Name"


def test_update_item_not_found(client):
    with patch("app.load_db", return_value=[]):
        response = client.patch(
            "/inventory/999",
            json={
                "quantity": 20
            }
        )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"


def test_update_item_invalid_field(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.patch(
            "/inventory/1",
            json={
                "invalid_field": "something"
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert "Invalid fields provided" in data["error"]


def test_update_item_invalid_quantity(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.patch(
            "/inventory/1",
            json={
                "quantity": "abc"
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity must be an integer"


def test_update_item_negative_quantity(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.patch(
            "/inventory/1",
            json={
                "quantity": -5
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity cannot be nagative"


def test_update_item_invalid_price(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.patch(
            "/inventory/1",
            json={
                "price": "abc"
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Quantity must be a number"


def test_update_item_negative_price(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.patch(
            "/inventory/1",
            json={
                "price": -100
            }
        )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Price cannot be nagative"



# DELETE ITEM


def test_delete_item(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        },
        {
            "id": 2,
            "name": "Second Product",
            "quantity": 5,
            "price": 50
        }
    ]

    with patch(
        "app.load_db",
        return_value=inventory
    ), patch(
        "app.save_db"
    ) as mock_save:

        response = client.delete("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Item deleted successfully"
    assert data["item"]["name"] == "Test Product"

    mock_save.assert_called_once()

    # Remaining item should be re-numbered
    assert inventory[0]["id"] == 1


def test_delete_item_not_found(client):
    inventory = [
        {
            "id": 1,
            "name": "Test Product",
            "quantity": 10,
            "price": 100
        }
    ]

    with patch("app.load_db", return_value=inventory):
        response = client.delete("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "item not found"



# EXTERNAL API ITEM SEARCH


def test_api_item_by_barcode(client):
    product = {
        "name": "Test Product",
        "brands": "Test Brand",
        "ingredients": "Milk",
        "categories": "Dairy",
        "image_url": "test.jpg",
        "barcode": "123456789"
    }

    with patch(
        "app.search_product",
        return_value=product
    ) as mock_search:

        response = client.get(
            "/api/item?barcode=123456789"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["source"] == "OpenFoodFacts"
    assert data["product"] == product

    mock_search.assert_called_once_with(
        barcode="123456789",
        name=""
    )


def test_api_item_by_name(client):
    product = {
        "name": "Test Milk",
        "brands": "Test Brand",
        "ingredients": "Milk",
        "categories": "Dairy",
        "image_url": "test.jpg",
        "barcode": "123456789"
    }

    with patch(
        "app.search_product",
        return_value=product
    ) as mock_search:

        response = client.get(
            "/api/item?name=Test%20Milk"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["source"] == "OpenFoodFacts"
    assert data["product"] == product

    mock_search.assert_called_once_with(
        barcode="",
        name="Test Milk"
    )


def test_api_item_without_parameters(client):
    response = client.get("/api/item")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Provide either barcode or name"


def test_api_item_not_found(client):
    with patch(
        "app.search_product",
        return_value=None
    ):

        response = client.get(
            "/api/item?name=Unknown%20Product"
        )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Product not found on OpenFoodFacts"


def test_api_item_external_api_error(client):
    with patch(
        "app.search_product",
        side_effect=Exception("OpenFoodFacts connection failed")
    ):

        response = client.get(
            "/api/item?name=Test%20Milk"
        )

    assert response.status_code == 502

    data = response.get_json()

    assert "External API request failed" in data["error"]