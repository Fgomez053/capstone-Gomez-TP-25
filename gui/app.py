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

    # output = ctk.CTkFrame(root)
    # output.pack(pady=20)

    # location_lbl = ctk.CTkLabel(output, text="", font=("Helvetica", 18))
    # location_lbl.grid(row=0, column=0, columnspan=2, pady=(0,10))


    ####  FEATURE  ###


    def on_fetch():
        city = entry_city.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "😒You forgot to enter a city name🙄.")
            return
        try:
            data = fetch_weather(city)
        except Exception as e:
            messagebox.showerror("Fetch Error", str("Check your spelling😒"))
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

        # init_csv()
        save_weather_entry(data)


    # CLEAR BUTTON function
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


# #######################################################

# import customtkinter as ctk
# from tkinter import messagebox
# import requests
# from io import BytesIO
# from pathlib import Path
# from PIL import Image
# from customtkinter import CTkImage

# from config import API_KEY
# from core.api import fetch_weather
# from core.storage import save_weather_entry
# from features.dark_theme import create_dark_theme_toggle

# def start_app():
#     # ─── Theme setup ─────────────────────────────────────────────────────
#     ctk.set_appearance_mode("System")
#     theme_path = Path(__file__).parent.parent / "data" / "my_ctkcolor.json"
#     ctk.set_default_color_theme(str(theme_path))

#     # ─── Main window ─────────────────────────────────────────────────────
#     root = ctk.CTk()
#     root.title("Weather App")       # your original title
#     root.geometry("600x500")

#     # ─── Dark Mode toggle ─────────────────────────────────────────────────
#     create_dark_theme_toggle(root)

#     # ─── Input row ────────────────────────────────────────────────────────
#     frame_input = ctk.CTkFrame(root)
#     frame_input.pack(pady=10, padx=20, fill="x")

#     entry_city = ctk.CTkEntry(
#         frame_input,
#         placeholder_text="City name",
#         width=200
#     )
#     entry_city.pack(side="left", padx=(0, 10))

#     fetch_btn = ctk.CTkButton(
#         frame_input,
#         text="submit"                # your original button text
#     )
#     fetch_btn.pack(side="left", padx=(0, 10))

#     clear_btn = ctk.CTkButton(
#         frame_input,
#         text="Clear"                 # your original button text
#     )
#     clear_btn.pack(side="left")

#     # ─── WEATHEROLOGY OUTPUT FRAME ────────────────────────────────────────
#     output = ctk.CTkFrame(root)
#     output.pack(pady=20)

#     location_lbl = ctk.CTkLabel(
#         output,
#         text="",
#         font=("Helvetica", 18)
#     )
#     location_lbl.grid(row=0, column=0, columnspan=2, pady=(0,10))

#     temp_lbl = ctk.CTkLabel(
#         output,
#         text="",
#         font=("Helvetica", 72, "bold")
#     )
#     temp_lbl.grid(row=1, column=0, sticky="w")

#     icon_lbl = ctk.CTkLabel(
#         output,
#         text=""
#     )
#     icon_lbl.grid(row=1, column=1, padx=(20,0))

#     # ─── Callback functions ───────────────────────────────────────────────
#     def on_fetch():
#         city = entry_city.get().strip()
#         if not city:
#             messagebox.showwarning("Input Error", "Please enter a city.")
#             return
#         try:
#             data = fetch_weather(city)
#         except Exception as e:
#             messagebox.showerror("Fetch Error", str(e))
#             return

#         save_weather_entry(data)

#         # Update location
#         name    = data.get("name", "")
#         country = data.get("sys", {}).get("country", "")
#         location_lbl.configure(text=f"{name}, {country}")

#         # Update temperature in °C
#         f = data["main"].get("temp", 0)
#         c = round((f - 32) * 5/9)
#         temp_lbl.configure(text=f"{c}°C")

#         # Fetch & display weather icon
#         icon_id = data["weather"][0]["icon"]
#         url     = f"http://openweathermap.org/img/wn/{icon_id}@4x.png"
#         resp    = requests.get(url)
#         img     = Image.open(BytesIO(resp.content)).resize((100,100))
#         ctk_img = CTkImage(light_image=img, dark_image=img, size=(100,100))
#         icon_lbl.configure(image=ctk_img)
#         icon_lbl.image = ctk_img  # keep reference

#     def clear_fields():
#         entry_city.delete(0, "end")
#         location_lbl.configure(text="")
#         temp_lbl.configure(text="")
#         icon_lbl.configure(image=None)
#         icon_lbl.image = None

#     # ─── Wire up buttons & start ─────────────────────────────────────────
#     fetch_btn.configure(command=on_fetch)
#     clear_btn.configure(command=clear_fields)

#     root.mainloop()
