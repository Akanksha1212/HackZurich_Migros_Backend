from fastapi import FastAPI
from app.database.database import Database

app = FastAPI()

database = Database()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# get mcheck value by barcode
@app.get("/mcheck/{barcode}")
def get_mcheck(barcode: str):
    ## retrieve product ID from barcode

    product_id = database.get_id_from_barcode(barcode)
    mcheck = database.get_mcheck_by_product_id(product_id)

    return {"mcheck": mcheck}
