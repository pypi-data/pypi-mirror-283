import os
import sys

from dotenv import load_dotenv

env_file = sys.argv[1]
load_dotenv(env_file)


class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID"))
    LOGS_MAKER_BOT = os.getenv("LOGS_MAKER_BOT")
    MONGO_URL = os.getenv("MONGO_URL")
