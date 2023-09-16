import json
import pandas as pd
import operator



class Database:
    MIGROS_PRODUCT_BASE_PATH = "MigrosData/Migros_case/products/en/"
    barcode_df = pd.read_csv("MigrosData/Migros_case/barcode_to_id.csv")

    def get_mcheck(self,data):
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


    def get_mcheck_by_product_id(self, product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            return self.get_mcheck(data)

         
    def get_id_from_barcode(self, barcode_id):

       
        data = self.barcode_df.loc[self.barcode_df['barcode'] == int(barcode_id)].copy()
        product_id =  data['id'].iloc[0]
        return product_id
    
    def product_info(self,data):
        res = {}
        res["name"] = data["name"]
        res["image"] = data["image_transparent"]["original"]
        res["price"] = data["price"]["item"]["price"]
        res["currency"] = data["price"]["currency"]

            
        return res
    
    def get_product_info(self,product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            return self.product_info(data)
    
    
        
    def get_sustainable_swaps(self,product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            original_product_mcheck = self.get_mcheck(data)
            related_data = data.get("related_products",0)
            if related_data == 0:
                return None
            else:
                 related_products = related_data["purchase_recommendations"]["product_ids"]
        for product in related_products:
            # print(product)
            choices = {}

            if product in self.barcode_df['id'].values:
                # print("yes")
               
                with open(self.MIGROS_PRODUCT_BASE_PATH + product + ".json") as f:
                    data = json.load(f)
                    mcheck = self.get_mcheck(data)
                    print(product,mcheck)
                choices[product] = mcheck
            # print(choices)
        if choices:
            # print(self.product_info("110231900000"))
            sustainable_product = max(choices.items(), key=operator.itemgetter(1))[0]
            mcheck = max(choices.items(), key=operator.itemgetter(1))[1]
            with open(self.MIGROS_PRODUCT_BASE_PATH + str(sustainable_product) + ".json") as f:
                data = json.load(f)
                sustainable_product_details = self.product_info(data)
            # print(sustainable_product_details)
            if mcheck > original_product_mcheck:
                return {"mcheck": mcheck, **sustainable_product_details}

            return {"None"}
 
            
                     


            
