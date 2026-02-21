from flask import Flask
from flask_cors import CORS
from extensions import db, jwt, bcrypt
from routes.auth import auth
from routes.assets import assets
from routes.analytics import analytics
from models.user import User

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "Isuru@123_super_secure_jwt_secret_key_2026!"

# ✅ Extensions
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)



# CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)



# lueprints
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(assets, url_prefix="/asset")
app.register_blueprint(analytics, url_prefix="/analytics")

print(app.url_map)

with app.app_context():
    db.create_all()

    # if not User.query.filter_by(email="admin@gmail.com").first():
    #     from extensions import bcrypt
    #     admin = User(
    #         username="Admin",
    #         email="admin1@gmail.com",
    #         password=bcrypt.generate_password_hash("123456").decode("utf-8"),
    #         role="admin",
    #         wallet_address="0xcd40e5257857BCC399A9a246B277Da2D86C862e8"
    #     )
    #     db.session.add(admin)
    #     db.session.commit()
    #     print("Admin user created.")

if __name__ == "__main__":
    app.run(debug=True)

# http://127.0.0.1:5000