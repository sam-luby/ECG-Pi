# import pySerial as ps
import csv
import serial
import time
import numpy as np
import pandas as pd

# TODO Maybe check Length of CSV file. when == 10ksamp or whatever, read, delete.
# TODO Maybe paired files to read/write simultaneously, switch when = Nsamp


arduino = serial.Serial('COM4', 115200, timeout=1)
time.sleep(1)  # allow for connection to be established
dat = []
i = 0

while True and i < 1000:
    data = arduino.readline()
    if data:
        dat.append(int(data))
        # print(int(data))
        i+=1

print(dat)
print(len(dat))

dat = pd.DataFrame(dat)
print(dat)
dat.to_csv("sample-data/output.csv")
