import openfoodfacts

api = openfoodfacts.API(
    username = None,
    password = None,
    country = "world",
    user_agent="FlaskInventorySystem/1.0"
)

search_results = api.product.text_search("coke")
print(search_results)