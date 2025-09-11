import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SESSION_SECRET", "dev-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "app.db")

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "app.db"))

