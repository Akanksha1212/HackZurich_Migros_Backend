import json
import pandas as pd
import operator
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import requests


class Database:
    visited_products = {}
    MIGROS_PRODUCT_BASE_PATH = "MigrosData/Migros_case/products/en/"
    customer_data_df = pd.read_csv("MigrosData/Migros_case/sample_customer.csv")
    barcode_df = pd.read_csv("MigrosData/Migros_case/barcode_to_id.csv")

    def get_price_per_g(self, data):
        if "price" not in data:
            return 0
        if "base" not in data["price"]:
            return 0
        if "price" not in data["price"]["base"]:
            return 0
        return data["price"]["base"]["price"] / data["price"]["base"]["quantity"]

    def get_price_per_g_by_product_id(self, product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            return self.get_price_per_g(data)

    def get_mcheck(self, data):
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
        data = self.barcode_df.loc[self.barcode_df["barcode"] == int(barcode_id)].copy()
        product_id = data["id"].iloc[0]
        return product_id

    def product_info(self, data):
        res = {}
        res["name"] = data["name"]
        res["image"] = data["image_transparent"]["original"]
        res["price"] = data["price"]["item"]["price"]
        res["currency"] = data["price"]["currency"]
        res["size"] = data["package"]["size"]
        res["price_per_kg"] = data["price"]["base"]["price"]

        return res

    def get_product_info(self, product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            return self.product_info(data)

    def get_sustainable_swaps(self, product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            original_product_mcheck = self.get_mcheck(data)
            related_data = data.get("related_products", 0)
            if related_data == 0:
                return None
            else:
                related_products = related_data["purchase_recommendations"][
                    "product_ids"
                ]
        choices = []
        for product in related_products:
            # print(product)

            if product in self.barcode_df["id"].values:
                # print("yes")

                with open(self.MIGROS_PRODUCT_BASE_PATH + product + ".json") as f:
                    data = json.load(f)
                    mcheck = self.get_mcheck(data)
                    print(product, mcheck)

                    choices.append((product, mcheck))
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
                    sustainable_products.append((product, mcheck))
                if len(sustainable_products) == 3:
                    break

            res = {}
            for product in sustainable_products:
                print("product", product)
                mcheck = product[1]
                sustainable_product = product[0]
                print("S", sustainable_product)

                with open(
                    self.MIGROS_PRODUCT_BASE_PATH + str(sustainable_product) + ".json"
                ) as f:
                    data = json.load(f)
                    sustainable_product_details = self.product_info(data)

                    res[sustainable_product] = {
                        "mcheck": mcheck,
                        **sustainable_product_details,
                    }

            return res

    # def predict_goal():

    def sustainability_goal(self, customer_data, customer_category):
        customer_category /= 3
        df_cleaned = self.customer_data_df.dropna(subset=["Diff", "Actual"]).astype(
            float
        )
        # print("mean", self.customer_data_df['Actual'].mean())

        avg_diff = self.customer_data_df["Diff"].mean() / 100
        avg_score = self.customer_data_df["Actual"].mean() / 100

        avg_score_normalised = (avg_score + 1) / 2
        previous_shop = self.customer_data_df.iloc[-1]
        a, b, c = 0.3333, 0.3333, 0.333

        previous_shop_goal = previous_shop["Goal"]
        multiplier_range = min(20, 100 - previous_shop_goal)
        multiplier = (
            (a * avg_diff) + (b * avg_score_normalised) + (c * customer_category)
        ) * multiplier_range

        if previous_shop["Diff"] >= 0:
            return previous_shop_goal + multiplier
        return previous_shop_goal - multiplier
    
    def get_sustainability_goal(self):
        previous_shop = self.customer_data_df.iloc[-1]
        previous_shop_goal = previous_shop["Goal"]
        return previous_shop_goal


    def user_checkout(self, customer_id, total_score):
        previous_shop = self.customer_data_df.iloc[-1]
        prev_goal = previous_shop["Goal"]
        diff = int(total_score) - int(prev_goal)

        self.customer_data_df.loc[self.customer_data_df.index[-1], "Actual"] = int(
            total_score
        )
        self.customer_data_df.loc[self.customer_data_df.index[-1], "Diff"] = int(diff)

        self.customer_data_df.to_csv(
            "MigrosData/Migros_case/sample_customer.csv", index=False
        )

        # Create a new row with the next "Goal" value
        new_goal = self.sustainability_goal("sample_customer", 2)
        new_goal = round(new_goal)
        new_row = {"Goal": new_goal, "Actual": None, "Diff": None}
        print(new_goal)

        self.customer_data_df = pd.concat(
            [self.customer_data_df, pd.DataFrame([new_row])], ignore_index=True
        )

        self.customer_data_df.to_csv(
            "MigrosData/Migros_case/sample_customer.csv", index=False
        )

    def get_product_price_rank(self, product_id):
        url = f"http://127.0.0.1:8080/similar_products/{product_id}?top_n=15"
        response = requests.get(url)
        
        # if product_id in self.visited_products:
        #     return self.visited_products[product_id]
        if response.status_code != 200:
            print("Error getting similar products")
            return "Error"
            
        response = response.json()
        price_per_g_list = []
        for product in response:
            price_per_g_list.append(self.get_price_per_g_by_product_id(product))
        price_per_g_list.sort(reverse=True)
        print(price_per_g_list)

        for product in response:
            target_price = self.get_price_per_g_by_product_id(product)
            max_price = price_per_g_list[0]
            min_price = price_per_g_list[-1]
            
        # return price_per_g_list.index(self.get_price_per_g_by_product_id(product_id)) / len(price_per_g_list)
            if max_price != min_price:

                res = (target_price - min_price) / (max_price - min_price)
                
            else:
                res = 0
            self.visited_products[product] = res

       
        return self.visited_products
    
    def get_sustainable_swaps_ML(self,related_products,product_id):
        with open(self.MIGROS_PRODUCT_BASE_PATH + product_id + ".json") as f:
            data = json.load(f)
            original_product_mcheck = self.get_mcheck(data)
        choices = []
        print(related_products)
        for product in related_products:
            # print(product)
            if product in self.barcode_df['id'].values:
    
            
                with open(self.MIGROS_PRODUCT_BASE_PATH + product + ".json") as f:
                    data = json.load(f)
                    mcheck = self.get_mcheck(data)
                    # print(product,mcheck)
                    if mcheck:
                        if mcheck > original_product_mcheck:
                    
                            choices.append((product,mcheck))
        # print("choices: ", choices)
        choices = sorted(choices, key=lambda x: x[1], reverse=True)
        
        sustainable_products = []
        for product, mcheck in choices:
            if mcheck > original_product_mcheck:
                sustainable_products.append((product,mcheck))
            
        # print("S: ", sustainable_products)
        
        res = {}
        for product in sustainable_products:
            mcheck = product[1]
            sustainable_product = product[0]
        
            with open(self.MIGROS_PRODUCT_BASE_PATH + str(sustainable_product) + ".json") as f:
                data = json.load(f)
                sustainable_product_details = self.product_info(data)
                res[sustainable_product] = {"mcheck": mcheck, **sustainable_product_details}
        print("ORIGINAL MCHECK", original_product_mcheck)
        return res
