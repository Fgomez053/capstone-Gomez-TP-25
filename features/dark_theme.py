import customtkinter as ctk

def create_dark_theme_toggle(parent):
  
    def toggle_theme():
    
        new_mode = "Dark" if ctk.get_appearance_mode() == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)

    switch = ctk.CTkSwitch(parent, text="Dark Mode", command=toggle_theme)
    switch.pack(pady=10)
    return switch
