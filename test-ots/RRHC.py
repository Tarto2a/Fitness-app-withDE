import random
import json
import time

# Load meals data
def load_meals_data():
    with open(r"C:\Users\USER\OneDrive\Desktop\GA\processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json", "r") as file:
        return json.load(file)

meals_data = load_meals_data()

# --- Hill Climbing with Random Restarts ---

def fitness(meal_plan, target_macros):
    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for meal in meal_plan.values():
        if isinstance(meal, dict):
            totals["calories"] += meal["calories"]
            totals["protein"] += meal["protein"]
            totals["fat"] += meal["fat"]
            totals["carbs"] += meal["carbs"]

    weights = {"calories": 1.0, "protein": 1.0, "fat": 1.0, "carbs": 1.0}
    score = sum(weights[key] * (abs(target_macros[key] - totals[key]) / (target_macros[key] + 1e-5)) for key in target_macros)
    return score

def mutate(plan, mutation_rate=0.3):
    new_plan = plan.copy()
    for key in new_plan:
        if random.random() < mutation_rate:
            category = new_plan[key]["category"]
            new_plan[key] = random.choice([m for m in meals_data if m["category"] == category])
    return new_plan

def create_random_plan():
    return {
        "breakfast": random.choice([m for m in meals_data if m["category"] == "Breakfast"]),
        "lunch": random.choice([m for m in meals_data if m["category"] == "Lunch"]),
        "dinner": random.choice([m for m in meals_data if m["category"] == "Dinner"]),
        "snack": random.choice([m for m in meals_data if m["category"] == "Snack"]),
    }

def hill_climbing(target_macros, iterations=500):
    current_plan = create_random_plan()

    for _ in range(iterations):
        new_plan = mutate(current_plan)
        if fitness(new_plan, target_macros) < fitness(current_plan, target_macros):
            current_plan = new_plan

    return current_plan

def random_restarts_hill_climbing(target_macros, restarts=5, iterations_per_restart=500):
    best_plan = None
    best_score = float('inf')

    for _ in range(restarts):
        plan = hill_climbing(target_macros, iterations=iterations_per_restart)
        plan_score = fitness(plan, target_macros)
        if plan_score < best_score:
            best_score = plan_score
            best_plan = plan

    return best_plan

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
        best_plan = random_restarts_hill_climbing(target_macros, restarts=5, iterations_per_restart=500)
        accuracy = evaluate_accuracy(best_plan, target_macros)
        
        for macro in total_accuracy:
            total_accuracy[macro] += accuracy[macro]
        
    end_time = time.time()
    avg_accuracy = {macro: round(total / 100, 2) for macro, total in total_accuracy.items()}
    
    print(f"\nExecution Time: {end_time - start_time:.2f} seconds")
    print("\nAverage Accuracy (%):")
    for macro, avg_acc in avg_accuracy.items():
        print(f"{macro.capitalize()}: {avg_acc}%")
