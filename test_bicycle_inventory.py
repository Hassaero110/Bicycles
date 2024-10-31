import pytest
import pandas as pd
from bicycle_inventory import (
    clean_bicycle_inventory,
    filtered_bicycle_inventory,
    brand_count,
    sorted as sort_bicycles,
    gbp_per_kg,
)

@pytest.fixture
def sample_data(tmp_path):
    data = data = [
        {"model_id": 1, "model_name": "Trailblazer 3000", "brand": "CycloX", "type": "Road Bike", "price_gbp": 936, "weight_kg": 13.5, "in_stock": True},
        {"model_id": 2, "model_name": "Speedster Pro", "brand": "RoadFlex", "type": "Road Bike", "price_gbp": None, "weight_kg": 7.8, "in_stock": False},
        {"model_id": 3, "model_name": "Hybrid Elite", "brand": "UrbanRide", "type": "Hybrid Bike", "price_gbp": 585, "weight_kg": None, "in_stock": None},
        {"model_id": 4, "model_name": "Climber 500", "brand": "HillMaster", "type": "Mountain Bike", "price_gbp": 1053, "weight_kg": 14.0, "in_stock": True},
        {"model_id": 5, "model_name": "City Cruiser", "brand": "UrbanRide", "type": "Hybrid Bike", "price_gbp": 468, "weight_kg": 11.5, "in_stock": True},
        {"model_id": None, "model_name": "Sprint King", "brand": "SpeedRacer", "type": "Road Bike", "price_gbp": 2496, "weight_kg": 8.0, "in_stock": False},
        {"model_id": 7, "model_name": "All-Terrain", "brand": "CycloX", "type": "Mountain Bike", "price_gbp": 858, "weight_kg": 16.0, "in_stock": True},
        {"model_id": 8, "model_name": "Roadster", "brand": "SpeedRacer", "type": "Road Bike", "price_gbp": None, "weight_kg": 10.2, "in_stock": True},
        {"model_id": 9, "model_name": None, "brand": "HillMaster", "type": "Mountain Bike", "price_gbp": 720, "weight_kg": 10.0, "in_stock": True},
        {"model_id": 10, "model_name": "Urban Comet", "brand": "CityRide", "type": "Hybrid Bike", "price_gbp": 720, "weight_kg": 11.0, "in_stock": True},
        {"model_id": 11, "model_name": "Speed Racer X", "brand": "RoadFlex", "type": "Road Bike", "price_gbp": 1499, "weight_kg": 7.5, "in_stock": False},
        {"model_id": 12, "model_name": "Trail Master 500", "brand": "CycloX", "type": "Mountain Bike", "price_gbp": 980, "weight_kg": 14.0, "in_stock": True}
    ]

    df = pd.DataFrame(data)
    json_data = df.to_json(orient='records')

    # Writing sample data to a temporary JSON file
    temp_file = tmp_path / "bicycle_inventory.json"
    temp_file.write_text(json_data)

    return str(temp_file), df

def test_clean_bicycle_inventory(sample_data):
    temp_file, df = sample_data

    result_json_string = clean_bicycle_inventory(temp_file)
    result_df = pd.read_json(result_json_string)
    expected_df = df.dropna(subset=['model_id', 'price_gbp', 'weight_kg', 'in_stock'])

    # Ensure consistent data types
    dtype_mapping = {
        'model_id': 'int64',
        'model_name': 'object',
        'brand': 'object',
        'type': 'object',
        'price_gbp': 'float64',
        'weight_kg': 'float64',
        'in_stock': 'bool'
    }

    result_df = result_df.astype(dtype_mapping)
    expected_df = expected_df.astype(dtype_mapping)

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        expected_df.reset_index(drop=True)
    )


def test_filtered_bicycle_inventory(sample_data):
    temp_file, df = sample_data

    cleaned_json_string = clean_bicycle_inventory(temp_file)
    filtered_json_string = filtered_bicycle_inventory(cleaned_json_string)
    result_df = pd.read_json(str(filtered_json_string))

    cleaned_df = pd.read_json(str(cleaned_json_string))
    expected_df = cleaned_df.query('type == "Mountain Bike" and price_gbp >= 1000 and in_stock == True')

    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def test_brand_count(sample_data):
    temp_file, df = sample_data

    cleaned_json_string = clean_bicycle_inventory(temp_file)
    brand_count_json_string = brand_count(cleaned_json_string)
    result_series = pd.read_json(str(brand_count_json_string))

    cleaned_df = pd.read_json(str(cleaned_json_string))
    expected_series = cleaned_df.groupby('brand')['brand'].count()

    pd.testing.assert_series_equal(result_series.sort_index(), expected_series.sort_index())


def test_sorted(sample_data):
    temp_file, df = sample_data

    cleaned_json_string = clean_bicycle_inventory(temp_file)
    sorted_json_string = sort_bicycles(cleaned_json_string)
    result_df = pd.read_json(str(sorted_json_string))

    cleaned_df = pd.read_json(str(cleaned_json_string))
    expected_df = cleaned_df.sort_values(by=['price_gbp', 'weight_kg'])[['model_id', 'price_gbp', 'weight_kg']]

    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def test_gbp_per_kg(sample_data):
    temp_file, df = sample_data

    cleaned_json_string = clean_bicycle_inventory(temp_file)
    gbp_per_kg_json_string = gbp_per_kg(cleaned_json_string)
    result_df = pd.read_json(str(gbp_per_kg_json_string))

    cleaned_df = pd.read_json(str(cleaned_json_string))
    cleaned_df['price_per_kg'] = cleaned_df['price_gbp'] / cleaned_df['weight_kg']

    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), cleaned_df.reset_index(drop=True))
