from unittest.mock import patch, Mock

import pytest
import requests

from utils.external_api import format_product, search_product


BASE_URL = "https://world.openfoodfacts.org/api/v2"



# format_product tests


def test_format_product():
    product = {
        "product_name": "Test Milk",
        "brands": "Test Brand",
        "ingredients": "Milk, sugar",
        "categories": "Dairy",
        "image_url": "https://example.com/milk.jpg",
        "code": "123456789",
    }

    result = format_product(product)

    assert result == {
        "name": "Test Milk",
        "brands": "Test Brand",
        "ingredients": "Milk, sugar",
        "categories": "Dairy",
        "image_url": "https://example.com/milk.jpg",
        "barcode": "123456789",
    }


def test_format_product_missing_fields():
    product = {
        "product_name": "Test Milk"
    }

    result = format_product(product)

    assert result == {
        "name": "Test Milk",
        "brands": "",
        "ingredients": "",
        "categories": "",
        "image_url": "",
        "barcode": "",
    }



# search_product by barcode


@patch("utils.external_api.requests.get")
def test_search_product_by_barcode(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Milk",
            "brands": "Test Brand",
            "ingredients": "Milk",
            "categories": "Dairy",
            "image_url": "https://example.com/milk.jpg",
            "code": "123456789",
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = search_product(barcode="123456789")

    assert result == {
        "name": "Test Milk",
        "brands": "Test Brand",
        "ingredients": "Milk",
        "categories": "Dairy",
        "image_url": "https://example.com/milk.jpg",
        "barcode": "123456789",
    }

    mock_get.assert_called_once_with(
        f"{BASE_URL}/product/123456789.json",
        params={
            "fields": "code,product_name,brands,ingredients_text,categories,image_url"
        },
        headers={
            "User-Agent": "FlaskInventorySystem - Version 1.0 - Linux - Contact: gabriel@example.com"
        },
        timeout=10
    )


def test_search_product_barcode_not_found():
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "utils.external_api.requests.get",
        return_value=mock_response
    ):
        result = search_product(barcode="999999999")

    assert result is None


def test_search_product_barcode_no_product():
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": None
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "utils.external_api.requests.get",
        return_value=mock_response
    ):
        result = search_product(barcode="123456789")

    assert result is None



# search_product by name


@patch("utils.external_api.requests.get")
def test_search_product_by_name(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Test Milk",
                "brands": "Test Brand",
                "ingredients": "Milk",
                "categories": "Dairy",
                "image_url": "https://example.com/milk.jpg",
                "code": "123456789",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = search_product(name="Test Milk")

    assert result == {
        "name": "Test Milk",
        "brands": "Test Brand",
        "ingredients": "Milk",
        "categories": "Dairy",
        "image_url": "https://example.com/milk.jpg",
        "barcode": "123456789",
    }

    mock_get.assert_called_once_with(
        f"{BASE_URL}/search",
        params={
            "search_terms": "Test Milk",
            "search_simple": 1,
            "action": "process",
            "page_size": 1,
            "fields": "code,product_name,brands,ingredients_text,categories,image_url"
        },
        headers={
            "User-Agent": "FlaskInventorySystem - Version 1.0 - Linux - Contact: gabriel@example.com"
        },
        timeout=10
    )


def test_search_product_name_not_found():
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": []
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "utils.external_api.requests.get",
        return_value=mock_response
    ):
        result = search_product(name="Product That Does Not Exist")

    assert result is None



# search_product without parameters


def test_search_product_without_barcode_or_name():
    result = search_product()

    assert result is None



# API request errors


def test_search_product_barcode_request_error():
    with patch(
        "utils.external_api.requests.get",
        side_effect=requests.exceptions.RequestException(
            "Connection error"
        )
    ):
        with pytest.raises(requests.exceptions.RequestException):
            search_product(barcode="123456789")


def test_search_product_name_request_error():
    with patch(
        "utils.external_api.requests.get",
        side_effect=requests.exceptions.RequestException(
            "Connection error"
        )
    ):
        with pytest.raises(requests.exceptions.RequestException):
            search_product(name="Test Milk")



# HTTP errors


def test_search_product_barcode_http_error():
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )

    with patch(
        "utils.external_api.requests.get",
        return_value=mock_response
    ):
        with pytest.raises(requests.exceptions.HTTPError):
            search_product(barcode="123456789")


def test_search_product_name_http_error():
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error"
    )

    with patch(
        "utils.external_api.requests.get",
        return_value=mock_response
    ):
        with pytest.raises(requests.exceptions.HTTPError):
            search_product(name="Test Milk")