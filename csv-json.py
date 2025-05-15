import json

# Load your original JSON file
with open(r'C:\Users\USER\OneDrive\Desktop\GA\daily_food_nutrition_dataset_1.json', 'r') as f:
    data = json.load(f)

# Transform the data
converted_data = [
    {
        "name": item["Food_Item"],
        "category": item["Meal_Type"],
        "calories": float(item["Calories (kcal)"]),
        "protein": float(item["Protein (g)"]),
        "fat": float(item["Fat (g)"]),
        "carbs": float(item["Carbohydrates (g)"])
    }
    for item in data
]

# Save the new JSON to a file
with open(r'C:\Users\USER\OneDrive\Desktop\GA\new_daily_food_nutrition_dataset.json', 'w') as f:
    json.dump(converted_data, f, indent=4)

print("Conversion complete. File saved as 'converted_data.json'.")
