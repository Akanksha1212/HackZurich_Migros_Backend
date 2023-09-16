from fastapi import FastAPI
from app.database.database import Database

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
    sustainable_swap = database.get_sustainable_swaps(product_id)
    return sustainable_swap

@app.get("/sustainability_goal/")
def get_sustainability_goal():

    sustainability_goal = database.sustainability_goal("sample_customer",2)
    return round(sustainability_goal)


