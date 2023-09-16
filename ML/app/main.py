from fastapi import FastAPI
from app.similar_item import SimilarItemRetriever
import os
import json
import pandas as pd


app = FastAPI()

DATA_DIR = "../Backend/MigrosData/Migros_case/products/en/"
file_paths = [
    os.path.join(DATA_DIR, file)
    for file in os.listdir(DATA_DIR)
    if file.endswith(".json")
]
product_ids = [json.load(open(file_path, "r"))["id"] for file_path in file_paths]
# load matrix
matrix = pd.read_pickle("final_matrix.pkl")


similar_item_retriever = SimilarItemRetriever(matrix=matrix, product_ids=product_ids)


@app.get("/similar_products/{product_id}")
def similar_products(product_id: str, top_n: int = 5):
    similar_items = similar_item_retriever.get_similar_products_by_id(product_id, top_n)
    return similar_items
