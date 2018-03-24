import csv
import numpy as np
import serial
import time
import pandas as pd

# TODO Maybe check Length of CSV file. when == 10ksamp or whatever, read, delete.
# TODO Maybe paired files to read/write simultaneously, switch when = Nsamp


def get_data_from_arduino(T):                        # arg (T) is how long to record for
    print("Recording ECG data for {} seconds.".format(T))
    FS = 250                                         # sampling rate [set by arduino, dont change]
    Nsamp = FS*T                                     # number of samples to obtain
    milestones = []
    for x in range(1,11):                            # List to store Nsamp/multiples of 10 for %age calc
        milestones.append(int(x*(Nsamp/10)))
    arduino = serial.Serial('COM4', 115200, timeout=1)  # USB Port, Baud Rate
    time.sleep(1)                                       # allow for connection to be established
    dat = []
    i = 0
    percentage = 10

    while True and i < Nsamp:                       #While there is data to record & less than specified number of samples
        data = arduino.readline()
        if data:
            dat.append(int(data))                   #Add ADC samples to list until time reached
            i+=1
            if i in milestones:                     #Silly %age completed indication for user
                print("Collecting data, {}% complete.".format(percentage))
                percentage+=10
    # print(len(dat))
    dat = pd.DataFrame(dat)
    dat.to_csv("sample-data/output.csv", index=False)