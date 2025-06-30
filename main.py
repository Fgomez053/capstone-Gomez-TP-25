import tkinter as tk

root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

label = tk.Label(root, text="Welcome to my Weather App")
label.pack(pady=20)

root.mainloop()

