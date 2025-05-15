
# 🥗 Meal Planning Optimization with Differential Evolution

This project is a FastAPI-based backend for generating weekly meal plans optimized to match specific nutritional targets (calories, protein, fat, and carbs) using the **Differential Evolution (DE)** algorithm.

---

## 🚀 Features

- Generates a 7-day meal plan based on user-defined macronutrient goals
- Uses real-world food data from the USDA FoodData Central SR Legacy dataset
- Built with FastAPI for high performance and easy integration
- Supports CORS for frontend communication

---

## 📂 Project Structure

```
meal-planing-app/
│
├── main.py                      # FastAPI application with DE algorithm
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview and instructions
└── src/
    └── data/
        └── processed_FoodData_Central_sr_legacy_food_json_2021-10-28.json  # Nutritional dataset
```

---

## ⚙️ Installation

1. **Clone the repo**:

```bash
git clone https://github.com/yourusername/meal-planing-app.git
cd meal-planing-app
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

Start the FastAPI app using Uvicorn:

```bash
uvicorn main:app --reload
```

Once running, open your browser to:

```
http://127.0.0.1:8000/docs
```

You'll see an interactive Swagger UI where you can test the `/weekly-plan` endpoint.

---

## 📡 API Usage

### `GET /weekly-plan`

**Query Parameters:**

| Name           | Type   | Default | Description                  |
|----------------|--------|---------|------------------------------|
| `target_calories` | float  | 2000    | Target daily calorie intake   |
| `target_protein`  | float  | 100     | Target daily protein (g)     |
| `target_fat`      | float  | 70      | Target daily fat (g)         |
| `target_carbs`    | float  | 250     | Target daily carbohydrates (g)|

**Example:**
```
http://127.0.0.1:8000/weekly-plan?target_calories=1800&target_protein=90&target_fat=60&target_carbs=200
```

---

## 📊 Dataset

- Source: [USDA FoodData Central SR Legacy](https://fdc.nal.usda.gov/)
- Converted to JSON and categorized into: **Breakfast, Lunch, Dinner, Snack**

---

## 🧠 Algorithm

The optimization is powered by **Differential Evolution**, which evolves a population of meal plans across generations to minimize nutritional deviation from the target vector.

---

## 📜 License

This project is open-source under the MIT License.

---

## 📫 Contact

For questions or contributions, feel free to open an issue or contact [yourname@email.com].
