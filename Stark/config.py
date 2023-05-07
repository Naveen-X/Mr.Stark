import os

from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


class Config(object):
    API_ID = int(os.environ.get("API_ID", 1))
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    IG_SESSION = os.environ.get("IG_SESSION", None)
    SPT_CLIENT = os.environ.get("SPT_CLIENT", None)
    SPT_SECRET = os.environ.get("SPT_SECRET", None)
    MONGO_DB = os.environ.get("MONGO_DB", None)
    GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", None)