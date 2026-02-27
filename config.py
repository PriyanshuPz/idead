import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "idead_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///idead.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REPORT_THRESHOLD = 8

    BURY_RATE_LIMIT = int(os.environ.get("BURY_RATE_LIMIT", "3"))
    BURY_RATE_PERIOD = int(os.environ.get("BURY_RATE_PERIOD", "60"))
    ACTION_RATE_LIMIT = int(os.environ.get("ACTION_RATE_LIMIT", "5"))
    ACTION_RATE_PERIOD = int(os.environ.get("ACTION_RATE_PERIOD", "60"))

    CAPTCHA_ENABLED = os.environ.get("CAPTCHA_ENABLED", "false").lower() == "true"
