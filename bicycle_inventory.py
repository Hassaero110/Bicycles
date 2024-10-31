import argparse
import pandas as pd
import os

folder_name = os.path.dirname(__file__)
file = os.path.join(folder_name, 'bicycle_inventory.json')

def clean_bicycle_inventory(file):

    uncleaned_bicycle_inventory_df = pd.read_json(file)
    cleaned_df = uncleaned_bicycle_inventory_df.dropna(subset=['model_id', 'price_gbp', 'weight_kg', 'in_stock'])
    result = cleaned_df.to_json(orient="records")

    return result


def filtered_bicycle_inventory(cleaned_json_string):

    cleaned_bicycle_inventory_df = pd.read_json(str(cleaned_json_string))
    filtered_df = cleaned_bicycle_inventory_df.query('type == "Mountain Bike" and price_gbp >= 1000 and in_stock == True')
    result = filtered_df.to_json(orient="records")

    return result


def brand_count(cleaned_json_string):

    cleaned_bicycle_inventory_df = pd.read_json(str(cleaned_json_string))
    bike_counts_df = cleaned_bicycle_inventory_df.groupby(['brand'])['brand'].count()
    result = bike_counts_df.to_json(orient='index')

    return result


def sorted(cleaned_json_string):

    cleaned_bicycle_inventory_df = pd.read_json(str(cleaned_json_string))
    sorted_df = cleaned_bicycle_inventory_df.sort_values(by=['price_gbp', 'weight_kg']) 
    sorted_df = sorted_df[['model_id', 'price_gbp', 'weight_kg']]
    result = sorted_df.to_json(orient='records')

    return result


def gbp_per_kg(cleaned_json_string):

    cleaned_bicycle_inventory_df = pd.read_json(str(cleaned_json_string))
    cleaned_bicycle_inventory_df['price_per_kg'] = cleaned_bicycle_inventory_df['price_gbp'] / cleaned_bicycle_inventory_df['weight_kg']
    result = cleaned_bicycle_inventory_df.to_json(orient='records')

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process bicycle inventory data.')
    parser.add_argument('function', choices=['filter', 'brand_count', 'sort', 'gbp_per_kg'], help='Function to run after cleaning the inventory data')
    args = parser.parse_args()

    folder_name = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(folder_name, 'bicycle_inventory.json')

    # Always run the clean function first
    x = clean_bicycle_inventory(file)

    # Run the specified function
    if args.function == 'filter':
        result = filtered_bicycle_inventory(x)
    elif args.function == 'brand_count':
        result = brand_count(x)
    elif args.function == 'sort':
        result = sorted(x)
    elif args.function == 'gbp_per_kg':
        result = gbp_per_kg(x)

    print(result)