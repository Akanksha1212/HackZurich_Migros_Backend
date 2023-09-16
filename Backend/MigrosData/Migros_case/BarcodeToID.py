import pandas as pd
import json
import glob
from IPython.display import display
import os




os.chdir("Backend/MigrosData/Migros_case/products/en")
df = pd.DataFrame()
count = 0
total = 0
for file in glob.glob("*.json"):
    total += 1

   
    with open(file, "r") as f:
        json_data = json.load(f)
        related_products = json_data.get("related_products", 0)
        if related_products == 0:
            count += 1
            print(count)
        # else:
        #     for barcode in json_data["gtins"]:

        #         row = {'barcode': barcode, 'id': json_data["id"]}
        #         df = df._append(row, ignore_index=True)

print(total)
print(count)
    


# display(df)
# df.to_csv("barcode_to_id.csv", index=False)


