from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()  # ✅ Chỉ tạo 1 lần ở đây

def create_app():
    app = Flask(__name__)

    # Cấu hình môi trường
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # Security
    app.secret_key = app.config["SECRET_KEY"]
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # ✅ Gắn app vào SQLAlchemy
    db.init_app(app)

    # ✅ Tạo bảng nếu dùng SQLite
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        with app.app_context():
            db.create_all()
            print("✅ Tables created automatically")
    # Kiểm tra app context để debug
    try:
        with app.app_context():
            db.session.execute("SELECT 1")
            print("✅ DB session is active")
    except Exception as e:
        print("❌ DB session failed:", e)


    # Đăng ký blueprint
    from .routes import main_bp
    from .admin_routes import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
