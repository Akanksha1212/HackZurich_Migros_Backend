from fastapi import FastAPI
from app.database.database import Database
import requests


app = FastAPI()

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
    sustainable_swaps = database.get_sustainable_swaps(product_id)
    url = f"http://127.0.0.1:8080/similar_products/{product_id}?top_n=15"
    
    
    response = requests.get(url)
    response = response.json()
    sustainable_swaps_ML = database.get_sustainable_swaps_ML(response,product_id)
    combined = {**sustainable_swaps, **sustainable_swaps_ML}
    
    print(sustainable_swaps_ML)

    # print(response.json())
    # if len(sustainable_swap) < 3:
    # return response
    return sustainable_swaps

# @app.get("/sustainable_swaps_ML/{product_id}")
# def get_sustainable_swaps_ML(product_id: str):
#     url = "http://127.0.0.1:8080/similar_products/{product_id}"
#     response = requests.request("GET", url, data={"top_n": 5})

    

