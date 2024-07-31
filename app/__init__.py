from flask import Flask
from app.config import Config
from app.db import init_db
from app.routes.auth_routes import auth_bp
from app.routes.employee_routes import employee_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)

    return app
