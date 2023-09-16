import json
import pandas as pd
import operator
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split




class Database:
    MIGROS_PRODUCT_BASE_PATH = "MigrosData/Migros_case/products/en/"
    customer_data_df = pd.read_csv("MigrosData/Migros_case/sample_customer.csv")
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
        res["size"] = data["package"]["size"]
        res["price_per_kg"] = data["price"]["base"]["price"]

            
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
        choices = []
        for product in related_products:
            # print(product)
            

            if product in self.barcode_df['id'].values:
                # print("yes")
               
                with open(self.MIGROS_PRODUCT_BASE_PATH + product + ".json") as f:
                    data = json.load(f)
                    mcheck = self.get_mcheck(data)
                    print(product,mcheck)
                    
                    choices.append((product,mcheck))
                    print(choices)
            # print(choices)
        if choices:
            # print(self.product_info("110231900000"))
            print(choices)
            choices = sorted(choices, key=lambda x: x[1], reverse=True)
            
  # Get the top 3 (or fewer) sustainable product names.
            sustainable_products = []
            for product, mcheck in choices:
                if mcheck > original_product_mcheck:
                    sustainable_products.append((product,mcheck))
                if len(sustainable_products) == 3:
                    break
            
            
            res = {}
            for product in sustainable_products:
                print("product", product)
                mcheck = product[1]
                sustainable_product = product[0]
                print("S", sustainable_product)
           
                with open(self.MIGROS_PRODUCT_BASE_PATH + str(sustainable_product) + ".json") as f:
                    data = json.load(f)
                    sustainable_product_details = self.product_info(data)

                    res[sustainable_product] = {"mcheck": mcheck, **sustainable_product_details}
                 
                
            return res
        
    # def predict_goal():


    
    def sustainability_goal(self,customer_data,customer_category):
        customer_category /= 3

        avg_diff = self.customer_data_df['Diff'].mean() / 100
        avg_score = self.customer_data_df['Actual'].mean() / 100
        avg_score_normalised = (avg_score + 1) / 2
        previous_shop = self.customer_data_df.iloc[-1]
        a,b,c = 0.3333, 0.3333, 0.333 
        # print(avg_diff)
        # print(avg_score_normalised)
        # print(customer_category)

        previous_shop_goal = previous_shop['Goal']
        multiplier_range = min(20, 100-previous_shop_goal)
        multiplier = ((a*avg_diff) + (b*avg_score_normalised) + (c*customer_category)) * multiplier_range
        
        if previous_shop['Diff'] >= 0:
            return previous_shop_goal + multiplier
        return previous_shop_goal - multiplier
    

    def user_checkout(self,customer_id,goal,total_spend):
        new_row_data = {'Goal': goal, 'Actual': total_spend, 'Diff': total_spend - goal}  # Replace with your column values
        self.customer_data_df = self.customer_data_df.append(new_row_data, ignore_index=True)


        self.customer_data_df['Actual']








        


 
            
                     


            
