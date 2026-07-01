import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

categories = {
    "Furniture": ["Chair", "Desk", "Bookcase", "Table", "Sofa"],
    "Technology": ["Laptop", "Monitor", "Printer", "Phone", "Tablet"],
    "Office Supplies": ["Paper", "Binder", "Stapler", "Pen Set", "Envelope"]
}
regions = ["East", "West", "Central", "South"]

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
order_id = 1000
for i in range(2500):
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    region = random.choice(regions)
    order_date = start_date + timedelta(days=random.randint(0, date_range_days))

    base_price = {"Furniture": 250, "Technology": 400, "Office Supplies": 30}[category]
    sales = round(np.random.gamma(2, base_price / 2) + 10, 2)
    margin = np.random.normal(0.18, 0.12)
    profit = round(sales * margin, 2)

    # inject some messiness for the "cleaning" step
    if random.random() < 0.02:
        sales = np.nan
    if random.random() < 0.015:
        region = None
    date_str = order_date.strftime("%Y-%m-%d") if random.random() > 0.05 else order_date.strftime("%m/%d/%Y")

    rows.append({
        "Order ID": f"ORD-{order_id}",
        "Product": product,
        "Category": category,
        "Sales": sales,
        "Profit": profit,
        "Date": date_str,
        "Region": region
    })
    order_id += 1

df = pd.DataFrame(rows)
# inject duplicates
dupes = df.sample(30, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

df.to_csv("sales_data.csv", index=False)
print(df.shape)
print(df.head())
