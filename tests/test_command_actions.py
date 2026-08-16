from types import SimpleNamespace
from unittest.mock import patch

import requests

from utils.command_actions import (
    api_request,
    command_list,
    command_view,
    command_add,
    command_update,
    command_delete,
    command_search,
)


BASE_URL = "http://127.0.0.1:5000"


# =========================================================
# api_request tests
# =========================================================

def test_api_request_success_json():
    mock_response = SimpleNamespace(
        ok=True,
        status_code=200,
        json=lambda: {"message": "success"},
        text=""
    )

    with patch("utils.command_actions.requests.request") as mock_request:
        mock_request.return_value = mock_response

        result = api_request(
            "GET",
            BASE_URL,
            "/inventory"
        )

    mock_request.assert_called_once_with(
        "GET",
        f"{BASE_URL}/inventory",
        json=None
    )

    assert result == {"message": "success"}


def test_api_request_with_payload():
    mock_response = SimpleNamespace(
        ok=True,
        status_code=201,
        json=lambda: {
            "id": 1,
            "name": "Milk"
        },
        text=""
    )

    payload = {
        "name": "Milk",
        "quantity": 10,
        "price": 100
    }

    with patch("utils.command_actions.requests.request") as mock_request:
        mock_request.return_value = mock_response

        result = api_request(
            "POST",
            BASE_URL,
            "/inventory",
            payload
        )

    mock_request.assert_called_once_with(
        "POST",
        f"{BASE_URL}/inventory",
        json=payload
    )

    assert result == {
        "id": 1,
        "name": "Milk"
    }


def test_api_request_connection_error(capsys):
    with patch(
        "utils.command_actions.requests.request",
        side_effect=requests.RequestException("Connection failed")
    ):
        result = api_request(
            "GET",
            BASE_URL,
            "/inventory"
        )

    assert result is None

    captured = capsys.readouterr()

    assert "API connection error" in captured.out
    assert "Connection failed" in captured.out


def test_api_request_error_response(capsys):
    mock_response = SimpleNamespace(
        ok=False,
        status_code=404,
        json=lambda: {"message": "Not found"},
        text=""
    )

    with patch("utils.command_actions.requests.request") as mock_request:
        mock_request.return_value = mock_response

        result = api_request(
            "GET",
            BASE_URL,
            "/inventory/999"
        )

    assert result is None

    captured = capsys.readouterr()

    assert "Error 404" in captured.out
    assert "Not found" in captured.out


def test_api_request_invalid_json():
    mock_response = SimpleNamespace(
        ok=True,
        status_code=200,
        json=lambda: (_ for _ in ()).throw(ValueError()),
        text="Plain text response"
    )

    with patch("utils.command_actions.requests.request") as mock_request:
        mock_request.return_value = mock_response

        result = api_request(
            "GET",
            BASE_URL,
            "/inventory"
        )

    assert result == {
        "message": "Plain text response"
    }


# =========================================================
# command_list tests
# =========================================================

def test_command_list(capsys):
    args = SimpleNamespace(
        url=BASE_URL
    )

    result = {
        "inventory": [
            {
                "id": 1,
                "name": "Test Product"
            }
        ]
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_list(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/inventory"
    )

    captured = capsys.readouterr()

    assert "Test Product" in captured.out


def test_command_list_api_error(capsys):
    args = SimpleNamespace(
        url=BASE_URL
    )

    with patch(
        "utils.command_actions.api_request",
        return_value=None
    ) as mock_api:

        command_list(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/inventory"
    )

    captured = capsys.readouterr()

    assert captured.out == ""


# =========================================================
# command_view tests
# =========================================================

def test_command_view(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="1"
    )

    result = {
        "id": 1,
        "name": "Test Product",
        "quantity": 10
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_view(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/inventory/1"
    )

    captured = capsys.readouterr()

    assert "Test Product" in captured.out
    assert "10" in captured.out


def test_command_view_api_error(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="999"
    )

    with patch(
        "utils.command_actions.api_request",
        return_value=None
    ) as mock_api:

        command_view(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/inventory/999"
    )

    captured = capsys.readouterr()

    assert captured.out == ""


# =========================================================
# command_add tests
# =========================================================

def test_command_add(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        name="Milk",
        quantity="10",
        price="100"
    )

    result = {
        "id": 2,
        "name": "Milk",
        "quantity": "10",
        "price": "100"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_add(args)

    expected_payload = {
        "name": "Milk",
        "quantity": "10",
        "price": "100"
    }

    mock_api.assert_called_once_with(
        "POST",
        BASE_URL,
        "/inventory",
        expected_payload
    )

    captured = capsys.readouterr()

    assert "Milk" in captured.out


def test_command_add_api_error(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        name="Milk",
        quantity="10",
        price="100"
    )

    with patch(
        "utils.command_actions.api_request",
        return_value=None
    ) as mock_api:

        command_add(args)

    mock_api.assert_called_once_with(
        "POST",
        BASE_URL,
        "/inventory",
        {
            "name": "Milk",
            "quantity": "10",
            "price": "100"
        }
    )

    captured = capsys.readouterr()

    assert captured.out == ""


# =========================================================
# command_update tests
# =========================================================

def test_command_update(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="1",
        name="Updated Product",
        price="150",
        quantity="20",
        barcode="123456789",
        image="new-image.jpg",
        categories="Food",
        brands="Test Brand",
        ingredients="Milk"
    )

    result = {
        "id": 1,
        "name": "Updated Product",
        "price": "150",
        "quantity": "20"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_update(args)

    expected_payload = {
        "name": "Updated Product",
        "price": "150",
        "quantity": "20",
        "barcode": "123456789",
        "image_url": "new-image.jpg",
        "categories": "Food",
        "brands": "Test Brand",
        "ingredients": "Milk"
    }

    mock_api.assert_called_once_with(
        "PATCH",
        BASE_URL,
        "/inventory/1",
        expected_payload
    )

    captured = capsys.readouterr()

    assert "Updated Product" in captured.out


def test_command_update_only_price():
    args = SimpleNamespace(
        url=BASE_URL,
        id="1",
        name=None,
        price="150",
        quantity=None,
        barcode=None,
        image=None,
        categories=None,
        brands=None,
        ingredients=None
    )

    result = {
        "id": 1,
        "price": "150"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_update(args)

    mock_api.assert_called_once_with(
        "PATCH",
        BASE_URL,
        "/inventory/1",
        {
            "price": "150"
        }
    )


def test_command_update_only_name():
    args = SimpleNamespace(
        url=BASE_URL,
        id="1",
        name="New Product",
        price=None,
        quantity=None,
        barcode=None,
        image=None,
        categories=None,
        brands=None,
        ingredients=None
    )

    result = {
        "id": 1,
        "name": "New Product"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_update(args)

    mock_api.assert_called_once_with(
        "PATCH",
        BASE_URL,
        "/inventory/1",
        {
            "name": "New Product"
        }
    )


def test_command_update_only_quantity():
    args = SimpleNamespace(
        url=BASE_URL,
        id="1",
        name=None,
        price=None,
        quantity="20",
        barcode=None,
        image=None,
        categories=None,
        brands=None,
        ingredients=None
    )

    result = {
        "id": 1,
        "quantity": "20"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_update(args)

    mock_api.assert_called_once_with(
        "PATCH",
        BASE_URL,
        "/inventory/1",
        {
            "quantity": "20"
        }
    )


def test_command_update_no_fields(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="1",
        name=None,
        price=None,
        quantity=None,
        barcode=None,
        image=None,
        categories=None,
        brands=None,
        ingredients=None
    )

    with patch(
        "utils.command_actions.api_request"
    ) as mock_api:

        command_update(args)

    captured = capsys.readouterr()

    assert "Provide" in captured.out

    mock_api.assert_not_called()


def test_command_update_api_error(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="1",
        name="Updated Product",
        price=None,
        quantity=None,
        barcode=None,
        image=None,
        categories=None,
        brands=None,
        ingredients=None
    )

    with patch(
        "utils.command_actions.api_request",
        return_value=None
    ) as mock_api:

        command_update(args)

    mock_api.assert_called_once_with(
        "PATCH",
        BASE_URL,
        "/inventory/1",
        {
            "name": "Updated Product"
        }
    )

    captured = capsys.readouterr()

    assert captured.out == ""


# =========================================================
# command_delete tests
# =========================================================

def test_command_delete(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="1"
    )

    result = {
        "message": "Item deleted successfully"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_delete(args)

    mock_api.assert_called_once_with(
        "DELETE",
        BASE_URL,
        "/inventory/1"
    )

    captured = capsys.readouterr()

    assert "deleted successfully" in captured.out


def test_command_delete_api_error(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        id="999"
    )

    with patch(
        "utils.command_actions.api_request",
        return_value=None
    ) as mock_api:

        command_delete(args)

    mock_api.assert_called_once_with(
        "DELETE",
        BASE_URL,
        "/inventory/999"
    )

    captured = capsys.readouterr()

    assert captured.out == ""


# =========================================================
# command_search tests
# =========================================================

def test_command_search_by_barcode(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        barcode="123456789",
        name=None
    )

    result = {
        "id": 1,
        "name": "Test Product",
        "barcode": "123456789"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_search(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/api/item?barcode=123456789"
    )

    captured = capsys.readouterr()

    assert "Test Product" in captured.out


def test_command_search_by_name(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        barcode=None,
        name="Test Product"
    )

    result = {
        "id": 1,
        "name": "Test Product"
    }

    with patch(
        "utils.command_actions.api_request",
        return_value=result
    ) as mock_api:

        command_search(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/api/item?name=Test Product"
    )

    captured = capsys.readouterr()

    assert "Test Product" in captured.out


def test_command_search_api_error(capsys):
    args = SimpleNamespace(
        url=BASE_URL,
        barcode="999999999",
        name=None
    )

    with patch(
        "utils.command_actions.api_request",
        return_value=None
    ) as mock_api:

        command_search(args)

    mock_api.assert_called_once_with(
        "GET",
        BASE_URL,
        "/api/item?barcode=999999999"
    )

    captured = capsys.readouterr()

    assert captured.out == ""