import sys, os
# so that main can be ran thru core
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.insert(0, project_root)

from pathlib import Path
import customtkinter as ctk 
from tkinter import messagebox
import requests, json, csv
from datetime import datetime
from config import API_KEY




#fetching dark/light features
from features.dark_theme import create_dark_theme_toggle

from core.api import fetch_weather
from core.storage import save_weather_entry

# ctk.set_appearance_mode("System")
# ctk.set_default_color_theme("data/my_ctkcolor.json")

theme_path = Path(__file__).parent / "data" / "my_ctkcolor.json"
ctk.set_default_color_theme(str(theme_path))

# creating a path so py can locate weather_app.configanywhere

# def main():
# ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

root.title("Weather App")
root.geometry("500x600")

    # … build your GUI …
    # root.mainloop()
# create_dark_theme_toggle(root)


lbl_title = ctk.CTkLabel(root, text="Weather App", font=(None, 24))
lbl_title.pack(pady=10)

frame_input = ctk.CTkFrame(root)
frame_input.pack(pady=10, padx=20, fill="x")

entry_city = ctk.CTkEntry(frame_input, placeholder_text="City name", width=200)
entry_city.pack(side="left", padx=(0, 10))

#result display box
result_text = ctk.CTkTextbox(
    root, 
    width=450, 
    height=300, 
    )
result_text.configure(state="disabled")
result_text.pack(pady=10, padx=20)


results_frame = ctk.CTkFrame(root)
results_frame.pack(pady=10, padx=20, fill="x")



    
data_dir = "data"
csv_file = os.path.join(data_dir, "weather_history.csv")
current_unit = "F"
last_temp = None


def init_csv():
    os.makedirs(data_dir, exist_ok=True)
    if not os.path.isfile(csv_file):
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                 "city", "temp_F", "humidity", "pressure", "description"
            ])



#try containers, and add tabs,...create file to import colors and themes, look into boilerplates for theme colors
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

# def fetch_weather(city: str) -> dict:
#     if not API_KEY:
#         raise RuntimeError("Missing API key. Please set API_KEY in your .env file.")
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

def on_fetch():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    try:
        data = fetch_weather(city)
    except Exception as e:
        messagebox.showerror("Fetch Error", str(e))
        return
    
    name = data.get("name","Unknow")
    main = data.get("main", {})
    temp = main.get("temp", "N/A")
    humidity = main.get("humidity", "N/A")
    pressure = main.get("pressure", "N/A")
    desc = data.get("weather", [{}])[0].get("description", "N/A").title()

    display = (
        f"City: {name}\n"
        f"Temperature: {temp}F\n"
        f"Condition: {desc}\n"
        f"Humidity: {humidity}%\n"
        f"Pressure: {pressure} hPa\n"
    )

    result_text.configure(state="normal")
    result_text.delete("0.0", "end")
    result_text.insert("0.0", display)
    result_text.configure(state="disabled")

    save_weather_entry(data)

# GUI BUTTON
btn_fetch = ctk.CTkButton(frame_input, text="Fetch Weather", command=on_fetch)
btn_fetch.pack(side="left")

def clear_fields():
    entry_city.delete(0, "end")
    result_text.configure(state="normal")
    result_text.delete("0.0", "end")
    result_text.configure(state="disabled")

    # GUI BUTTON
clear_button = ctk.CTkButton(
        frame_input,
        text="Clear",
        command=clear_fields
    )
# root = ctk.CTk()
# root.title("Weather App")
# root.geometry("500x600")

#creating the call

clear_button.pack(side="left", padx=(10, 0))

if __name__ == "__main__":
    
    # main()


    root.mainloop()
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
