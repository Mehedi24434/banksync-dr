import os
from dotenv import load_dotenv

load_dotenv()

CHROME_PATH = os.getenv("CHROME_PATH")
PROFILE_DIR = os.getenv("PROFILE_DIR")
