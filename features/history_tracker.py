
# features/history_tracker.py

import customtkinter as ctk
from tkinter import messagebox

from core.storage import load_history


def create_history_button(parent):
    
    btn = ctk.CTkButton(parent, text="History", command=show_history)
    btn.pack(side="left", padx=(10, 0))
    return btn

def show_history():
    history = load_history(7)
    if not history:
        messagebox.showinfo("History", "No weather history available.")
        return

    # Pop-up window
    win = ctk.CTkToplevel()
    win.title("Weather History")

    txt = ctk.CTkTextbox(win, width=500, height=300)
    txt.pack(padx=20, pady=20)
    txt.configure(state="normal")

    # Insert each entry on its own line
    for row in history:
        line = (
            f"{row['timestamp']} — {row['city']}: "
            f"{row['temp_F']}°F, {row['humidity']}%, "
            f"{row['pressure']} hPa, {row['description']}\n"
        )
        txt.insert("end", line)

    txt.configure(state="disabled")
