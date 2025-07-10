from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent / ".env"
if not env_path.exists():
    raise RuntimeError(f"'.env' file not found at {env_path}")

load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError(
        f"API_KEY not found in {env_path}. Ensure the file contains exactly 'API_KEY=your_key' with no spaces or quotes."
    )