import os
from dotenv import load_dotenv

load_dotenv()
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
    WSA = os.environ.get("WSA", None)
    ARQ_API = os.environ.get("ARQ_API", None)
    VSN_CRAFT = os.environ.get("VSN_CRAFT", None)
    CHROME_BIN = os.environ.get("CHROME_BIN",  "/usr/bin/google-chrome-stable")
    GOOGLE_AI_STUDIO_KEY = os.environ.get("GOOGLE_AI_STUDIO_KEY", None)