import customtkinter as ctk
from tkinter import messagebox
from requests.exceptions import HTTPError
from core.api import fetch_last_5_days
from core.storage import load_history

def create_history_button(parent, entry_widget, result_widget):
    """
    Place a 'History' button that first tries
    the API, then falls back to CSV if unauthorized.
    """
    btn = ctk.CTkButton(
        parent,
        text="History",
        command=lambda: show_history(entry_widget, result_widget)
    )
    btn.pack(side="left", padx=(10, 0))
    return btn

def show_history(entry_widget, result_widget):
    city = entry_widget.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city first.")
        return

    # 1) First try the free Time-Machine API (last 5 days)
    try:
        days = fetch_last_5_days(city)  # may raise HTTPError 401
    except HTTPError as e:
        if e.response.status_code == 401:
            # 2) Fallback: load the last 7 saved CSV entries for this city
            messagebox.showwarning(
                "API Unauthorized",
                "Your API key cannot access historical data.\n"
                "Showing your local saved history instead."
            )
            all_rows  = load_history(7)  # last 7 CSV rows
            city_rows = [r for r in all_rows if r["city"].lower() == city.lower()]
            if not city_rows:
                messagebox.showinfo("History", f"No local history for {city.title()}.")
                return
            display_rows = city_rows[-7:]
            _render_blocks(display_rows, city, result_widget)
            return
        else:
            messagebox.showerror("Error", str(e))
            return
    except Exception as e:
        # any other error
        messagebox.showerror("Error", str(e))
        return

    # 3) If API succeeded, render those 5 days
    #  each entry from fetch_last_5_days() has keys like 'date', 'temp', etc.
    blocks = []
    for d in days:
        blocks.append({
            "date":    d["date"],
            "city":    city,
            "temp_F":  d.get("temp"),
            "humidity":d.get("humidity"),
            "pressure":d.get("pressure"),
            "description": d.get("weather",[{}])[0].get("description","")
        })
    _render_blocks(blocks, city, result_widget)

def _render_blocks(rows, city, result_widget):
    """
    Given a list of dicts with keys:
      date, city, temp_F, humidity, pressure, description
    render them in the textbox exactly like Fetch.
    """
    result_widget.configure(state="normal")
    result_widget.delete("0.0", "end")

    for r in rows:
        header = f"Date: {r.get('date', r.get('timestamp',''))}\n"
        block = (
            f"{header}"
            f"City: {r['city']}\n"
            f"Temp: {r['temp_F']}°F\n"
            f"Humidity: {r['humidity']}%\n"
            f"Pressure: {r['pressure']} hPa\n"
            f"{r['description'].title()}\n\n"
        )
        result_widget.insert("end", block)

    result_widget.configure(state="disabled")
