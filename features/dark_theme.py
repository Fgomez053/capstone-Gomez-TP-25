import customtkinter as ctk

def create_dark_theme_toggle(parent):
    """Adds a Dark/Light mode switch."""
    def _toggle():
        new = "Dark" if ctk.get_appearance_mode()=="Light" else "Light"
        ctk.set_appearance_mode(new)
    sw = ctk.CTkSwitch(parent, text="Dark Mode", command=_toggle)
    sw.pack(pady=10)
    return sw



# """"This is my 'Theme-switch' feature, which is my first feature.
#  This fuction will work when you call it. 
# In my case its 'fetures.dark_theme.py'"""