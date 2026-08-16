import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2"

def format_product(product):
    return {
        "name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "ingredients": product.get("ingredients", ""),
        "categories": product.get("categories", ""),
        "image_url": product.get("image_url", ""),
        "barcode": product.get("code", ""),
    }

def search_product(barcode=None, name=None):
    """Fetch a product from openfoodfacts by barcode or product name."""
    headers = {
        "User-Agent": "FlaskInventorySystem - Version 1.0 - Linux - Contact: gabriel@example.com"
    }

    if barcode:
        url = f"{BASE_URL}/product/{barcode}.json"
        try:
            response = requests.get(
                url,
                params={"fields":"code,product_name,brands,ingredients_text,categories,image_url"},
                headers=headers,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            if data.get("status") != 1 or not data.get("product"):
                return None

            return format_product(data["product"])
        except requests.exceptions.RequestException as e:
             raise e

    if name:
            url = f"{BASE_URL}/search"
            try:
                response = requests.get(
                    url,
                    params={
                        "search_terms": name,
                        "search_simple": 1,
                        "action": "process",
                        "page_size": 1,
                        "fields": "code,product_name,brands,ingredients_text,categories,image_url"
                    },
                    headers=headers,
                    timeout=10
                )
        
                response.raise_for_status()
                data = response.json()

                products = data.get("products", [])
                if not products:
                    return None
        
                return format_product(products[0])
            
            except requests.exceptions.RequestException as e:
                 raise e

    return None