# NutriSync — AI-Powered Pakistani Calorie & Fitness Tracker

NutriSync is a local full-stack Flask web application combining user authentication, biometric onboarding, calorie and workout tracking, ML-based Pakistani meal and exercise recommendations, food-image recognition, and weight-progress timeline prediction.

---

## Getting Started (How to Run Locally)

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone [https://github.com/khizarahmedalvi07-hue/AI-Project.git](https://github.com/khizarahmedalvi07-hue/AI-Project.git)
cd AI-Project
git checkout khizar-foundation
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell / CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Application
```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`. On the first run, Flask-SQLAlchemy automatically creates the local SQLite database at `instance/nutrisync.db` with all four tables initialized.

### 5. Verify Setup
1. Open `http://127.0.0.1:5000` in your browser.
2. Create an account on `/signup` and complete the `/onboarding` form.
3. Confirm you land on `/dashboard` and visit `http://127.0.0.1:5000/api/profile` to see your saved JSON profile.

---

## Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
- **Database:** Local SQLite (`sqlite:///nutrisync.db`)
- **Frontend:** HTML, CSS (Jinja2 templates), Vanilla JavaScript (`fetch` API)
- **Architecture:** Hybrid server-rendered templates + JSON REST APIs organized with Flask Blueprints

---

## Project Structure

```text
nutrisync/
├── app.py
├── models.py
├── requirements.txt
├── .gitignore
├── README.md
├── instance/
│   └── nutrisync.db
├── routes/
│   └── auth.py
├── static/
│   └── js/
│       ├── auth.js
│       └── dashboard.js
└── templates/
    ├── base.html
    ├── signup.html
    ├── login.html
    ├── onboarding.html
    └── dashboard.html
```

- `app.py` — Initializes Flask, SQLite, `LoginManager`, creates tables, and registers Blueprints.
- `models.py` — Defines `User`, `FoodLog`, `WorkoutLog`, and `WeightHistory` SQLAlchemy models with `.to_dict()` JSON serializers.
- `routes/auth.py` — Portion 1 Blueprint serving HTML pages and authentication, profile, log, and weight REST endpoints.
- `static/js/auth.js` — Handles JSON `fetch` submissions for sign-up, login, and onboarding forms.
- `static/js/dashboard.js` — Loads profile, logs, calorie stats, recommendations, and timeline predictions asynchronously and handles weight, steps, and food photo forms.
- `templates/` — Jinja2 HTML templates extending `base.html`.

---

## Database Schema (`instance/nutrisync.db`)

### `users` (`User`)
| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `email` | String(120) | Unique, Not Null (lowercased) |
| `password_hash` | String(256) | Werkzeug salted hash |
| `full_name` | String(100) | Not Null |
| `age` | Integer | Nullable |
| `gender` | String(20) | `"male"` or `"female"` |
| `height_cm` | Float | Height in cm |
| `weight_kg` | Float | Latest weight in kg |
| `goal` | String(50) | `"weight_loss"`, `"maintenance"`, or `"muscle_gain"` |
| `gym_access` | Boolean | `True` (gym) or `False` (home/bodyweight) |
| `activity_level` | Float | Harris-Benedict multiplier (`1.2`, `1.375`, `1.55`, `1.725`) |
| `onboarding_complete` | Boolean | Default `False` |

### `food_logs` (`FoodLog`)
`id`, `user_id` (FK -> `users.id`), `food_name`, `calories`, `portion`, `logged_at` (UTC DateTime)

### `workout_logs` (`WorkoutLog`)
`id`, `user_id` (FK -> `users.id`), `exercise_name`, `sets`, `reps`, `calories_burned`, `completed`

### `weight_history` (`WeightHistory`)
`id`, `user_id` (FK -> `users.id`), `weight_kg`, `logged_at` (UTC DateTime)

### Stored Value Reference
- **`activity_level`:** `1.2` (Sedentary), `1.375` (Lightly Active), `1.55` (Moderately Active), `1.725` (Very Active) — ready for direct `BMR * user.activity_level` calculation.
- **`goal`:** `"weight_loss"` (`-500 kcal`), `"maintenance"` (`0 kcal`), `"muscle_gain"` (`+300 kcal`).
- **`gym_access`:** `True` maps to `1` in ML datasets; `False` maps to `0`.

---

## Implemented REST API Endpoints (Portion 1 — Khizar)

| Endpoint | Method | Auth | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/signup` | `POST` | No | `{"full_name", "email", "password"}` | `201`: `{"status": "ok", "redirect": "/onboarding"}` |
| `/api/auth/login` | `POST` | No | `{"email", "password"}` | `200`: `{"status": "ok", "redirect": "/dashboard"}` |
| `/api/profile` | `GET` | Yes | None | `200`: `{"status": "ok", "user": {...}}` |
| `/api/profile` | `POST` | Yes | `{"age", "gender", "height_cm", "weight_kg", "goal", "gym_access", "activity_level"}` | `200`: `{"status": "ok", "user": {...}, "redirect": "/dashboard"}` |
| `/api/logs` | `GET` | Yes | None | `200`: `{"status": "ok", "food_logs": [...], "workout_logs": [...], "weight_history": [...]}` |
| `/api/weight` | `POST` | Yes | `{"weight_kg": 64.5}` | `201`: `{"status": "ok", "entry": {...}}` |

---

## Teammate Integration Contract (Portions 2, 3 & 4)

Each teammate should create their own Flask Blueprint inside `routes/`, import models from `models.py`, and register the Blueprint in `app.py`. The frontend (`static/js/dashboard.js`) is already wired to consume these exact endpoints:

| Portion & Owner | Blueprint File | Endpoint | Input | Expected JSON Output |
| :--- | :--- | :--- | :--- | :--- |
| **Portion 2 — Rayyan** | `routes/tracking.py` | `GET /api/dashboard` | None | `{"target": 2100, "eaten": 650, "burned": 300, "remaining": 1750}` |
| **Portion 2 — Rayyan** | `routes/tracking.py` | `POST /api/steps` | `{"steps": 5000}` | `{"calories_burned": 162.5, "remaining": 1912.5}` |
| **Portion 2 — Rayyan** | `routes/tracking.py` | `POST /api/workouts/complete` | `{"exercise_name": "Squats", "duration_minutes": 20}` | `{"calories_burned": 108.3, "remaining": 2020.8}` |
| **Portion 3 — Manuchahr** | `routes/ml_recommend.py` | `GET /api/recommendations` | None | `{"exercises": [...], "meals": {"breakfast": "...", "lunch": "...", "dinner": "..."}}` |
| **Portion 4 — Umer** | `routes/vision_ai.py` | `POST /api/food/log` | `multipart/form-data` (`top_image`, `side_image`) | `{"food_name": "Chicken Biryani", "calories": 480, "portion": "1 plate"}` |
| **Portion 4 — Umer** | `routes/vision_ai.py` | `GET /api/predict/timeline` | None | `{"weeks_to_goal": 8, "message": "At your current pace, you may reach your goal in approximately 8 weeks."}` |

### Registering a New Blueprint in `app.py`
```python
from routes.tracking import tracking_bp
app.register_blueprint(tracking_bp)
```

---

## Git Branching Workflow

Do not push directly to `main`. Create a feature branch from `khizar-foundation` for your portion:

```bash
git checkout -b rayyan-tracking
git add .
git commit -m "Add calorie calculation and step tracking endpoints"
git push -u origin rayyan-tracking
```

Suggested branch names:
- `khizar-foundation` — Portion 1 (Database, Auth, Base UI & REST APIs)
- `rayyan-tracking` — Portion 2 (BMR/TDEE, Steps & Workout Tracking)
- `manuchahr-ml` — Portion 3 (KNN Exercises & Random Forest Meal Plans)
- `umer-vision` — Portion 4 (YOLOv8, Gemini/Groq & Linear Regression)