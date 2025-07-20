# from pathlib import Path
# from dotenv import load_dotenv
# import os

# # Looks for .env inside the core/ subfolder instead of beside config.py

# env_path = Path(__file__).resolve().parent / "core" / ".env"
# if not env_path.exists():
#     raise RuntimeError(f"'.env' file not found at {env_path}")

# load_dotenv(dotenv_path=env_path)
# API_KEY = os.getenv("API_KEY")
# if not API_KEY:
#     raise RuntimeError(
#         f"API_KEY not found in {env_path}. Ensure the file contains exactly 'API_KEY=your_key' with no spaces or quotes."
#     )
#####################################################################################
from pathlib import Path
from dotenv import load_dotenv
import os

# Load your API key from .env at project root
env_path = Path(__file__).resolve().parent / "core" / ".env"
if not env_path.exists():
    raise RuntimeError(f"'.env file' not found at {env_path}")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set in .env")
