import sys, os

from pathlib import Path
import customtkinter as ctk 
from tkinter import messagebox
import requests, json, csv
from datetime import datetime
from config import API_KEY




#fetching dark/light features
# from features.dark_theme import create_dark_theme_toggle

from core.api import fetch_weather
from core.storage import save_weather_entry

from gui.app import start_app

if __name__ == "__main__":
    start_app()

    #start of DATA SAVING
data_dir = "data"
csv_file = os.path.join(data_dir, "weather_history.csv")
current_unit = "F"
last_temp = None


# def init_csv():
#     os.makedirs(data_dir, exist_ok=True)
#     if not os.path.isfile(csv_file):
#         with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 "timestamp",
#                  "city", "temp_F", "humidity", "pressure", "description"
#             ])
# ########################def save_weather_entry(data: dict):
#     init_csv()
#     timestamp = datetime.now().isoformat()
#     city = data.get("name", "")
#     main = data.get("main", {})
#     temp = main.get("temp")
#     humidity = main.get("humidity")
#     pressure = main.get("pressure")
#     description = data.get("weather", [{}])[0].get("description", "")
#     with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow([timestamp, city, temp, humidity, pressure, description])

######################
#
#
##################################



# import customtkinter as ctk
# from tkinter import messagebox
# from core.api import fetch_weather
# from core.storage import save_weather_entry
# from features.dark_theme import create_dark_theme_toggle
# from pathlib import Path
# import requests
# from PIL import Image
# from io import BytesIO
# from customtkinter import CTkImage

# # Theme
# ctk.set_appearance_mode("System")
# theme_path = Path(__file__).parent / "data" / "my_ctkcolor.json"
# ctk.set_default_color_theme(str(theme_path))

# # Create window
# root = ctk.CTk()
# root.title("weatherology")
# root.geometry("600x500")

# # Dark/Light toggle
# create_dark_theme_toggle(root)

# # Input frame
# frm = ctk.CTkFrame(root)
# frm.pack(pady=10)
# entry_city = ctk.CTkEntry(frm, placeholder_text="City name")
# entry_city.pack(side="left", padx=(0,10))
# fetch_btn = ctk.CTkButton(frm, text="submit")
# fetch_btn.pack(side="left")

# # OUTPUT frame
# output = ctk.CTkFrame(root)
# output.pack(pady=20)
# location_lbl = ctk.CTkLabel(output, text="", font=("Helvetica",18))
# location_lbl.grid(row=0, column=0, columnspan=2, pady=(0,10))
# temp_lbl     = ctk.CTkLabel(output, text="", font=("Helvetica",72,"bold"))
# temp_lbl.grid(row=1, column=0, sticky="w")
# icon_lbl     = ctk.CTkLabel(output, text="")
# icon_lbl.grid(row=1, column=1, padx=(20,0))

# # Hook up fetch logic
# def on_fetch():
#     city = entry_city.get().strip()
#     if not city:
#         messagebox.showwarning("Input Error","Enter a city.")
#         return
#     data = fetch_weather(city)
#     save_weather_entry(data)
#     # Location
#     name    = data.get("name","")
#     country = data.get("sys",{}).get("country","")
#     location_lbl.configure(text=f"{name}, {country}")
#     # Temp in °C
#     f = data["main"]["temp"]
#     c = round((f-32)*5/9)
#     temp_lbl.configure(text=f"{c}°C")
#     # Icon
#     icon_id = data["weather"][0]["icon"]
#     url     = f"http://openweathermap.org/img/wn/{icon_id}@4x.png"
#     resp    = requests.get(url)
#     img     = Image.open(BytesIO(resp.content)).resize((100,100))
#     ctk_img = CTkImage(light_image=img, dark_image=img, size=(100,100))
#     icon_lbl.configure(image=ctk_img)
#     icon_lbl.image = ctk_img

# fetch_btn.configure(command=on_fetch)

# # Only one mainloop call:
# root.mainloop()
