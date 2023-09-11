# customtkinter Version: 0.3

import tkinter as tk
import customtkinter


save = []

#submit button method
def button_submit_action():
    print (1)
#slider methods
def get_current_value():
    print(2)
def slider_changed(event):
    print(3)

# Ein Fenster erstellen
fenster = tk.Tk()  # create CTk window like you do with the Tk window
fenster.title("TraMap")

# General styles and color scheme
bg_color = "#E5E5E5"
font_color= "#1F1F1F"
font_style= ("Tahoma",9)

# Customize fenster


fenster.geometry("1400x1000")

# Fensterobjekte erstellen

fenster.mainloop()

