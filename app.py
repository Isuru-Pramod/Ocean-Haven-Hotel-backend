from flask import Flask
from routes.analytics import analytics

app = Flask(__name__)

app.register_blueprint(analytics)

if __name__ == "__main__":
    app.run(debug=True)
