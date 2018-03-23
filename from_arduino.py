import csv
import numpy as np
import serial
import time
import pandas as pd

# TODO Maybe check Length of CSV file. when == 10ksamp or whatever, read, delete.
# TODO Maybe paired files to read/write simultaneously, switch when = Nsamp


def get_data_from_arduino(T):
    FS = 250                                         #sampling rate [set by arduino, dont change]
    T = T                                            # time, in seconds, to record for
    Nsamp = FS*T                                     # number of samples to obtain
    arduino = serial.Serial('COM4', 115200, timeout=1)  # USB Port, Baud Rate
    time.sleep(1)                                       # allow for connection to be established
    dat = []
    i = 0
    while True and i < Nsamp:                       #While there is data to record & less than specified number of samples
        data = arduino.readline()
        if data:
            dat.append(int(data))
            i+=1
    print(len(dat))
    dat = pd.DataFrame(dat)
    dat.to_csv("sample-data/output.csv", index=False)