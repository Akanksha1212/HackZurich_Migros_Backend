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
    product_id = barcode[0:7]
    database.get_mcheck_by_product_id("110230800000")
    return
