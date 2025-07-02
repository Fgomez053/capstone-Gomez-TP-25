import customtkinter as ctk 
import os
from tkinter import messagebox
import requests
import json
import csv
from datetime import datetime
from config import API_KEY

ctk.set_appearance_mode("system")
ctk.set_default_color_theme(blue)

data_dir = "data"
csv_file = os.path.join(data_dir, "weather_history.csv")

def init_csv():
    os.makedirs(data_dir, exist_ok=True)
    if not os.path.isfile(csv_file):
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "city", "temp_F", "humidity", "pressure", "description"
            ])

def save_weather_entry(data: dict):
    init_csv()
    timestamp = datetime.now().isoformat()
    city = data.get("name", "")
    main = data.get("main", {})
    temp = main.get("temp")
    humidity = main.get("humidity")
    pressure = main.get("pressure")
    description = data.get("weather", [{}])[0].get("description", "")
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, city, temp, humidity, pressure, description])

def fetch_weather(city: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Missing API key. Please set API_KEY in your .env file.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def on_fetch():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    try:
        data = fetch_weather(city)
        save_weather_entry(data)
        
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, json.dumps(data, indent=2))
        result_text.config(state=tk.DISABLED)
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"Error fetching data: {http_err}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Request Error", f"Network error: {err}")


root = ctk.CTk()
root.title("Weather App")
root.geometry("500x550")

# label = tk.Label(root, text="Welcome to my Weather App")
# label.pack(pady=20)

welcome_label = ctk.CTkLabel(
root,
text="Weather App",
font=("Roboto", 24)    
)
welcome_label.pack(pady=20)

frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=20, fill="x")

city_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Enter city name",
    width=200
)
city_entry.pack(side="left", padx=(0, 10))

fetch_button = ctk.CTkButton(
    frame, 
    text="Fetch Weather", 
    command=on_fetch
    )

fetch_button.pack(side="left")

result_text = ctk.CTkTextbox(
    root, 
    width=450, 
    height=300, 
    )
result_text.config(state="disabled")
result_text.pack(pady=10, padx=20)

""""-- Create tables
CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);
CREATE TABLE weather_stations (
    station_id INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL,
    location_id INTEGER NOT NULL,
    elevation REAL NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE weather_readings (
    reading_id INTEGER PRIMARY KEY,
    station_id INTEGER NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    pressure REAL NOT NULL,
    precipitation REAL NOT NULL,
    reading_date TEXT NOT NULL,
    FOREIGN KEY (station_id) REFERENCES weather_stations(station_id)
);
"""
root.mainloop()

