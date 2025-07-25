from tkinter import messagebox
from core.api import fetch_weather
from core.storage import save_tracked_city_entry

def create_tracking_button(parent, entry_city, result_text):
    def on_track_click():
        city = entry_city.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city.")
            return
        try:
            data = fetch_weather(city)
            save_tracked_city_entry(data)
            messagebox.showinfo("Tracking Started", f"Now tracking weather for {city}.")
            
            # Optional: show a preview
            result_text.configure(state="normal")
            result_text.delete("0.0", "end")
            result_text.insert("0.0",
                f"📍 City: {data.get('name','')}\n"
                f"🌡️ Temp: {data['main'].get('temp','N/A')}°F\n"
                f"💧 Humidity: {data['main'].get('humidity','N/A')}%\n"
                f"📈 Pressure: {data['main'].get('pressure','N/A')} hPa\n"
                f"🌤️ Condition: {data.get('weather',[{}])[0].get('description','').title()}\n\n"
                f"✅ Data saved to your weather history!"
            )
            result_text.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Tracking Error", str(e))

    import customtkinter as ctk
    ctk.CTkButton(parent, text="Start Tracking City", command=on_track_click)\
        .pack(side="left", padx=(0,10))
