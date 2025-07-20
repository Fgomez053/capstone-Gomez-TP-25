# import csv, os
# from datetime import datetime
# from pathlib import Path

# DATA_DIR = Path(__file__).parent.parent / "data"
# CSV_FILE = DATA_DIR / "weather_history.csv"

# def init_csv():
#     os.makedirs(DATA_DIR, exist_ok=True)
#     if not CSV_FILE.exists():
#         with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
#             csv.writer(f).writerow([
#                 "timestamp", "city", "temp_F",
#                 "humidity", "pressure", "description"
#             ])

# def save_weather_entry(data: dict):
#     init_csv()
#     ts   = datetime.now().isoformat()
#     city = data.get("name", "")
#     m    = data.get("main", {})
#     desc = data.get("weather", [{}])[0].get("description", "")
#     with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
#         csv.writer(f).writerow([
#             ts,
#             city,
#             m.get("temp"),
#             m.get("humidity"),
#             m.get("pressure"),
#             desc
#         ])


# def load_history(n=7) -> list[dict]:
#     """
#     Return up to the last `n` entries from weather_history.csv
#     as a list of dicts with keys:
#       timestamp, city, temp_F, humidity, pressure, description
#     """
#     init_csv()
#     with open(CSV_FILE, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         rows = list(reader)
#     return rows[-n:]
##########################################################################################################

# core/storage.py

# core/storage.py

# import csv, os
# from datetime import datetime
# from pathlib import Path

# DATA_DIR = Path(__file__).parent.parent / "data"
# CSV_FILE = DATA_DIR / "weather_history.csv"

# def init_csv():
#     """Ensure the CSV and folder exist, with header row."""
#     os.makedirs(DATA_DIR, exist_ok=True)
#     if not CSV_FILE.exists():
#         with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
#             csv.writer(f).writerow([
#                 "timestamp", "city", "temp_F",
#                 "humidity", "pressure", "description"
#             ])

# def save_weather_entry(data: dict):
#     """Append one record of fetched weather to the CSV."""
#     init_csv()
#     ts   = datetime.now().isoformat()
#     city = data.get("name", "")
#     m    = data.get("main", {})
#     desc = data.get("weather", [{}])[0].get("description", "")
#     with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
#         csv.writer(f).writerow([
#             ts,
#             city,
#             m.get("temp"),
#             m.get("humidity"),
#             m.get("pressure"),
#             desc
#         ])

# def load_history(n=7) -> list[dict]:
#     """
#     Read up to the last `n` rows from the CSV
#     and return a list of dicts.
#     """
#     init_csv()
#     with open(CSV_FILE, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         rows = list(reader)
#     return rows[-n:]
#####################################################################################
import csv, os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
CSV_FILE = DATA_DIR / "weather_history.csv"

def init_csv():
    """Ensure the CSV exists with a header row."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "timestamp", "city", "temp_F",
                "humidity", "pressure", "description"
            ])

def save_weather_entry(data: dict):
    """Append the current-fetch data to the CSV."""
    init_csv()
    ts   = datetime.now().isoformat()
    city = data.get("name", "")
    m    = data.get("main", {})
    desc = data.get("weather",[{}])[0].get("description","")
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            ts,
            city,
            m.get("temp"),
            m.get("humidity"),
            m.get("pressure"),
            desc
        ])

def load_history(n=7) -> list[dict]:
    """
    Read up to the last `n` rows from the CSV
    as a list of dicts.
    """
    init_csv()
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows[-n:]
