import json
import pandas as pd
from IPython.display import display


class Database:
    MIGROS_PRODUCT_BASE_PATH = "MigrosData/Migros_case/products/en/"
    barcode_df = pd.read_csv("MigrosData/Migros_case/barcode_to_id.csv")
   

    def get_mcheck_by_product_id(self, product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            print(data["m_check2"])
            return
        
    def get_id_from_barcode(self, barcode_id):

       
        data = self.barcode_df.loc[self.barcode_df['barcode'] == int(barcode_id)].copy()

        id =  data['id'].iloc[0]
        return id


        

