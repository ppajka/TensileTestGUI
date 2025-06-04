exposure = None
gain = None
rate_load = None
rate_cams = None

def get_vars():
    return exposure, gain, rate_load, rate_cams, cam1, cam2
def set_cam_vars(new_exposure, new_gain, new_rate_cams, new_cam1, new_cam2):
    global exposure, gain, rate_cams, cam1, cam2
    exposure = float(new_exposure)
    gain = float(new_gain)
    rate_cams = float(new_rate_cams)
    cam1 = new_cam1
    cam2 = new_cam2
def set_load_vars(new_rate_load):
    global rate_load
    rate_load = float(new_rate_load)
