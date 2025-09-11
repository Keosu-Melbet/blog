from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    # Đăng ký routes
    from .routes import main_bp
    from .admin_routes import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    return app
