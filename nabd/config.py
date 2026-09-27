import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///nabd.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AWS_REGION = os.environ.get("AWS_REGION", "eu-central-1")
    S3_BUCKET = os.environ.get("S3_BUCKET", "nabd-patient-reports")
    MIXPANEL_TOKEN = os.environ.get("MIXPANEL_TOKEN", "")
    MOYASAR_SECRET_KEY = os.environ.get("MOYASAR_SECRET_KEY", "")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB uploads
