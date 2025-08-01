# import customtkinter as ctk

# def create_dark_theme_toggle(parent, result_text=None, reset_fn=None):
#     """Dark/light switch. Resets result_text background if reset_fn is passed."""
#     def _toggle():
#         new_mode = "Dark" if ctk.get_appearance_mode() == "Light" else "Light"
#         ctk.set_appearance_mode(new_mode)

#         # ✅ Reset background after theme switch (if empty)
#         if result_text and reset_fn:
#             reset_fn(result_text)

#     sw = ctk.CTkSwitch(parent, text="Dark Mode", command=_toggle)
#     sw.pack(pady=10)
#     return sw




# """"This is my 'Theme-switch' feature,
#  which is my first feature.
#  This fuction will work when you call it. 
# In my case its 'fetures.dark_theme.py'
# 
# 
# it also kept resting my  'result_text'
#  background to black.which was a problem
#  when theme switched to light"""


import customtkinter as ctk

def create_dark_theme_toggle(parent):
  
    def toggle_theme():
    
        new_mode = "Dark" if ctk.get_appearance_mode() == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)
        # run your callback so it can fix widget colors
        if on_toggle:
            on_toggle()

    switch = ctk.CTkSwitch(parent, text="Dark Mode", command=toggle_theme)
    switch.pack(pady=10)
    return switch
