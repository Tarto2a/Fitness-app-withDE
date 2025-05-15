import random
import json
import copy
import time

# --- Load Meals Data ---
def load_meals_data():
    with open(r"C:\Users\USER\OneDrive\Desktop\GA\processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json", "r") as file:
        return json.load(file)

meals_data = load_meals_data()

# --- Fitness Function ---
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

# --- Create Random Meal Plan ---
def random_meal_plan():
    return {
        "breakfast": random.choice([m for m in meals_data if m["category"] == "Breakfast"]),
        "lunch": random.choice([m for m in meals_data if m["category"] == "Lunch"]),
        "dinner": random.choice([m for m in meals_data if m["category"] == "Dinner"]),
        "snack": random.choice([m for m in meals_data if m["category"] == "Snack"]),
    }

# --- PSO Algorithm ---
def pso(target_macros, num_particles=20, generations=50, inertia=0.5, cognitive=1.5, social=2.0):
    particles = [random_meal_plan() for _ in range(num_particles)]
    pBest = copy.deepcopy(particles)
    pBest_scores = [fitness(p, target_macros) for p in pBest]

    gBest = min(pBest, key=lambda p: fitness(p, target_macros))
    gBest_score = fitness(gBest, target_macros)

    for _ in range(generations):
        for i, particle in enumerate(particles):
            new_particle = copy.deepcopy(particle)

            for meal_type in particle.keys():
                if random.random() < inertia:
                    # Stay the same (inertia)
                    pass
                elif random.random() < cognitive:
                    # Move toward pBest
                    new_particle[meal_type] = pBest[i][meal_type]
                elif random.random() < social:
                    # Move toward gBest
                    new_particle[meal_type] = gBest[meal_type]
                else:
                    # Random explore
                    category = particle[meal_type]["category"]
                    new_particle[meal_type] = random.choice([m for m in meals_data if m["category"] == category])

            # Evaluate new particle
            new_fitness = fitness(new_particle, target_macros)
            if new_fitness < pBest_scores[i]:
                pBest[i] = new_particle
                pBest_scores[i] = new_fitness

        # Update global best
        best_idx = pBest_scores.index(min(pBest_scores))
        if pBest_scores[best_idx] < gBest_score:
            gBest = pBest[best_idx]
            gBest_score = pBest_scores[best_idx]

    return gBest

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
        best_plan = pso(target_macros)
        accuracy = evaluate_accuracy(best_plan, target_macros)

        for macro in total_accuracy:
            total_accuracy[macro] += accuracy[macro]
            
    end_time = time.time()
    avg_accuracy = {macro: round(total / 100, 2) for macro, total in total_accuracy.items()}

    print(f"\nExecution Time: {end_time - start_time:.2f} seconds")
    print("\nAverage Accuracy (%):")
    for macro, avg_acc in avg_accuracy.items():
        print(f"{macro.capitalize()}: {avg_acc}%")
