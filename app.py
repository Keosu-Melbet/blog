import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

# Logging
logging.basicConfig(level=logging.DEBUG)

# Base cho SQLAlchemy
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # DB config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///keosu.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    db.init_app(app)

    # Template globals
    @app.template_global()
    def get_current_year():
        return datetime.now().year

    with app.app_context():
        import models
        from models import User, Category

        db.create_all()

        # Tạo admin mặc định
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", is_admin=True)
            admin.set_password("123456")  # ⚠️ đổi khi production
            db.session.add(admin)
            db.session.commit()
            app.logger.info("Created default admin user: admin / 123456")

        # Tạo category mặc định
        default_categories = [
            {"name": "Kèo thơm", "slug": "keo-thom", "description": "Những kèo thơm hôm nay"},
            {"name": "Soi kèo", "slug": "soi-keo", "description": "Phân tích và soi kèo trận đấu"},
            {"name": "Mẹo cược", "slug": "meo-cuoc", "description": "Mẹo và kinh nghiệm cược bóng đá"},
            {"name": "Tin tức", "slug": "tin-tuc", "description": "Tin tức bóng đá mới nhất"},
            {"name": "Lịch thi đấu", "slug": "lich-thi-dau", "description": "Lịch thi đấu các giải"},
        ]
        for cat_data in default_categories:
            if not Category.query.filter_by(slug=cat_data["slug"]).first():
                category = Category(**cat_data)
                db.session.add(category)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating default categories: {e}")

        # Import routes
        import routes
        from admin_routes import admin_bp
        app.register_blueprint(admin_bp)

    return app
