from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes.auth import auth_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "nutrisync-dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrisync.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login_page"
login_manager.session_protection = "strong"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(auth_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)