from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import random
import json
from fastapi.middleware.cors import CORSMiddleware


def load_meals_data():
    with open(r"C:\Users\USER\OneDrive\Desktop\OT\meal-planing-app\src\data\processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json", "r") as file:
        return json.load(file)


class Meal(BaseModel):
    name: str
    category: str
    calories: float
    protein: float
    fat: float
    carbs: float


meals_data = load_meals_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fitness(plan, target):
    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for meal in plan.values():
        if isinstance(meal, dict):
            for key in totals:
                totals[key] += meal[key]

    weights = {"calories": 1.0, "protein": 1.5, "fat": 1.2, "carbs": 1.0}
    return sum(weights[k] * abs(totals[k] - target[k]) for k in target)


def mutate(vector, F):
    return [a + F * (b - c) for a, b, c in zip(*vector)]


def differential_evolution(target_macros, pop_size=20, gens=50, F=0.8, CR=0.7):
    def random_plan():
        return {
            "breakfast": random.choice([m for m in meals_data if m["category"] == "Breakfast"]),
            "lunch": random.choice([m for m in meals_data if m["category"] == "Lunch"]),
            "dinner": random.choice([m for m in meals_data if m["category"] == "Dinner"]),
            "snack": random.choice([m for m in meals_data if m["category"] == "Snack"]),
        }

    population = [random_plan() for _ in range(pop_size)]

    for _ in range(gens):
        new_population = []
        for i in range(pop_size):
            a, b, c = random.sample([ind for j, ind in enumerate(population) if j != i], 3)
            trial = {}
            for key in a:
                if random.random() < CR:
                    trial[key] = random.choice([a[key], b[key], c[key]])
                else:
                    trial[key] = population[i][key]

            new_population.append(trial if fitness(trial, target_macros) < fitness(population[i], target_macros) else population[i])

        population = new_population

    return min(population, key=lambda p: fitness(p, target_macros))


@app.get("/weekly-plan", response_model=List[dict])
def get_weekly_plan(
    target_calories: float = Query(2000),
    target_protein: float = Query(100),
    target_fat: float = Query(70),
    target_carbs: float = Query(250),
):
    target = {
        "calories": target_calories,
        "protein": target_protein,
        "fat": target_fat,
        "carbs": target_carbs
    }

    weekly_plan = []
    for day in range(7):
        best_plan = differential_evolution(target_macros=target)
        best_plan["day"] = f"Day {day + 1}"
        weekly_plan.append(best_plan)

    return weekly_plan
