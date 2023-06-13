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
    WSA = os.environ.get("WSA", None)
    ARQ_API = os.environ.get("ARQ_API", None)
    LEXICA_ART_1 = os.environ.get("LEXICA_ART_1", None)
    LEXICA_ART_2 = os.environ.get("LEXICA_ART_2", None)
    LEXICA_ART_3 = os.environ.get("LEXICA_ART_3", None)
    LEXICA_ART_4 = os.environ.get("LEXICA_ART_4", None)
    LEXICA_ART_5 = os.environ.get("LEXICA_ART_5", None)
    LEXICA_ART_6 = os.environ.get("LEXICA_ART_6, None)
    LEXICA_ART_7 = os.environ.get("LEXICA_ART_7, None)
    LEXICA_ART_8 = os.environ.get("LEXICA_ART_8", None)
    LEXICA_ART_9 = os.environ.get("LEXICA_ART_9", None)
    LEXICA_ART_10 = os.environ.get("LEXICA_ART_10", None)