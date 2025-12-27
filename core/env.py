import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root or core/
ENV_PATH = Path(__file__).parent / "SecretKeys.env"

load_dotenv(dotenv_path=ENV_PATH)

def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise RuntimeError(f"Missing env variable: {key}")
    return value
