import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment
config_path = Path(__file__).parent / "config.yaml"

try:
    with open(config_path) as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Config file not found at {config_path}")

API_KEY = os.environ["API_KEY"]
MODEL_NAME = config["model"]["name"]


# print(API_KEY)
