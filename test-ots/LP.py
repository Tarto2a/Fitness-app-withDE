import json
from scipy.optimize import linprog
import time

# Load meals data
def load_meals_data():
    with open(r"C:\Users\USER\OneDrive\Desktop\GA\processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json", "r") as file:
        return json.load(file)

meals_data = load_meals_data()

# --- Linear Programming Functions ---

def create_lp_problem(target_macros):
    num_meals = len(meals_data)

    # Cost function: weighted squared error for each nutrient
    c = []
    for meal in meals_data:
        # Relative squared difference to penalize mismatch
        w_cal = ((meal['calories'] - target_macros['calories']/4)**2) / (target_macros['calories']**2)
        w_prot = ((meal['protein'] - target_macros['protein']/4)**2) / (target_macros['protein']**2)
        w_fat = ((meal['fat'] - target_macros['fat']/4)**2) / (target_macros['fat']**2)
        w_carb = ((meal['carbs'] - target_macros['carbs']/4)**2) / (target_macros['carbs']**2)

        # Give more importance to carbs if needed
        c.append(w_cal + w_prot + w_fat + 2 * w_carb)  # Note: "2 *" gives carbs more weight

    # One meal per category constraint
    A_eq = []
    b_eq = []
    categories = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
    for category in categories:
        row = [1 if meal['category'] == category else 0 for meal in meals_data]
        A_eq.append(row)
        b_eq.append(1)

    bounds = [(0, 1) for _ in range(num_meals)]

    return c, A_eq, b_eq, bounds



def solve_lp_problem(c, A_eq, b_eq, bounds):
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if result.success:
        meal_plan = {}
        for i, meal in enumerate(meals_data):
            if result.x[i] > 0.5:
                category = meal['category']
                meal_plan[category] = meal
        return meal_plan
    else:
        print("Linear programming failed to find a solution.")
        return None

# --- Accuracy Evaluation ---

def evaluate_accuracy(meal_plan, target_macros):
    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for meal in meal_plan.values():
        if isinstance(meal, dict):
            totals["calories"] += meal["calories"]
            totals["protein"] += meal["protein"]
            totals["fat"] += meal["fat"]
            totals["carbs"] += meal["carbs"]

    accuracy = {}
    for key in target_macros:
        target = target_macros[key]
        actual = totals[key]
        diff = abs(target - actual)
        accuracy[key] = round(100 * (1 - diff / target), 2) if target != 0 else 0.0
    return accuracy

# --- Example Run ---

if __name__ == "__main__":
    target_macros = {
        "calories": 2000,
        "protein": 100,
        "fat": 70,
        "carbs": 250
    }

    total_accuracy = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0
    }

    start_time = time.time()
    for _ in range(100):
        c, A_eq, b_eq, bounds = create_lp_problem(target_macros)
        best_plan = solve_lp_problem(c, A_eq, b_eq, bounds)

        if best_plan:
            accuracy = evaluate_accuracy(best_plan, target_macros)
            for macro in total_accuracy:
                total_accuracy[macro] += accuracy[macro]

    end_time = time.time()
    avg_accuracy = {macro: round(total / 100, 2) for macro, total in total_accuracy.items()}

    print(f"\nExecution Time: {end_time - start_time:.2f} seconds")
    print("\nAverage Accuracy (%):")
    for macro, avg_acc in avg_accuracy.items():
        print(f"{macro.capitalize()}: {avg_acc}%")
