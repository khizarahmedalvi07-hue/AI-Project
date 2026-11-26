from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, FoodLog, WorkoutLog, WeightHistory

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        if not current_user.onboarding_complete:
            return redirect(url_for("auth.onboarding_page"))
        return redirect(url_for("auth.dashboard_page"))
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/signup", methods=["GET"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard_page"))
    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard_page"))
    return render_template("login.html")


@auth_bp.route("/onboarding", methods=["GET"])
@login_required
def onboarding_page():
    return render_template("onboarding.html")


@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    if not current_user.onboarding_complete:
        return redirect(url_for("auth.onboarding_page"))
    return render_template("dashboard.html")


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/api/auth/signup", methods=["POST"])
def api_signup():
    data = request.get_json(silent=True) or {}
    full_name = str(data.get("full_name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not full_name or not email or not password:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "Email already registered."}), 409

    user = User(full_name=full_name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session.clear()
    login_user(user)
    return jsonify({"status": "ok", "redirect": url_for("auth.onboarding_page")}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"status": "error", "message": "Invalid email or password."}), 401

    session.clear()
    login_user(user)
    target = url_for("auth.dashboard_page") if user.onboarding_complete else url_for("auth.onboarding_page")
    return jsonify({"status": "ok", "redirect": target}), 200


@auth_bp.route("/api/profile", methods=["GET", "POST"])
@login_required
def api_profile():
    if request.method == "GET":
        return jsonify({"status": "ok", "user": current_user.to_dict()}), 200

    data = request.get_json(silent=True) or {}
    try:
        current_user.age = int(data.get("age"))
        current_user.gender = str(data.get("gender"))
        current_user.height_cm = float(data.get("height_cm"))
        current_user.weight_kg = float(data.get("weight_kg"))
        current_user.goal = str(data.get("goal"))
        current_user.gym_access = bool(data.get("gym_access"))
        current_user.activity_level = float(data.get("activity_level"))
        current_user.onboarding_complete = True

        weight_entry = WeightHistory(user_id=current_user.id, weight_kg=current_user.weight_kg)
        db.session.add(weight_entry)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "user": current_user.to_dict(),
            "redirect": url_for("auth.dashboard_page")
        }), 200
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Invalid profile values provided."}), 400


@auth_bp.route("/api/logs", methods=["GET"])
@login_required
def api_logs():
    foods = FoodLog.query.filter_by(user_id=current_user.id).order_by(FoodLog.logged_at.desc()).all()
    workouts = WorkoutLog.query.filter_by(user_id=current_user.id).all()
    weights = WeightHistory.query.filter_by(user_id=current_user.id).order_by(WeightHistory.logged_at.asc()).all()

    food_list = []
    for f in foods:
        food_list.append(f.to_dict())

    workout_list = []
    for w in workouts:
        workout_list.append(w.to_dict())

    weight_list = []
    for wt in weights:
        weight_list.append(wt.to_dict())

    return jsonify({
        "status": "ok",
        "food_logs": food_list,
        "workout_logs": workout_list,
        "weight_history": weight_list
    }), 200


@auth_bp.route("/api/weight", methods=["POST"])
@login_required
def api_log_weight():
    data = request.get_json(silent=True) or {}
    try:
        new_weight = float(data.get("weight_kg"))
        if new_weight <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Enter a valid weight in kg."}), 400

    current_user.weight_kg = new_weight
    entry = WeightHistory(user_id=current_user.id, weight_kg=new_weight)
    db.session.add(entry)
    db.session.commit()

    return jsonify({"status": "ok", "entry": entry.to_dict()}), 201