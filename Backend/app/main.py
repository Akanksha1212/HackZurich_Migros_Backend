from fastapi import FastAPI
from app.database.database import Database
import requests

description = """
Welcome to the MigrosNudge API. 🚀

## Product Info

Retrieves information about a product from the Migros Database from its barcode ID.

## Sustainable swap

Given any barcode, returns a list of similar products with higher M-check scores using our ML model.

## Sustainability goal

Returns the sustainability goal for a customer's next shop.

## Checkout

Updates the user's details with their latest grocery shop which is fed into our model to calculate their next sustainability goal.


"""

app = FastAPI(title="MigrosNudge API" description=description)

database = Database()




@app.get("/")
def read_root():
    return {"Hello": "World"}


# get mcheck value by barcode
@app.get("/product_info/{barcode}")
def get_product_info(barcode: str):
    ## retrieve product ID from barcode

    product_id = database.get_id_from_barcode(barcode)
    mcheck = database.get_mcheck_by_product_id(product_id)
    product_details = database.get_product_info(product_id)

    return {"mcheck": mcheck, **product_details}


@app.get("/sustainable_swap/{barcode}")
def get_sustainable_swaps(barcode: str):
    product_id = database.get_id_from_barcode(barcode)
    sustainable_swap = database.get_sustainable_swaps(product_id)

    url = f"http://127.0.0.1:8080/similar_products/{product_id}?top_n=15"
    
    
    response = requests.get(url)
    response = response.json()

    sustainable_swaps_ML = database.get_sustainable_swaps_ML(response,product_id)
    combined = {**sustainable_swap, **sustainable_swaps_ML}
    

    return combined


@app.get("/sustainability_goal/{customer_id}")
def get_sustainability_goal():
    sustainability_goal = database.get_sustainability_goal()
    return round(sustainability_goal)


@app.get("/user_checkout/{total_score}/{customer_id}")
def update_user_goals(total_score):
    database.user_checkout("sample_customer",total_score)



@app.get("/product_sustainability_rank/{product_id}")
def get_product_price_rank(product_id: str):
    return database.get_product_price_rank(product_id)
