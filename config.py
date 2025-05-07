import os

class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Flask CRUD App")

    # Ensure these are explicitly set in the runtime environment
    JWT_SECRET = os.environ["JWT_SECRET"]
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OTLP_ENDPOINT = os.environ["OTLP_ENDPOINT"]
