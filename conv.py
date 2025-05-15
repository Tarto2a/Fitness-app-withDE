import json
import random

# تحميل بيانات JSON من ملف
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# تصنيف الوجبات بناءً على وصف الوجبة
def categorize_meal(description):
    if "oatmeal" in description.lower() or "eggs" in description.lower():
        return "Breakfast"
    elif "chicken" in description.lower() or "beef" in description.lower():
        return "Lunch"
    elif "salmon" in description.lower() or "tuna" in description.lower():
        return "Dinner"
    else:
        return "Snack"

# استخراج الوجبات مع تصنيفها وتحويل البيانات
def process_data(data):
    processed_meals = []

    for food in data['SRLegacyFoods']:
        description = food['description']
        nutrients = {nutrient['nutrient']['name']: nutrient['amount'] for nutrient in food['foodNutrients']}
        
        # تصنيف الوجبة
        meal_category = categorize_meal(description)

        # استخراج الوجبة المجهزة مع تفاصيلها
        meal = {
            "name": description,
            "category": meal_category,
            "calories": nutrients.get('Energy', 0),
            "protein": nutrients.get('Protein', 0),
            "fat": nutrients.get('Total lipid (fat)', 0),
            "carbs": nutrients.get('Carbohydrate, by difference', 0)
        }
        
        processed_meals.append(meal)
    
    return processed_meals

# حفظ الوجبات في ملف JSON جديد
def save_data(processed_meals, output_file):
    with open(output_file, 'w') as file:
        json.dump(processed_meals, file, indent=4)

# تنفيذ السكريبت
input_file = r'C:\Users\USER\OneDrive\Desktop\GA\FoodData_Central_sr_legacy_food_json_2021-10-28.json'  # ملف الـ USDA JSON
output_file = r'C:\Users\USER\OneDrive\Desktop\GA\New_FoodData_Central_sr_legacy_food_json_2021-10-28.json'  # الملف الناتج

data = load_data(input_file)
processed_meals = process_data(data)
save_data(processed_meals, output_file)

print(f"تم تحويل البيانات بنجاح وحفظها في {output_file}")
