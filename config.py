import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def _database_uri():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Render and some platforms expose postgres:// URLs.
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    default_sqlite = BASE_DIR / "instance" / "idead.db"
    return f"sqlite:///{default_sqlite}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "idead_secret_key")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REPORT_THRESHOLD = int(os.environ.get("REPORT_THRESHOLD", "8"))

    BURY_RATE_LIMIT = int(os.environ.get("BURY_RATE_LIMIT", "3"))
    BURY_RATE_PERIOD = int(os.environ.get("BURY_RATE_PERIOD", "60"))
    ACTION_RATE_LIMIT = int(os.environ.get("ACTION_RATE_LIMIT", "5"))
    ACTION_RATE_PERIOD = int(os.environ.get("ACTION_RATE_PERIOD", "60"))
    VIEW_RATE_LIMIT = int(os.environ.get("VIEW_RATE_LIMIT", "30"))
    VIEW_RATE_PERIOD = int(os.environ.get("VIEW_RATE_PERIOD", "60"))

    CAPTCHA_ENABLED = os.environ.get("CAPTCHA_ENABLED", "false").lower() == "true"
