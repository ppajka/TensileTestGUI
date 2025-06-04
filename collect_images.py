import cv2
import time
from pypylon import pylon
import numpy as np

# folder = Z:/adit/SeniorDesign/GUI Testing/IMAGES
img_folder = "Z:/adit/SeniorDesign/GUI Testing/IMAGES"

def collect_images(cam1, cam2, exposure):
    cam1.TriggerSoftware.Execute()
    cam2.TriggerSoftware.Execute()
    time.sleep((exposure+30000) / 1e6)

    cam1.TriggerSoftware.Execute()
    time_cam1 = time.time()
    cam2.TriggerSoftware.Execute()
    get_img1 = cam1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    get_img2 = cam2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    time_cam2 = time.time()
    return get_img1, get_img2, time_cam1, time_cam2
