import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
import requests
from io import BytesIO
from PIL import Image
from customtkinter import CTkImage

from config import API_KEY
from core.api import fetch_weather
from core.storage import save_weather_entry, load_tracked_history
from features.dark_theme import create_dark_theme_toggle
from features.tracking_button import create_tracking_button
from features.activity_suggester import suggest_activity
from Group3.group_feature import create_group_feature_tab

# ensure project root is on sys.path
project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def reset_result_bg(widget):
    mode = ctk.get_appearance_mode()
    widget.configure(fg_color="#1a1a1a" if mode == "Dark" else "#ffffff")

def start_app():
    # ── Theme & Window ──────────────────────────────────────
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme(str(project_root / "data" / "my_ctkcolor.json"))

    root = ctk.CTk()
    root.geometry("800x650")
    root.title("Weather App")

    # Simple close handler—avoids TclErrors from manual after_cancel
    def on_closing():
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # ── Top Display: Icon + Text ────────────────────────────
    display_frame = ctk.CTkFrame(root)
    display_frame.pack(padx=20, pady=10, fill="both", expand=True)
    display_frame.grid_columnconfigure(1, weight=1)

    image_label = ctk.CTkLabel(display_frame, text="")
    image_label.grid(row=0, column=0, padx=(10,5), pady=10, sticky="n")

    result_text = ctk.CTkTextbox(display_frame, height=300)
    result_text.configure(state="disabled")
    result_text.grid(row=0, column=1, padx=(5,10), pady=10, sticky="nsew")
    reset_result_bg(result_text)

    # ── Dark/Light Mode Toggle ───────────────────────────────
    create_dark_theme_toggle(root, on_toggle=lambda: reset_result_bg(result_text))

    # ── App Title ────────────────────────────────────────────
    ctk.CTkLabel(root, text="Weather App", font=(None, 24)).pack(pady=(5,0))

    # ── Tab View Setup ───────────────────────────────────────
    tab_view = ctk.CTkTabview(root, width=760, height=320)
    tab_view.pack(padx=20, pady=(10,0), fill="both", expand=False)

    tab_view.add("Main")
    tab_view.add("City Tracker")
    tab_view.add("Group 3")

    tab_main    = tab_view.tab("Main")
    tab_tracker = tab_view.tab("City Tracker")
    tab_group3  = tab_view.tab("Group 3")

    # Populate Group 3 tab (in its own module)
    create_group_feature_tab(tab_group3,result_text)

    # ── Main Tab: Fetch & Display ───────────────────────────
    frame_main = ctk.CTkFrame(tab_main)
    frame_main.pack(pady=10, padx=20, fill="x")

    entry_city = ctk.CTkEntry(frame_main, placeholder_text="City name", width=200)
    entry_city.pack(side="left", padx=(0,10))

    def on_fetch():
        city = entry_city.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city.")
            return
        try:
            data = fetch_weather(city)
        except Exception:
            messagebox.showerror("Fetch Error", "Check your spelling or network.")
            return

        save_weather_entry(data)

        # ── Display Icon ───────────────────────────────────
        icon = data.get("weather",[{}])[0].get("icon","")
        if icon:
            try:
                url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                resp = requests.get(url); resp.raise_for_status()
                img = Image.open(BytesIO(resp.content))
                ctk_img = CTkImage(img, size=(120,120))
                image_label.configure(image=ctk_img, text="")
                image_label.image = ctk_img
            except:
                pass

        # ── Display Text & Activity ─────────────────────────
        desc = data.get("weather",[{}])[0].get("description","").title()
        disp = (
            f"City: {data.get('name','')}\n"
            f"Temp: {data['main'].get('temp','N/A')}°F\n"
            f"Humidity: {data['main'].get('humidity','N/A')}%\n"
            f"Pressure: {data['main'].get('pressure','N/A')} hPa\n"
            f"{desc}"
        )
        act = suggest_activity(data.get("weather",[{}])[0].get("main",""))
        disp += f"\n\n🌟 Suggested Activity:\n{act}"

        result_text.configure(state="normal")
        result_text.delete("0.0","end")
        result_text.insert("0.0", disp)
        result_text.configure(state="disabled")

    def clear_fields():
        entry_city.delete(0,"end")
        result_text.configure(state="normal")
        result_text.delete("0.0","end")
        reset_result_bg(result_text)
        image_label.configure(image=None, text="")
        result_text.configure(state="disabled")

    ctk.CTkButton(frame_main, text="Fetch Weather", command=on_fetch)\
       .pack(side="left", padx=(0,10))
    ctk.CTkButton(frame_main, text="Clear", command=clear_fields)\
       .pack(side="left", padx=(0,10))

    # ── City Tracker Tab ────────────────────────────────────
    frame_tracker = ctk.CTkFrame(tab_tracker)
    frame_tracker.pack(pady=10, padx=20, fill="x")

    entry_tracked_city = ctk.CTkEntry(
        frame_tracker, placeholder_text="City to track", width=200
    )
    entry_tracked_city.pack(side="left", padx=(0,10))

    create_tracking_button(frame_tracker, entry_tracked_city, result_text)

    ctk.CTkButton(
        frame_tracker,
        text="Clear",
        command=lambda: (
            entry_tracked_city.delete(0, "end"),
            result_text.configure(state="normal"),
            result_text.delete("0.0", "end"),
            result_text.configure(state="disabled")
        )      
    ).pack(side="left", padx=(5,10))

    for days in (3,5,7):

     def _show_tracked(days):
        history = load_tracked_history(days)
        if not history:
            messagebox.showinfo("No Data", f"No entries for last {days} days.")
            return
        result_text.configure(state="normal")
        result_text.delete("0.0","end")
        result_text.insert("0.0", f"📊 Last {days} Tracked Entries:\n\n")
        for row in history:
            ts = row["timestamp"][:10]
            result_text.insert(
                "end",
                f"{ts} — {row['city']} — "
                f"{row['temp_F']}°F, {row['humidity']}% humidity\n"
            )
        result_text.configure(state="disabled")

    for d in (3,5,7):
        ctk.CTkButton(
            frame_tracker,
            text=f"Show Last {d} Days",
            width=140,
            command=lambda x=d: _show_tracked(x)
        ).pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    start_app()
