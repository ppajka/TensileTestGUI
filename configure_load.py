import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from GUI_widgets import *
import shared_vars

load_root_entries = 0
load_root_textlabels = 0
def specimen_selection(value):
    global load_root_entries, load_root_textlabels, new_load_root_labels, specimen_type
    specimen_type = value
    if load_root_entries != 0:
        for entry in load_root_entries:
            entry.destroy()
        for label in load_root_textlabels:
            label.destroy()
    if specimen_type == specimen_types[1]:
        load_root_entries, load_root_textlabels = textboxes(frame_left, load_root_labels[0:3], 2, 0)
        new_load_root_labels = load_root_labels[0:3]
    elif specimen_type == specimen_types[2]:
        load_root_entries, load_root_textlabels = textboxes(frame_left, load_root_labels[3:5], 2, 0)
        new_load_root_labels = load_root_labels[3:5]
    else:
        pass

def loading_selection(value):
    print(value)

def get_load_inputs(textbox_labels, textbox_entries):
    global rate_load
    load_root_inputs = get_input(textbox_labels, textbox_entries)
    rate_load = load_root_inputs[-1]
    shared_vars.set_load_vars(rate_load)
    if specimen_type == specimen_types[1]:
        specimen_width = load_root_inputs[0]
        specimen_height = load_root_inputs[1]
        specimen_data_excel = pd.DataFrame({'Specimen Width': [specimen_width],
                                            'Specimen Height': [specimen_height]})
        specimen_data_excel.to_excel(load_file, index=False)
    elif specimen_type == specimen_types[2]:
        specimen_diameter = load_root_inputs[0]
        specimen_data_excel = pd.DataFrame({'': [0],
                                            'Specimen Diameter': [specimen_diameter]})
        specimen_data_excel.to_excel(load_file, index=False)

def configure_load(GUI, text_inputs):
    global load_file, load_root, load_root_labels, specimen_types, specimen_labels, frame_left
    load_root = tk.Toplevel(GUI)  # secondary window
    ctk.set_appearance_mode("dark")
    load_root.title("Configure Load Frame")
    load_root.geometry("650x300")
    if (text_inputs[1] == ''):
        print("Please enter load file location")
        # return
    load_file = text_inputs[1]

    frame_left = ctk.CTkFrame(load_root)
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_right = ctk.CTkFrame(load_root)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    specimen_types = ["-", "Flat", "Cylindrical"]
    load_root_labels = ["Width:", "Depth:", "Acquisition Rate:", "Diameter:", "Acquisition Rate:"]
    loading_types = ["Tension", "Compression", "Cyclic"]

    text_input_button = ctk.CTkButton(frame_left, text="√", font=("Calibri", 20),
                                      fg_color="Green4", hover_color="dark green",
                                      height=30, width=50, command=lambda: get_load_inputs(new_load_root_labels, load_root_entries))
    text_input_button.grid(row=8, column=0, sticky="w", padx=(10, 0), pady=(5, 0))

    specimen_combo = ctk.CTkComboBox(frame_left,
                                         values=specimen_types,
                                         command=specimen_selection)
    specimen_combo.grid(row=0, column=0, sticky="w", padx=(5, 0))
    specimen_combo.set(specimen_types[0])

    loading_combo = ctk.CTkComboBox(frame_right,
                                         values=loading_types,
                                         command=loading_selection)
    loading_combo.grid(row=0, column=0, padx=(5, 0))
    loading_combo.set(loading_types[0])

    load_root.mainloop()