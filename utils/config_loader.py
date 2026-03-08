import os
import json
from dotenv import load_dotenv

load_dotenv()

class ConfigLoader:
    @staticmethod
    def get_config():
        env = os.getenv("ENV", "QA").upper()
        with open("config.json") as f:
            config_data = json.load(f)
        return config_data[env]