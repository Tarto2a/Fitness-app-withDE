# Input data
algorithms = [
    {"name": "GA", "time": 23.04, "accuracy": {"calories": 90.93, "protein": 88.76, "fat": 92.89, "carbs": 47.59}},
    {"name": "POS", "time": 4.04, "accuracy": {"calories": 83.29, "protein": 75.42, "fat": 74.28, "carbs": 42.18}},
    {"name": "RRHC", "time": 78.58, "accuracy": {"calories": 94.39, "protein": 96.43, "fat": 96.6, "carbs": 51.93}},
    {"name": "SA", "time": 131.23, "accuracy": {"calories": 95.41, "protein": 96.96, "fat": 97.84, "carbs": 51.99}},
    {"name": "DE", "time": 3.32, "accuracy": {"calories": 89.46, "protein": 81.9, "fat": 89.02, "carbs": 46.74}},
    {"name": "LP", "time": 2.3, "accuracy": {"calories": 75, "protein": 53.1, "fat": 85.57, "carbs": 78.68}},
]

# Compute avg accuracy for each
for alg in algorithms:
    acc = alg["accuracy"]
    alg["avg_accuracy"] = round(sum(acc.values()) / 4, 2)

# Normalize
max_acc = max(alg["avg_accuracy"] for alg in algorithms)
max_time = max(alg["time"] for alg in algorithms)

# Compute final score
for alg in algorithms:
    acc_norm = alg["avg_accuracy"] / max_acc
    time_norm = 1 - (alg["time"] / max_time)
    alg["final_score"] = round(0.7 * acc_norm + 0.3 * time_norm, 4)

# Sort by final score
algorithms.sort(key=lambda x: x["final_score"], reverse=True)

# Print results
print(f"{'Algorithm':<6} | {'Time(s)':>8} | {'Avg Acc(%)':>11} | {'Final Score':>12}")
print("-" * 45)
for alg in algorithms:
    print(f"{alg['name']:<9} {alg['time']:>8.2f} {alg['avg_accuracy']:>11.2f} {alg['final_score']:>12.4f}")
