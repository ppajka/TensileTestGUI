import tkinter as tk
import customtkinter as ctk
import cv2

def textboxes(window, textbox_labels, row_start, col_start):
    input_entries = []
    input_labels = []
    for i in range(len(textbox_labels)):  # loop to create textbox inputs
        input_label = ctk.CTkLabel(window, text=textbox_labels[i])
        # input_label.pack()
        input_label.grid(row=2*i+row_start, column=col_start, sticky="w", padx=(5, 0))
        input_entry = ctk.CTkEntry(window, height=5, width=300)
        # input_entry.pack()
        input_entry.grid(row=2*i+1+row_start, column=col_start, sticky="w", padx=(5, 0))
        input_entries.append(input_entry)
        input_labels.append(input_label)
    return input_entries, input_labels

def get_input(textbox_labels, textbox_entries):  # func to get text inputs
    inputs = []
    for i in range(len(textbox_labels)):
        entry = textbox_entries[i]
        input = entry.get()
        inputs.append(input)
    return inputs

def img2window(window, img, num_imgs):
    window.update_idletasks()
    window_width = window.winfo_width()
    # window_width = window_size[1]
    img_height = img.shape[0]
    img_width = img.shape[1]
    if img_width > ((1/num_imgs)*window_width):
        scaling = ((1/num_imgs)*window_width) / img_width
        aspect_ratio = img_width / img_height
        new_img_width = round((1/num_imgs)*window_width)
        new_img_height = round(new_img_width / aspect_ratio)
        # new_img_width = round(scaling*img_width)
        # new_img_height = round(scaling * img_height)
        img = cv2.resize(img, (new_img_width, new_img_height), interpolation=cv2.INTER_NEAREST)
        # img = img.resize((new_img_width, new_img_height), Image.LANCZOS)
        # img = img.subsample(img_width // new_img_width, img_height // new_img_height)
        scaled_img_height = img.shape[0]
        scaled_img_width = img.shape[1]
        scale_factor = img_width / scaled_img_width
    else:
        scale_factor = 1
    return img, scale_factor
