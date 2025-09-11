import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
      # Cấu hình theo môi trường
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
      # Tạo bảng nếu dùng SQLite và chưa có
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        with app.app_context():
            db.create_all()
            print("✅ Tables created automatically")
    # Security
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-key")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Config
    app.config.from_object("config")

    # Database
    db.init_app(app)

    # Register Blueprints
    from .routes import main_bp
    from .admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
