import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from faker import Faker

load_dotenv(".env_vars")

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Initialize Faker
fake = Faker()
Faker.seed(42)

# Define Electronics categories and their characteristics
electronics_models = {
    "Smartphone": {
        "category": "Mobile",
        "price_range": (300, 1200),
        "brands": ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi"],
    },
    "Laptop": {
        "category": "Computer",
        "price_range": (500, 2500),
        "brands": ["Dell", "HP", "Lenovo", "Apple", "ASUS"],
    },
    "Tablet": {
        "category": "Mobile",
        "price_range": (200, 1000),
        "brands": ["Apple", "Samsung", "Amazon", "Microsoft"],
    },
    "Smartwatch": {
        "category": "Wearable",
        "price_range": (150, 800),
        "brands": ["Apple", "Samsung", "Fitbit", "Garmin"],
    },
    "Headphones": {
        "category": "Audio",
        "price_range": (50, 500),
        "brands": ["Sony", "Bose", "Apple", "Sennheiser"],
    },
    "Smart TV": {
        "category": "Entertainment",
        "price_range": (300, 2000),
        "brands": ["Samsung", "LG", "Sony", "TCL", "Vizio"],
    },
    "Gaming Console": {
        "category": "Gaming",
        "price_range": (200, 800),
        "brands": ["Sony", "Microsoft", "Nintendo", "Valve"],
    },
    "Camera": {
        "category": "Photography",
        "price_range": (400, 3000),
        "brands": ["Canon", "Nikon", "Sony", "Fujifilm"],
    },
}

# Financing options
financing_options = ["Cash", "Credit Card", "Installment", "Store Financing"]

# Sales staff
MAX_STAFF = 8
sales_staff = [fake.name() for _ in range(MAX_STAFF)]


# Generate random date within the past 3 years
def random_date(start_date=datetime(2022, 1, 1), end_date=datetime(2025, 3, 1)):
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)


# Generate dataset
MAX_NUM_RECORDS = 500
data = []

for _ in range(MAX_NUM_RECORDS):
    # Select random model
    model_name = random.choice(list(electronics_models.keys()))
    model_info = electronics_models[model_name]

    # Get model details
    category = model_info["category"]
    brand = random.choice(model_info["brands"])
    min_price, max_price = model_info["price_range"]

    # Generate sale date
    sale_date = random_date()

    # Generate sale price (base + brand adjustment + negotiation factor)
    base_price = random.randint(min_price, max_price)
    brand_factor = electronics_models[model_name]["brands"].index(brand) + 1
    brand_adjustment = brand_factor * 100  # Reduced adjustment for electronics
    negotiation_factor = random.uniform(0.95, 1.05)  # 5% discount to 5% markup

    sale_price = int((base_price + brand_adjustment) * negotiation_factor)

    # Calculate store profit
    cost_to_store = int(sale_price * 0.75)  # Approximation of store cost
    profit = sale_price - cost_to_store

    # Generate additional data
    year = random.randint(sale_date.year - 2, sale_date.year)
    customer_name = fake.name()
    customer_age = random.randint(18, 80)
    customer_gender = random.choice(["Male", "Female"])
    financing = random.choice(financing_options)
    salesperson = random.choice(sales_staff)

    data.append(
        {
            "sale_id": fake.uuid4()[:8],
            "sale_date": sale_date,
            "year": year,
            "model": model_name,
            "brand": brand,
            "category": category,
            "sale_price": sale_price,
            "cost_to_store": cost_to_store,
            "store_profit": profit,
            "customer_name": customer_name,
            "customer_age": customer_age,
            "customer_gender": customer_gender,
            "financing_type": financing,
            "salesperson": salesperson,
        }
    )


# Create DataFrame
df = pd.DataFrame(data)

# Display the first few rows
print(df.head())

# Save the data
path = os.getenv("SALES_DATA_PATH")
print(f"Saving data to {path}")
df.to_parquet(path, index=False)
