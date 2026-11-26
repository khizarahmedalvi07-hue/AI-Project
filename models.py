from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    goal = db.Column(db.String(50), nullable=True)
    gym_access = db.Column(db.Boolean, default=False)
    activity_level = db.Column(db.Float, nullable=True)
    onboarding_complete = db.Column(db.Boolean, default=False)

    food_logs = db.relationship("FoodLog", backref="user", lazy=True)
    workout_logs = db.relationship("WorkoutLog", backref="user", lazy=True)
    weight_history = db.relationship("WeightHistory", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "goal": self.goal,
            "gym_access": self.gym_access,
            "activity_level": self.activity_level,
            "onboarding_complete": self.onboarding_complete
        }


class FoodLog(db.Model):
    __tablename__ = "food_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    food_name = db.Column(db.String(150), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    portion = db.Column(db.String(80), nullable=True)
    logged_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "food_name": self.food_name,
            "calories": self.calories,
            "portion": self.portion,
            "logged_at": self.logged_at.isoformat() if self.logged_at else None
        }


class WorkoutLog(db.Model):
    __tablename__ = "workout_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exercise_name = db.Column(db.String(150), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    calories_burned = db.Column(db.Float, default=0.0)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "exercise_name": self.exercise_name,
            "sets": self.sets,
            "reps": self.reps,
            "calories_burned": self.calories_burned,
            "completed": self.completed
        }


class WeightHistory(db.Model):
    __tablename__ = "weight_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    logged_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "weight_kg": self.weight_kg,
            "logged_at": self.logged_at.isoformat() if self.logged_at else None
        }