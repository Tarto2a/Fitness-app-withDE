import React, { useState } from 'react';
import './App.css';

function App() {
  const [userData, setUserData] = useState({
    weight: 70,
    height: 1.75,
    age: 25,
    gender: 'male',
    activity: 'moderate',
    goal: 'maintain'
  });

  const [weeklyPlan, setWeeklyPlan] = useState([]);

  const handleUserDataChange = (e) => {
    const { name, value } = e.target;
    setUserData({
      ...userData,
      [name]: name === 'gender' || name === 'activity' || name === 'goal' ? value : Number(value)
    });
  };
  
  const calculateMacros = ({ weight, height, age, gender, activity, goal }) => {
    let bmr = gender === "male"
      ? 10 * weight + 6.25 * height * 100 - 5 * age + 5
      : 10 * weight + 6.25 * height * 100 - 5 * age - 161;

    const activityLevels = {
      sedentary: 1.2,
      light: 1.375,
      moderate: 1.55,
      active: 1.725,
      very_active: 1.9
    };

    let calories = bmr * (activityLevels[activity] || 1.2);

    if (goal === "gain") calories += 300;
    else if (goal === "lose") calories -= 300;

    const protein = weight * 2;
    const fat = (calories * 0.25) / 9;
    const carbs = (calories - (protein * 4 + fat * 9)) / 4;

    return {
      calories: Math.round(calories),
      protein: Math.round(protein),
      fat: Math.round(fat),
      carbs: Math.round(carbs)
    };
  };

  const fetchPlan = () => {
    const targets = calculateMacros(userData);

    fetch(`http://127.0.0.1:8000/weekly-plan?target_calories=${targets.calories}&target_protein=${targets.protein}&target_fat=${targets.fat}&target_carbs=${targets.carbs}`)
      .then(response => response.json())
      .then(data => setWeeklyPlan(data))
      .catch(error => console.error('Error fetching meal plan:', error));
  };

  return (
    <div className="App">
      <h1>Personal Meal Plan Generator</h1>

      <div className='user-data'>
        <label>Weight (kg):</label>
        <input type="number" name="weight" value={userData.weight} onChange={handleUserDataChange} /><br />

        <label>Height (m):</label>
        <input type="number" step="0.01" name="height" value={userData.height} onChange={handleUserDataChange} /><br />

        <label>Age:</label>
        <input type="number" name="age" value={userData.age} onChange={handleUserDataChange} /><br />

        <label>Gender:</label>
        <select name="gender" value={userData.gender} onChange={handleUserDataChange}>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select><br />

        <label>Activity Level:</label>
        <select name="activity" value={userData.activity} onChange={handleUserDataChange}>
          <option value="sedentary">Sedentary</option>
          <option value="light">Light</option>
          <option value="moderate">Moderate</option>
          <option value="active">Active</option>
          <option value="very_active">Very Active</option>
        </select><br />

        <label>Goal:</label>
        <select name="goal" value={userData.goal} onChange={handleUserDataChange}>
          <option value="lose">🔥 Lose Weight</option>
          <option value="gain">💪 Gain Muscle</option>
          <option value="maintain">⚖️ Maintain Weight</option>
        </select><br />

        <button onClick={fetchPlan}>Generate Plan</button>
      </div>

      {weeklyPlan.length > 0 && (
        <div className='meal-plan'>
          <h2>Target Macros</h2>
          <p><b>Calories:</b> {calculateMacros(userData).calories} kcal</p>
          <p><b>Protein:</b> {calculateMacros(userData).protein} g</p>
          <p><b>Fat:</b> {calculateMacros(userData).fat} g</p>
          <p><b>Carbs:</b> {calculateMacros(userData).carbs} g</p>
          <hr />
          <h2>Weekly Meal Plan</h2>
          {weeklyPlan.map((day, index) => (
            <div key={index}>
              <h3>{day.day}</h3>
              <p><b>Breakfast:</b> {day.breakfast.name}</p>
              <p><b>Lunch:</b> {day.lunch.name}</p>
              <p><b>Dinner:</b> {day.dinner.name}</p>
              <p><b>Snack:</b> {day.snack.name}</p>
              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
