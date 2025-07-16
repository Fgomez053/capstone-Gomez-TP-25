import os
import csv
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from core.api import fetch_weather
from core.storage import save_weather_entry
from features.dark_theme import create_dark_theme_toggle

#theme

theme_path = Path(__file__).parent.parent / "data" / "my_ctkcolor.json"
ctk.set_appearance_mode("System")
ctk.set_default_color_theme(str(theme_path))


#CSV path

data_dir = Path(__file__).parent.parent / "data"
csv_file = data_dir / "weather_history.csv"

def init_csv():
    os.makedirs(data_dir, exist_ok=True)
    if not csv_file.exists():
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "city", "temp_F", "humidity", "pressure", "description"
            ])

def start_app():
    # Builds the window
    root = ctk.CTk()
    root.title("Weather App")
    root.geometry("500x600")

    create_dark_theme_toggle(root)

    # the Title
    lbl_title = ctk.CTkLabel(root, text="Weather App", font=(None, 24))
    lbl_title.pack(pady=10)

    #input frame

    frame_input = ctk.CTkFrame(root)
    frame_input.pack(pady=10, padx=20, fill="x")

    entry_city = ctk.CTkEntry(frame_input, placeholder_text="City name", width=200)
    entry_city.pack(side="left", padx=(0, 10))


        # RESULTS TEXT BOX
    result_text = ctk.CTkTextbox(root, width=450, height=300)
    result_text.configure(state="disabled")
    result_text.pack(pady=10, padx=20)

        # Extra frame for future results/buttons
    results_frame = ctk.CTkFrame(root)
    results_frame.pack(pady=10, padx=20, fill="x")

    ####  FEATURE  ###


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

        name = data.get("name", "Unknown")
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

        init_csv()
        save_weather_entry(data)


    # CLEAR BUTTON
    def clear_fields():
        entry_city.delete(0, "end")
        result_text.configure(state="normal")
        result_text.delete("0.0", "end")
        result_text.configure(state="disabled")

    btn_fetch = ctk.CTkButton(frame_input, text="Fetch Weather", command=on_fetch)
    btn_fetch.pack(side="left")

    clear_button = ctk.CTkButton(frame_input, text="Clear", command=clear_fields)
    clear_button.pack(side="left", padx=(10, 0))

    root.mainloop()