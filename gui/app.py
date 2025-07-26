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

def start_app():
    # Theme setup
    ctk.set_appearance_mode("System")
    theme_path = project_root / "data" / "my_ctkcolor.json"
    ctk.set_default_color_theme(str(theme_path))

    # Main window
    root = ctk.CTk()
    root.title("Weather App")
    root.geometry("800x550")

    create_dark_theme_toggle(root)

    # Title
    ctk.CTkLabel(root, text="Felix's Weather App", font=(None, 24)).pack(pady=(10, 0))

    # Shared Result Text
    # result_text = ctk.CTkTextbox(root, width=700, height=200)
    # result_text.configure(state="disabled")
    # result_text.pack(pady=10, padx=20)
    
    # #Image
    # image_label = ctk.CTkLabel(root, text="")  
    # image_label.pack(pady=(10,0))
        # --- Display Frame (holds icon & text side by side) ---   # NEW
    display_frame = ctk.CTkFrame(root)                         # NEW
    display_frame.pack(pady=10, padx=20, fill="both", expand=True)  # NEW

    # Image label (now a child of display_frame)            # NEW
    image_label = ctk.CTkLabel(display_frame, text="")        # NEW (parent changed)
    image_label.pack(side="left", padx=(0,10), pady=10)       # NEW (side="left")

    # Result textbox (also in display_frame)                # UPDATED parent & packing
    result_text = ctk.CTkTextbox(display_frame, width=500, height=300)  # UPDATED
    result_text.configure(state="disabled")
    result_text.pack(side="left", fill="both", expand=True)   # UPDATED (side & expand)


    # Tab Setup
    tab_view = ctk.CTkTabview(root, width=700, height=200)
    tab_view.pack(padx=20, fill="both", expand=True)

    tab_main = tab_view.add("Main")
    tab_tracker = tab_view.add("City Tracker")

    # --- Main Tab Content --- #
    frame_input = ctk.CTkFrame(tab_main)
    frame_input.pack(pady=10, padx=20)

    entry_city = ctk.CTkEntry(frame_input, placeholder_text="City name", width=200)
    entry_city.pack(side="left", padx=(0, 10))

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
        weather_main = data.get("weather", [{}])[0].get("main", "")
        activity = suggest_activity(weather_main)
        display += f"\n\n🌟 Suggested Activity:\n{activity}"
         # 1) Grab the icon code from the API response
        icon_code = data.get("weather", [{}])[0].get("icon", "")
        if icon_code:
            # 2) Download the icon PNG
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            resp = requests.get(url)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content))

            # 3) Wrap it in a CTkImage for CustomTkinter
            ctk_icon = CTkImage(img, size=(280, 280))

            # 4) Update the label
            image_label.configure(image=ctk_icon, text="")
            image_label.image = ctk_icon  # keep a reference

        result_text.configure(state="normal")
        result_text.delete("0.0", "end")
        result_text.insert("0.0", display)
        result_text.configure(state="disabled")

    def clear_fields():
        entry_city.delete(0, "end")
        result_text.configure(state="normal")
        result_text.delete("0.0", "end")
        result_text.configure(state="disabled")

    ctk.CTkButton(frame_input, text="Fetch Weather", command=on_fetch)\
        .pack(side="left", padx=(0, 10))
    ctk.CTkButton(frame_input, text="Clear", command=clear_fields)\
        .pack(side="left", padx=(0, 10))

    # --- City Tracker Tab Content --- #
    from features.tracking_button import create_tracking_button
    from core.storage import load_tracked_history

    frame_tracker = ctk.CTkFrame(tab_tracker)
    frame_tracker.pack(pady=10, padx=10)

    entry_tracked_city = ctk.CTkEntry(frame_tracker, placeholder_text="City to track")
    entry_tracked_city.pack(pady=(0, 10))

    create_tracking_button(frame_tracker, entry_tracked_city, result_text)

    # Day range buttons
    def create_day_range_button(parent, result_text, days):
        def on_click():
            history = load_tracked_history(days)
            if not history:
                messagebox.showinfo("No Data", f"No tracked data for last {days} days.")
                return

            result_text.configure(state="normal")
            result_text.delete("0.0", "end")
            result_text.insert("0.0", f"📊 Last {days} Tracked Entries:\n\n")
            for row in history[-days:]:
                result_text.insert("end",
                    f"{row['timestamp'][:10]} — {row['city']} — "
                    f"{row['temp_F']}°F, {row['humidity']}% humidity\n")
            result_text.configure(state="disabled")
        return ctk.CTkButton(parent, text=f"Show Last {days} Days", command=on_click)

    day_btn_frame = ctk.CTkFrame(frame_tracker)
    day_btn_frame.pack(pady=10)

    create_day_range_button(day_btn_frame, result_text, 3).pack(side="left", padx=5)
    create_day_range_button(day_btn_frame, result_text, 5).pack(side="left", padx=5)
    create_day_range_button(day_btn_frame, result_text, 7).pack(side="left", padx=5)

    root.mainloop()
