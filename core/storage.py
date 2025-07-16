# import csv, os
# from datetime import datetime
# from pathlib import path

# DATA_DIR = "data"
# CSV_FILE = os.path.join(DATA_DIR, "weather_history.csv")

# def init_csv():
#     os.makedirs(DATA_DIR, exist_ok=True)
#     if not os.path.isfile(CSV_FILE):
#         with open(CSV_FILE, "w", newline="", encoding="utf-8")as f:
#             csv.writer(f).writerow(
#                 ["timestamp", "city", "temp_f", "humidity", "pressure", "description"]
#             )


# def save_weather_entry(data: dict):
#     init_csv()
#     ts = datetime.now().isoformat()
#     city = data.get("name", "")
#     m = data.get("main", {})
#     desc = data.get("weather",[{}])[0].get("description", "")
#     with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
#         csv.writer(f).writerow(
#             [ts, city, m.get("temp"), m.get("temp"), m.get("humidity"), m.get("pressure"), desc]
#         )

import csv, os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
CSV_FILE = DATA_DIR / "weather_history.csv"

def init_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "timestamp", "city", "temp_F",
                "humidity", "pressure", "description"
            ])

def save_weather_entry(data: dict):
    init_csv()
    ts   = datetime.now().isoformat()
    city = data.get("name", "")
    m    = data.get("main", {})
    desc = data.get("weather", [{}])[0].get("description", "")
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            ts,
            city,
            m.get("temp"),
            m.get("humidity"),
            m.get("pressure"),
            desc
        ])
