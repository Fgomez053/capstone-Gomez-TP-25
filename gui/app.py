import sys
from pathlib import Path

# Make sure core/ and features/ are importable
project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import customtkinter as ctk
from tkinter import messagebox
import requests
from io import BytesIO
from PIL import Image
from customtkinter import CTkImage

from config import API_KEY
from core.api import fetch_weather
from core.storage import save_weather_entry
from features.dark_theme import create_dark_theme_toggle
from features.history_tracker import create_history_button

def start_app():
    # Theme & color setup
    ctk.set_appearance_mode("System")
    theme_path = project_root / "data" / "my_ctkcolor.json"
    ctk.set_default_color_theme(str(theme_path))

    # Main window
    root = ctk.CTk()
    root.title("Weather App")
    root.geometry("700x400")

    # Dark mode toggle
    create_dark_theme_toggle(root)

    # Title
    ctk.CTkLabel(root, text="Weather App", font=(None,24)).pack(pady=(10,0))

    # Input row
    frame_input = ctk.CTkFrame(root)
    frame_input.pack(pady=10, padx=20, fill="x")

    entry_city = ctk.CTkEntry(frame_input, placeholder_text="City name", width=200)
    entry_city.pack(side="left", padx=(0,10))

    # Result textbox
    result_text = ctk.CTkTextbox(root, width=550, height=350)
    result_text.configure(state="disabled")
    result_text.pack(pady=10, padx=20, fill="both", expand=True)

    # Callbacks
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

        display = (
            f"City: {data.get('name','')}\n"
            f"Temp: {data['main'].get('temp','N/A')}°F\n"
            f"Humidity: {data['main'].get('humidity','N/A')}%\n"
            f"Pressure: {data['main'].get('pressure','N/A')} hPa\n"
            f"{data.get('weather',[{}])[0].get('description','').title()}"
        )
        result_text.configure(state="normal")
        result_text.delete("0.0","end")
        result_text.insert("0.0", display)
        result_text.configure(state="disabled")

    def clear_fields():
        entry_city.delete(0, "end")
        result_text.configure(state="normal")
        result_text.delete("0.0", "end")
        result_text.configure(state="disabled")

    # Buttons
    ctk.CTkButton(frame_input, text="Fetch Weather", command=on_fetch)\
        .pack(side="left", padx=(0,10))
    ctk.CTkButton(frame_input, text="Clear", command=clear_fields)\
        .pack(side="left", padx=(0,10))
    create_history_button(frame_input, entry_city, result_text)

    root.mainloop()

if __name__ == "__main__":
    start_app()
