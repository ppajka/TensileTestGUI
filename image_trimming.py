import tkinter as tk
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os
from GUI_widgets import *
import numpy as np

# img_trim_file = "Z:\adit\SeniorDesign\GUI_Testing_Updated\TESTS\bug_testing_input\Untitled.tif"

def click(action):  # func for mouse1 click position
    global x_i, y_i
    canvas.delete("rectangle")
    x_i = int(canvas.canvasx(action.x))  # starting x pos of rect
    y_i = int(canvas.canvasy(action.y))  # starting y pos of rect
    return
def drag(action):  # func for mouse1 drag position
    global x_f, y_f
    x_f = int(canvas.canvasx(action.x))  # final x pos of rect
    y_f = int(canvas.canvasy(action.y))  # final y pos of rect
    canvas.delete("rectangle")  # delete rect for each previous mouse move
    canvas.create_rectangle(x_i, y_i, x_f, y_f, outline="blue", tags="rectangle")  # create rect
    return
def confirm_selection():  # func for confirmSelection button
    global pos
    pos = scale_factor*np.array([x_i, y_i, x_f, y_f])  # get final pos of confirmed rect
    pos = np.round(pos).astype(int)
    return
def crop_image(GUI, inputs):  # func to crop images
    x1, y1, x2, y2 = pos  # get boundaries of cropped region
    if x1 >= x2:  # switch x values if first is larger
        x1, x2 = x2, x1
    if y1 >= y2:  # switch y values if first is larger
        y1, y2 = y2, y1
    input_folder = inputs[0]
    output_folder = inputs[0]
    img_root.destroy()  # close window
    GUI.destroy()
    for img_file in os.listdir(input_folder):
        if img_file.endswith(".png"):
            img_path = os.path.join(input_folder, img_file)
            img = cv2.imread(img_path)
            img_crop = img[y1:y2, x1:x2]
            cv2.imwrite(os.path.join(output_folder, img_file), img_crop)
    return
def image_trimming(GUI, text_inputs):  # func to create image trimming window
    global img_root, canvas, inputs, scale_factor
    if (text_inputs[0] == '') or (text_inputs[2] == ''):
        print("Please enter image file input/output locations and the final image to be trimmed")
        return
    inputs = text_inputs
    img_root = tk.Toplevel(GUI)  # secondary window
    img_root.title("Image Trimming")
    img_root.config(bg="white")
    img_root.geometry("1000x900")

    confirm_button = tk.Button(img_root, text="Confirm Selection", font=("Calibri", 20),
                               bg="green", fg="white",
                               width=30, height=1, command=confirm_selection)
    crop_button = tk.Button(img_root, text="Crop Images", font=("Calibri", 20),
                               bg="blue2", fg="white",
                               width=30, height=1, command=lambda: crop_image(GUI, inputs))
    confirm_button.pack(side=tk.TOP)
    crop_button.pack(side=tk.TOP, padx=5)

    img = cv2.imread(text_inputs[2])  # get image in tk from file input
    img, scale_factor = img2window(img_root, img, 1)
    img_height = img.shape[0]
    img_width = img.shape[1]
    pil_img = Image.fromarray(img)
    tk_img = ImageTk.PhotoImage(pil_img)


    canvas = tk.Canvas(img_root, width=img_width, height=img_height, cursor="cross", bg="gray4")  # canvas interface
    canvas.pack(fill="both", expand=True)  # set up canvas area
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

    # binds for mouse actions
    canvas.bind("<Button-1>", click)
    canvas.bind("<B1-Motion>", drag)

    img_root.mainloop()
    return

