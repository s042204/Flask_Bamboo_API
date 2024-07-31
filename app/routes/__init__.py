from flask import Flask
from app.config import Config
from app.db import init_db

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    init_db(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.employee_routes import employee_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)

    print("Template folder:", app.template_folder)  # Add this line
    print("Static folder:", app.static_folder) 

    return app
