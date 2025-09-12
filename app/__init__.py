import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from .extensions import db  # ✅ Import từ extensions

def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    app.secret_key = app.config["SECRET_KEY"]
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    db.init_app(app)  # ✅ Gắn app vào SQLAlchemy

    with app.app_context():
        from .models import Article  # ✅ Import sau khi init_app
        db.create_all()
        print("✅ Tables created")

    from .routes import main_bp
    from .admin_routes import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    from datetime import datetime

def get_current_year():
    return datetime.now().year

app.jinja_env.globals["get_current_year"] = get_current_year

    return app
