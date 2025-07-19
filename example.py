import customtkinter as ctk
from tkinter import messagebox
import requests, csv
from datetime import datetime
from io import BytesIO
from pathlib import Path
# from PIL import Image
from customtkinter import CTkImage

from config import API_KEY
from core.api import fetch_weather
from core.storage import save_weather_entry
from features.dark_theme import create_dark_theme_toggle

# ─── Theme setup ─────────────────────────────────────────────────────────
ctk.set_appearance_mode("System")
theme_path = Path(__file__).parent / "data" / "my_ctkcolor.json"
ctk.set_default_color_theme(str(theme_path))

# ─── Main window ─────────────────────────────────────────────────────────
root = ctk.CTk()
root.title("⚡ weatherology ⚡")
root.geometry("600x500")

# ─── Dark Mode toggle feature ────────────────────────────────────────────
create_dark_theme_toggle(root)

# ─── Input row ───────────────────────────────────────────────────────────
frm = ctk.CTkFrame(root)
frm.pack(pady=10)
entry_city = ctk.CTkEntry(frm, placeholder_text="City name", width=200)
entry_city.pack(side="left", padx=(0,10))
fetch_btn = ctk.CTkButton(frm, text="submit")
fetch_btn.pack(side="left", padx=(0,10))
clear_btn = ctk.CTkButton(frm, text="Clear")
clear_btn.pack(side="left")

# ─── Output “weatherology” frame ────────────────────────────────────────
output = ctk.CTkFrame(root)
output.pack(pady=20)

location_lbl = ctk.CTkLabel(output, text="", font=("Helvetica", 18))
location_lbl.grid(row=0, column=0, columnspan=2, pady=(0,10))

temp_lbl = ctk.CTkLabel(output, text="", font=("Helvetica", 72, "bold"))
temp_lbl.grid(row=1, column=0, sticky="w")

icon_lbl = ctk.CTkLabel(output, text="")
icon_lbl.grid(row=1, column=1, padx=(20,0))

# ─── Callback functions ─────────────────────────────────────────────────
def on_fetch():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city.")
        return
    try:
        data = fetch_weather(city)
    except Exception as e:
        messagebox.showerror("Fetch Error", str(e))
        return

    save_weather_entry(data)

    # Location
    name    = data.get("name", "")
    country = data.get("sys", {}).get("country", "")
    location_lbl.configure(text=f"{name}, {country}")

    # Temperature in °C
    f = data["main"].get("temp", 0)
    c = round((f - 32) * 5/9)
    temp_lbl.configure(text=f"{c}°C")

    # Weather icon
    icon_id = data["weather"][0]["icon"]
    url     = f"http://openweathermap.org/img/wn/{icon_id}@4x.png"
    resp    = requests.get(url)
    img     = Image.open(BytesIO(resp.content)).resize((100, 100))
    ctk_img = CTkImage(light_image=img, dark_image=img, size=(100,100))
    icon_lbl.configure(image=ctk_img)
    icon_lbl.image = ctk_img  # prevent garbage collection

def clear_fields():
    entry_city.delete(0, "end")
    location_lbl.configure(text="")
    temp_lbl.configure(text="")
    icon_lbl.configure(image=None)
    icon_lbl.image = None

# ─── Wire up buttons & start ────────────────────────────────────────────
fetch_btn.configure(command=on_fetch)
clear_btn.configure(command=clear_fields)

root.mainloop()






######################
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
