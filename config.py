import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

DEFAULT_DB = "sqlite:///" + os.path.join(INSTANCE_DIR, "ventas.db").replace('\\','/')

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", DEFAULT_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "exports")
    REPORT_PAGE_SIZE = 50

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
