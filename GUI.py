import numpy as np
import tkinter as tk
import customtkinter as ctk
import cv2  # opencv-python
from GUI_widgets import *
from image_trimming import *
from configure_cams import *
from configure_load import *
from start_test import start_acquisition

# img_folder = "C:\Scratch\Showcase\GUI 1\Images"
# load_file = "C:\Scratch\Showcase\GUI 1\Test.xlsx"

GUI_inputs = ['', '', '', '']  # for catching exception of no inputs given
def get_GUI_inputs(textbox_labels, textbox_entries):
    global GUI_inputs
    GUI_inputs = get_input(textbox_labels, textbox_entries)  # get text box inputs from user

# Set up GUI
ctk.set_appearance_mode("dark")  # dark mode CTK appearance
ctk.set_default_color_theme("green")
GUI = ctk.CTk()  # main window

GUI.title("Specimen Testing Interface")
GUI.geometry("650x300")  # width by height in pixels

# set up visuals
frame_left = ctk.CTkFrame(GUI)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_right = ctk.CTkFrame(GUI)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

GUI_labels = [
    "Images Folder Location:",
    "Load Data File Location (.xlsx):",
    "Final Image File Location (.png):",
    "DIC Results File Location (.csv):"
]

GUI_entries, GUI_textlabels = textboxes(frame_left, GUI_labels, 0, 0)

text_input_button = ctk.CTkButton(frame_left, text="√", font=("Calibri", 20),
                                 fg_color="Green4", hover_color="dark green",
                                 height=30, width=50, command=lambda: get_GUI_inputs(GUI_labels, GUI_entries))
text_input_button.grid(row=2*len(GUI_labels)+2, column=0, sticky="w", padx=(10, 0), pady=(5, 0))


configure_cams_button = ctk.CTkButton(frame_right, text="Configure Cameras", font=("Calibri", 20),
                              fg_color="Blue3", hover_color="Blue4",
                              height=30, width=250, command=lambda: configure_cams(GUI))
configure_cams_button.pack(pady=5)

configure_load_button = ctk.CTkButton(frame_right, text="Configure Load Frame", font=("Calibri", 20),
                              fg_color="dark slate blue", hover_color="midnight blue",
                              height=30, width=250, command=lambda: configure_load(GUI, GUI_inputs))
configure_load_button.pack(pady=5)

launch_trim_button = ctk.CTkButton(frame_right, text="Launch Image Trimming", font=("Calibri", 20),
                              fg_color="DarkOrchid3", hover_color="DarkOrchid4",
                              height=30, width=250, command=lambda: image_trimming(GUI, GUI_inputs))  # launch img trim
# launch_trim_button.grid(row=0, column=10, sticky="e", padx=(0, 5))  # grid used to position ctk elements
launch_trim_button.pack(pady=5)

start_test_button = ctk.CTkButton(frame_right, text="Start Test", font=("Calibri", 20),
                              fg_color="Green4", hover_color="dark green",
                              height=30, width=250, command=lambda: start_acquisition(GUI, GUI_inputs))
start_test_button.pack(pady=5)

output_results_button = ctk.CTkButton(frame_right, text="Output Results", font=("Calibri", 20),
                              fg_color="goldenrod3", hover_color="DarkGoldenrod4",
                              height=30, width=250, command=lambda: image_trimming(GUI, GUI_inputs))
output_results_button.pack(pady=5)

GUI.mainloop()
