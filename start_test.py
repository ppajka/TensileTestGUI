import threading
import time
import numpy as np
import pandas as pd
# import openpyxl for pandas
from pypylon import pylon
import serial  # pyserial
from collect_load import *
from collect_images import *
from shared_vars import get_vars


def cam_thread(stop_event):
    global time_cam1_array, time_cam2_array
    img_count = 0
    time_cam1_array = [time.time()]
    time_cam2_array = [time.time()]
    while not stop_event.is_set():
        img_count += 1

        get_img1, get_img2, time_cam1, time_cam2 = collect_images(cam1, cam2, exposure)
        time_cam1_array.append(time_cam1)
        time_cam2_array.append(time_cam2)

        img1 = get_img1.GetArray()
        img2 = get_img2.GetArray()
        # release results
        get_img1.Release()
        get_img2.Release()

        cv2.imwrite(f"{img_folder}/img-00{img_count:04d}_0.png", img1)
        cv2.imwrite(f"{img_folder}/img-00{img_count:04d}_1.png", img2)

        event.wait()  # Wait for event to be set
        event.clear()  # Reset the event for the next iteration

def load_thread(stop_event):
    global time_load_array, force, displacement
    period_cams = 0
    period_load = 0
    force = []
    displacement = []
    time_load_array = [time.time()]
    while not stop_event.is_set():
        period_cams += period_load
        t1 = time.time()
        force_raw, travel_raw, time_load = collect_load()
        if period_cams >= (rate_cams - rate_load):
            event.set()
            period_cams = 0

        force.append(raw2data(force_raw, -2))
        displacement.append(raw2data(travel_raw, -3))
        time_load_array.append(time_load)
        period_load = time.time() - t1
        if period_load < rate_load:
            time.sleep(rate_load - period_load)
            period_load = time.time() - time_load

def start_acquisition(GUI, text_inputs):
    global exposure, gain, rate_load, rate_cams, cam1, cam2, \
        img_folder, load_file, event, start_time, stop_event, \
        time_cam1_array, time_cam2_array, time_load_array, force, displacement
    img_folder = text_inputs[0]
    load_file = text_inputs[1]
    GUI.destroy()
    time.sleep(1)
    exposure, gain, rate_load, rate_cams, cam1, cam2 = get_vars()


    cam1.TriggerSelector.SetValue("FrameStart")
    cam1.TriggerMode.SetValue("On")
    cam1.TriggerSource.SetValue("Software")
    cam2.TriggerSelector.SetValue("FrameStart")
    cam2.TriggerMode.SetValue("On")
    cam2.TriggerSource.SetValue("Software")

    cam1.Gain.SetValue(gain)
    cam2.Gain.SetValue(gain)

    cam1.ExposureTime.SetValue(exposure)
    cam2.ExposureTime.SetValue(exposure)

    cam1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    cam2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    event = threading.Event()
    stop_event = threading.Event()

    # Create threads
    start_time = time.time()
    thread1 = threading.Thread(target=cam_thread, args=(stop_event,))
    thread2 = threading.Thread(target=load_thread, args=(stop_event,))

    # Start threads
    thread1.start()
    thread2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Test Stopped")
        # stop grabbing images
        cam1.StopGrabbing()
        cam2.StopGrabbing()
        cam1.Close()
        cam2.Close()
        ser_port.close()

        time_cam1_array = [x - time_cam1_array[0] for x in time_cam1_array[1:]]
        time_cam2_array = [x - time_cam2_array[0] for x in time_cam2_array[1:]]
        time_load_array = [x - time_load_array[0] for x in time_load_array[1:]]

        max_length = max(len(time_cam1_array), len(time_cam2_array), len(time_load_array), len(force))

        time_cam1_array += [float('nan')] * (max_length - len(time_cam1_array))
        time_cam2_array += [float('nan')] * (max_length - len(time_cam2_array))
        time_load_array += [float('nan')] * (max_length - len(time_load_array))
        force += [float('nan')] * (max_length - len(force))
        displacement += [float('nan')] * (max_length - len(displacement))

        test_data_excel = pd.DataFrame({'Cam1 Time': time_cam1_array,
                                        'Cam2 Time': time_cam2_array,
                                        'Force Time': time_load_array,
                                        'Force': force,
                                        'Displacement': displacement})

        specimen_excel = pd.read_excel(load_file)
        final_data_excel = pd.concat([specimen_excel.iloc[:, :2], test_data_excel], axis=1)

        final_data_excel.to_excel(load_file, index=False)

        stop_event.set()
        thread1.join()
        thread2.join()



