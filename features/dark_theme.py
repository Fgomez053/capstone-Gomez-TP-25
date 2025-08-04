# features/dark_theme.py
import customtkinter as ctk

def create_dark_theme_toggle(parent, on_toggle=None):
 
    def _toggle():
        # flip between Light and Dark
        new_mode = "Dark" if ctk.get_appearance_mode() == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)
        # notify caller so they can reset widget colors
        if on_toggle:
            on_toggle()

    sw = ctk.CTkSwitch(parent, text="Dark Mode", command=_toggle)
    sw.pack(pady=10)
    return sw
