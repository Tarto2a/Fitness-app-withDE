import random
import json
import time

# Load meals data
def load_meals_data():
    with open(r"C:\Users\USER\OneDrive\Desktop\GA\processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json", "r") as file:
        return json.load(file)

meals_data = load_meals_data()

# --- Differential Evolution (DE) Functions ---

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

def mutate(population, target_idx, mutation_factor=0.8):
    size = len(population)
    idxs = list(range(size))
    idxs.remove(target_idx)
    a, b, c = random.sample(idxs, 3)
    target_plan = population[target_idx]
    mutant_plan = {}
    
    for key in target_plan:
        # Perform mutation
        mutant_plan[key] = random.choice([population[a][key], population[b][key], population[c][key]])

    return mutant_plan

def crossover(target_plan, mutant_plan, crossover_prob=0.7):
    trial_plan = {}
    for key in target_plan:
        if random.random() < crossover_prob:
            trial_plan[key] = mutant_plan[key]
        else:
            trial_plan[key] = target_plan[key]

    return trial_plan

def differential_evolution(target_macros, population_size=20, generations=50):
    population = []
    
    # Initialize population
    for _ in range(population_size):
        plan = {
            "breakfast": random.choice([m for m in meals_data if m["category"] == "Breakfast"]),
            "lunch": random.choice([m for m in meals_data if m["category"] == "Lunch"]),
            "dinner": random.choice([m for m in meals_data if m["category"] == "Dinner"]),
            "snack": random.choice([m for m in meals_data if m["category"] == "Snack"]),
        }
        population.append(plan)

    for _ in range(generations):
        for i in range(population_size):
            # Mutation and Crossover
            mutant_plan = mutate(population, i)
            trial_plan = crossover(population[i], mutant_plan)
            
            # Selection: Keep the better plan based on fitness
            if fitness(trial_plan, target_macros) < fitness(population[i], target_macros):
                population[i] = trial_plan

    # Find the best plan after generations
    population.sort(key=lambda plan: fitness(plan, target_macros))
    return population[0]

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
        best_plan = differential_evolution(target_macros)
        accuracy = evaluate_accuracy(best_plan, target_macros)
        
        for macro in total_accuracy:
            total_accuracy[macro] += accuracy[macro]

        # print("Best Plan (by DE):")
        # for meal_type, meal in best_plan.items():
        #     if isinstance(meal, dict):
        #         print(f"{meal_type.capitalize()}: {meal['name']} - {meal['calories']} cal")
        
    end_time = time.time()
    avg_accuracy = {macro: round(total / 100, 2) for macro, total in total_accuracy.items()}
        
    print(f"\nExecution Time: {end_time - start_time:.2f} seconds")
    print("\nAverage Accuracy (%):")
    for macro, avg_acc in avg_accuracy.items():
        print(f"{macro.capitalize()}: {avg_acc}%")
