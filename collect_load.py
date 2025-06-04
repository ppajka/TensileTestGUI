import numpy as np
import time
import serial  # pyserial

# serial port and baud rate
ser_port = serial.Serial('COM4', baudrate=115200, timeout=1)

# load frame commands
commands = [
    "n",  # force and travel
    "x"  # request travel
]

def read():  # func to read load frame response
    response = ser_port.readline().decode().strip()
    return response
def write(command):  # func to write command to load frame
    ser_port.write(command.encode())
    return
def collect_load():  # func to collect data every second (testing)
    write(commands[0])
    force_raw = read()
    time_force = time.time()
    travel_raw = read()
    return force_raw, travel_raw, time_force
def raw2data(data_raw, num):  # func to convert str to float
    data = float(data_raw[0:num])  # remove units in str
    return data

