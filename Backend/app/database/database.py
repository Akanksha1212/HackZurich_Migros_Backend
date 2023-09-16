import json
import pandas as pd


class Database:
    MIGROS_PRODUCT_BASE_PATH = "MigrosData/Migros_case/products/en/"
    barcode_df = pd.read_csv("MigrosData/Migros_case/barcode_to_id.csv")

    def get_mcheck_by_product_id(self, product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            if "m_check2" not in data:
                return None
            if "carbon_footprint" in data["m_check2"]:
                if "ground_and_sea_cargo" not in data["m_check2"]["carbon_footprint"]:
                    return None
                return data["m_check2"]["carbon_footprint"]["ground_and_sea_cargo"][
                    "rating"
                ]
            elif "animal_welfare" in data["m_check2"]:
                return data["m_check2"]["animal_welfare"]["rating"]
            return None

         
    def get_id_from_barcode(self, barcode_id):

       
        data = self.barcode_df.loc[self.barcode_df['barcode'] == int(barcode_id)].copy()

        product_id =  data['id'].iloc[0]
        return product_id
    
    def get_product_info(self,product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            res = {}
            res["name"] = data["name"]
            res["image"] = data["image_transparent"]["original"]
            res["price"] = data["price"]["item"]["price"]
            
            return res
            
