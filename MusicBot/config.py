from os import getenv
import os
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Mr.Stark")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "CapitalLondonRadio")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/dcfdf612e499eef0e0b1f.png")
admins = {}
API_ID = int(getenv("API_ID", "5084195"))
API_HASH = getenv("API_HASH", "d24c617a9c6775d1f5b313f693b4400e")
BOT_USERNAME = getenv("BOT_USERNAME", "@Mr_StarkBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "Stark")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "Mr_StarkBot")
PROJECT_NAME = getenv("PROJECT_NAME", "Stark v1")
SOURCE_CODE = getenv("SOURCE_CODE", "github.com/Naveen-xd2580/Mr.Stark")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "0"))
ARQ_API_KEY = getenv("ARQ_API_KEY", "KKFIAN-COGFZQ-BJSALE-HKJDHF-ARQ")
PMPERMIT = getenv("PMPERMIT", None)
LOG_GRP = getenv("LOG_GRP", "-1001491739934")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
