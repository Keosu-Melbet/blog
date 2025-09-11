class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
