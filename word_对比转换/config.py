import os


class BaseConfig():
    SECRET_KEY = "secret key"

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.83.145:8000/v1/chat/completions")

    OPENAI_PROXY = os.environ.get("OPENAI_PROXY", default="")

    MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", default="172.22.50.25:31088")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", default="fbKdRuYYPsu5nXew")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", default="v1uKl3ZPe8sSBpZZRQZqIncvbQrlS2sh")