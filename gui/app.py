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
from features.tracking_button import create_tracking_button
from features.activity_suggester import suggest_activity


#helps keep result_text background on its own color theme
def reset_result_bg(result_text):
    """Set background color of result_text based on current theme."""
    mode = ctk.get_appearance_mode()
    if mode == "Dark":
        result_text.configure(fg_color="#1a1a1a")
    else:
        result_text.configure(fg_color="#ffffff")

# Add this helper function
def get_temp_color(temp_f):
    if temp_f < 32:
        return "#0f89e6"  # icy blue
    elif temp_f < 50:
        return "#25a3eb"  # light sky blue
    elif temp_f < 60:
        return "#87faad"  # mint green
    elif temp_f < 70:
        return "#eae142"  # soft yellow
    elif temp_f < 80:
        return "#f06e6c"  # peach
    elif temp_f < 90:
        return "#f03709"  # coral
    elif temp_f < 100:
        return "#d40606"  # red-orange
    else:
        return "#110707"  # deep red


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
            messagebox.showwarning("Input Error", "🙄Please enter a city🙄.")
            return
        try:
            data = fetch_weather(city)
        except Exception as e:
            messagebox.showerror("Fetch Error", str("😒Check your spelling🙄"))
            return

        save_weather_entry(data)

        display = (
            f"City: {data.get('name','')}\n"
            f"Temp: {data['main'].get('temp','N/A')}°F\n"
            f"Humidity: {data['main'].get('humidity','N/A')}%\n"
            f"Pressure: {data['main'].get('pressure','N/A')} hPa\n"
            f"{data.get('weather',[{}])[0].get('description','').title()}"
        )
        #activity suggester
        weather_main = data.get("weather", [{}])[0].get("main", "")
        activity = suggest_activity(weather_main)
        display += f"\n\n🌟 Suggested Activity:\n{activity}"

        temp = data["main"].get("temp")
        if temp is not None:
            color = get_temp_color(temp)
            result_text.configure(fg_color=color)


        result_text.configure(state="normal")
        result_text.delete("0.0","end")
        result_text.insert("0.0", display)
        result_text.configure(state="disabled")

    def clear_fields():
        entry_city.delete(0, "end")
        result_text.configure(state="normal")
        result_text.delete("0.0", "end")
        reset_result_bg(result_text)  # ✅ set default background for theme
        result_text.configure(state="disabled")

    # Buttons
    ctk.CTkButton(frame_input, text="Fetch Weather", command=on_fetch)\
        .pack(side="left", padx=(0,10))
    ctk.CTkButton(frame_input, text="Clear", command=clear_fields)\
        .pack(side="left", padx=(0,10))
    create_tracking_button(frame_input, entry_city, result_text)
    root.mainloop()

if __name__ == "__main__":
    start_app()
