from flask import Flask
from flask_cors import CORS
from routes.analytics import analytics

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(analytics)

if __name__ == "__main__":
    app.run(debug=True)
