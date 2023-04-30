import os

from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


class Config(object):
    API_ID = int(os.environ.get("API_ID", 1))
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    PRO_USERS = set(int(x) for x in os.environ.get("PRO_USERS", "").split())
    PRO = list(PRO_USERS)
