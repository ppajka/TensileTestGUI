import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import time
import cv2
from PIL import Image, ImageTk
from GUI_widgets import *
from collect_images import *
import shared_vars

def exposure_slider_move(value):
    exposure_entry.delete(0, tk.END)
    exposure_entry.insert(0, str(value))
    exposure_slider.set(value)

def gain_slider_move(value):
    gain_entry.delete(0, tk.END)
    gain_entry.insert(0, str(value))
    gain_slider.set(value)

def get_cam_inputs(action):
    global cam_root_inputs, exposure, gain, rate_cams
    cam_root_inputs = get_input(cam_root_labels, cam_root_entries)
    try:
        exposure = int(cam_root_inputs[0])
        gain = int(cam_root_inputs[1])
        rate_cams = float(cam_root_inputs[2])

        exposure_slider.set(exposure)
        gain_slider.set(gain)
        if (exposure_min <= exposure <= exposure_max) and (gain_min <= gain <= gain_max):
            cam1.Gain.SetValue(gain)
            cam2.Gain.SetValue(gain)
            cam1.ExposureTime.SetValue(exposure)
            cam2.ExposureTime.SetValue(exposure)
            cam_root.after(500, refresh_images)
        else:
            print("Please select an exposure and gain within the bounds")
        shared_vars.set_cam_vars(exposure, gain, rate_cams, cam1, cam2)
    except ValueError:
        pass

def refresh_images():
    cam1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    cam2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    get_img1, get_img2, time_cam1, time_cam2 = collect_images(cam1, cam2, exposure)
    img1 = get_img1.GetArray()
    img2 = get_img2.GetArray()
    get_img1.Release()
    get_img2.Release()
    cam1.StopGrabbing()
    cam2.StopGrabbing()

    img1, scale_factor1 = img2window(cam_root, img1, 2)
    img2, scale_factor2 = img2window(cam_root, img2, 2)

    img1_pil = Image.fromarray(img1)
    img2_pil = Image.fromarray(img2)

    img1_tk = ImageTk.PhotoImage(img1_pil)
    img2_tk = ImageTk.PhotoImage(img2_pil)

    canvas1.itemconfig(canvas1_id, image=img1_tk)
    canvas2.itemconfig(canvas2_id, image=img2_tk)
    canvas1.imgref = img1_tk
    canvas2.imgref = img2_tk

def configure_cams(GUI):
    global cam_root, exposure_entry, gain_entry, \
        exposure_slider, gain_slider,cam1, cam2, \
        cam_root_labels, cam_root_entries,\
        canvas1, canvas2, canvas1_id, canvas2_id, \
        exposure_min, exposure_max, gain_min, gain_max

    # connect cams
    tlf = pylon.TlFactory.GetInstance()
    cameras = tlf.EnumerateDevices()

    cam1 = pylon.InstantCamera(tlf.CreateDevice(cameras[0]))
    cam2 = pylon.InstantCamera(tlf.CreateDevice(cameras[1]))

    cam1.Open()
    cam2.Open()
    cam1.TriggerSelector.SetValue("FrameStart")
    cam1.TriggerMode.SetValue("On")
    cam1.TriggerSource.SetValue("Software")
    cam2.TriggerSelector.SetValue("FrameStart")
    cam2.TriggerMode.SetValue("On")
    cam2.TriggerSource.SetValue("Software")

    exposure_min = cam1.ExposureTime.Min
    exposure_max = 100000
    gain_min = 1
    gain_max = 20

    cam1.Gain.SetValue(gain_min)
    cam2.Gain.SetValue(gain_min)

    cam1.ExposureTime.SetValue(exposure_min)
    cam2.ExposureTime.SetValue(exposure_min)

    cam_root = tk.Toplevel(GUI)  # secondary window
    ctk.set_appearance_mode("dark")
    cam_root.title("Configure Cameras")
    cam_root.geometry("1000x500")

    frame_top = ctk.CTkFrame(cam_root)
    frame_top.pack(side=tk.TOP, fill="x")
    frame_left = ctk.CTkFrame(cam_root)
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame_right = ctk.CTkFrame(cam_root)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    cam_root_labels = [
        "Exposure:",
        "Gain:",
        "Acquisition Rate:"
    ]

    cam_root_entries, cam_root_textlabels = textboxes(frame_top, cam_root_labels, 0, 0)
    exposure_entry = cam_root_entries[0]
    gain_entry = cam_root_entries[1]
    rate_cams_entry = cam_root_entries[2]

    exposure_entry.insert(0, str(exposure_min))
    gain_entry.insert(0, str(gain_min))
    rate_cams_entry.insert(0, str(1))

    exposure_entry.bind("<Return>", get_cam_inputs)
    gain_entry.bind("<Return>", get_cam_inputs)
    rate_cams_entry.bind("<Return>", get_cam_inputs)

    exposure_slider = tk.Scale(frame_top, from_=exposure_min, to=exposure_max, length=200,
                               orient=tk.HORIZONTAL, bg="gray10", fg="gray90",
                               command=exposure_slider_move)
    exposure_slider.grid(row=1, column=1)

    gain_slider = tk.Scale(frame_top, from_=gain_min, to=gain_max, length=200,
                           orient=tk.HORIZONTAL, bg="gray10", fg="gray90",
                           command=gain_slider_move)
    gain_slider.grid(row=3, column=1)

    exposure_slider.bind("<ButtonRelease>", get_cam_inputs)
    gain_slider.bind("<ButtonRelease>", get_cam_inputs)

    cam1.StartGrabbing(pylon.GrabStrategy_OneByOne)
    cam2.StartGrabbing(pylon.GrabStrategy_OneByOne)

    get_img1, get_img2, time_cam1, time_cam2 = collect_images(cam1, cam2, exposure_min)
    img1_i = get_img1.GetArray()
    img2_i = get_img2.GetArray()

    get_img1.Release()
    get_img2.Release()

    cam1.StopGrabbing()
    cam2.StopGrabbing()

    img1_i, scale_factor1 = img2window(cam_root, img1_i, 2)
    img2_i, scale_factor2 = img2window(cam_root, img2_i, 2)

    img_height_i = img1_i.shape[0]
    img_width_i = img1_i.shape[1]
    img1_pil_i = Image.fromarray(img1_i)
    img2_pil_i = Image.fromarray(img2_i)

    img1_tk_i = ImageTk.PhotoImage(img1_pil_i)
    img2_tk_i = ImageTk.PhotoImage(img2_pil_i)

    canvas1 = tk.Canvas(frame_left, width=img_width_i, height=img_height_i, bg="gray4")  # canvas interface
    canvas1.pack(side=tk.LEFT, fill="both", expand=True)
    canvas1_id = canvas1.create_image(0, 0, anchor="nw", image=img1_tk_i)

    canvas2 = tk.Canvas(frame_right, width=img_width_i, height=img_height_i, bg="gray4")  # canvas interface
    canvas2.pack(side=tk.RIGHT, fill="both", expand=True)
    canvas2_id = canvas2.create_image(0, 0, anchor="nw", image=img2_tk_i)

    cam_root.mainloop()
    return