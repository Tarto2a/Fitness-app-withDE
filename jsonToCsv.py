import json
import csv

# Input and output file names
json_file = r'C:\Users\USER\OneDrive\Desktop\OT\meal-planing-app\src\data\processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json'
csv_file = 'data.csv'

# Load JSON data
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# If the JSON is a list of dictionaries
if isinstance(data, list) and all(isinstance(entry, dict) for entry in data):
    # Get fieldnames from the first dictionary
    fieldnames = data[0].keys()

    # Write CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully converted {json_file} to {csv_file}")
else:
    print("JSON structure not supported. Expected a list of dictionaries.")
