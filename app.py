from flask import Flask
from config import Config
from database import db
from routes import register_routes

app = Flask(__name__)
def create_app():
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  