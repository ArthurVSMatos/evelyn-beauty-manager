import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'evelyn_dev.db'}",
    )

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    APP_NAME = "Evelyn Beauty"

    @staticmethod
    def validate_production_config():
        required_vars = {
            "SECRET_KEY": Config.SECRET_KEY,
            "ADMIN_USERNAME": Config.ADMIN_USERNAME,
            "ADMIN_PASSWORD": Config.ADMIN_PASSWORD,
        }

        missing_vars = [key for key, value in required_vars.items() if not value]

        if os.getenv("FLASK_ENV") == "production" and missing_vars:
            raise RuntimeError(
                f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing_vars)}"
            )