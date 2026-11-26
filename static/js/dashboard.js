document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.getElementById("alert-box");

    function showAlert(message) {
        if (!alertBox) return;
        alertBox.textContent = message;
        alertBox.style.display = "block";
    }

    async function loadProfile() {
        const res = await fetch("/api/profile");
        if (!res.ok) return;
        const data = await res.json();
        const user = data.user;

        document.getElementById("profile-goal").textContent = user.goal.replace("_", " ").toUpperCase();
        document.getElementById("profile-gym").textContent = user.gym_access ? "Gym Access" : "Home / Bodyweight";
        document.getElementById("current-weight-display").textContent = user.weight_kg + " kg";
    }

    async function loadCalorieSummary() {
        try {
            const res = await fetch("/api/dashboard");
            if (!res.ok) return;
            const data = await res.json();

            document.getElementById("target-kcal").textContent = Math.round(data.target) + " kcal";
            document.getElementById("eaten-kcal").textContent = Math.round(data.eaten) + " kcal";
            document.getElementById("burned-kcal").textContent = Math.round(data.burned) + " kcal";
            document.getElementById("remaining-kcal").textContent = Math.round(data.remaining) + " kcal";
        } catch (err) {
            console.log("Waiting for Rayyan's /api/dashboard endpoint.");
        }
    }

    async function loadLogs() {
        const res = await fetch("/api/logs");
        if (!res.ok) return;
        const data = await res.json();

        const foodListEl = document.getElementById("food-log-list");
        foodListEl.innerHTML = "";
        if (data.food_logs.length === 0) {
            foodListEl.innerHTML = "<li class='empty-item'>No meals logged yet.</li>";
        } else {
            for (let i = 0; i < data.food_logs.length; i++) {
                const item = data.food_logs[i];
                const li = document.createElement("li");
                li.className = "log-item";
                li.innerHTML = "<span>" + item.food_name + " (" + (item.portion || "1 serving") + ")</span><strong>" + Math.round(item.calories) + " kcal</strong>";
                foodListEl.appendChild(li);
            }
        }

        const workoutListEl = document.getElementById("workout-log-list");
        workoutListEl.innerHTML = "";
        if (data.workout_logs.length === 0) {
            workoutListEl.innerHTML = "<li class='empty-item'>No workouts logged yet.</li>";
        } else {
            for (let i = 0; i < data.workout_logs.length; i++) {
                const w = data.workout_logs[i];
                const li = document.createElement("li");
                li.className = "log-item";
                const statusText = w.completed ? "Done" : "Pending";
                li.innerHTML = "<span>" + w.exercise_name + " (" + statusText + ")</span><strong>" + Math.round(w.calories_burned) + " kcal</strong>";
                workoutListEl.appendChild(li);
            }
        }

        const weightListEl = document.getElementById("weight-history-list");
        weightListEl.innerHTML = "";
        for (let i = 0; i < data.weight_history.length; i++) {
            const wt = data.weight_history[i];
            const li = document.createElement("li");
            li.className = "log-item";
            const dateStr = wt.logged_at ? wt.logged_at.split("T")[0] : "";
            li.innerHTML = "<span>" + dateStr + "</span><strong>" + wt.weight_kg + " kg</strong>";
            weightListEl.appendChild(li);
        }
    }

    async function loadRecommendations() {
        try {
            const res = await fetch("/api/recommendations");
            if (!res.ok) return;
            const data = await res.json();

            const mealBox = document.getElementById("meal-plan-box");
            if (data.meals) {
                mealBox.innerHTML =
                    "<p><strong>Breakfast:</strong> " + data.meals.breakfast + "</p>" +
                    "<p><strong>Lunch:</strong> " + data.meals.lunch + "</p>" +
                    "<p><strong>Dinner:</strong> " + data.meals.dinner + "</p>";
            }
        } catch (err) {
            console.log("Waiting for Manuchahr's /api/recommendations endpoint.");
        }
    }

    async function loadPrediction() {
        try {
            const res = await fetch("/api/predict/timeline");
            if (!res.ok) return;
            const data = await res.json();
            if (data.message) {
                document.getElementById("prediction-box").textContent = data.message;
            }
        } catch (err) {
            console.log("Waiting for Umer's /api/predict/timeline endpoint.");
        }
    }

    const weightForm = document.getElementById("weight-form");
    if (weightForm) {
        weightForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const weightVal = parseFloat(document.getElementById("new-weight-input").value);
            const res = await fetch("/api/weight", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ weight_kg: weightVal })
            });
            const data = await res.json();
            if (res.ok) {
                document.getElementById("new-weight-input").value = "";
                loadProfile();
                loadLogs();
                loadPrediction();
            } else {
                showAlert(data.message || "Could not log weight.");
            }
        });
    }

    const foodUploadForm = document.getElementById("food-upload-form");
    if (foodUploadForm) {
        foodUploadForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const statusEl = document.getElementById("food-upload-status");
            const formData = new FormData(foodUploadForm);
            statusEl.textContent = "Analyzing food images...";

            try {
                const res = await fetch("/api/food/log", {
                    method: "POST",
                    body: formData
                });
                const data = await res.json();
                if (res.ok) {
                    statusEl.textContent = "Logged: " + data.food_name + " (" + data.calories + " kcal)";
                    foodUploadForm.reset();
                    loadLogs();
                    loadCalorieSummary();
                } else {
                    statusEl.textContent = data.message || "Recognition failed.";
                }
            } catch (err) {
                statusEl.textContent = "Waiting for Umer's /api/food/log endpoint.";
            }
        });
    }

    const stepsForm = document.getElementById("steps-form");
    if (stepsForm) {
        stepsForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const stepsVal = parseInt(document.getElementById("steps-input").value, 10);
            try {
                const res = await fetch("/api/steps", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ steps: stepsVal })
                });
                if (res.ok) {
                    document.getElementById("steps-input").value = "";
                    loadCalorieSummary();
                }
            } catch (err) {
                showAlert("Waiting for Rayyan's /api/steps endpoint.");
            }
        });
    }

    loadProfile();
    loadCalorieSummary();
    loadLogs();
    loadRecommendations();
    loadPrediction();
});