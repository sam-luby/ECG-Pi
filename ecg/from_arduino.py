import serial
import time
import pandas as pd


# gather data from Arduino using serial port
def get_data_from_arduino(T, fs, filename):                        # arg (T) is how long to record for
    print("Recording ECG data for {} seconds.".format(T))
    FS = fs                                         # sampling rate [set by arduino, dont change]
    Nsamp = FS*T                                     # number of samples to obtain
    milestones = []
    for x in range(1,11):                            # List to store Nsamp/multiples of 10 for %age calc
        milestones.append(int(x*(Nsamp/10)))
    arduino = serial.Serial('COM3', 115200, timeout=1)  # USB Port, Baud Rate
    time.sleep(1)                                       # allow for connection to be established
    dat = []
    i = 1
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
    print("Recording complete, processing ECG data...")
    dat = pd.DataFrame(dat)

    # store data in csv
    dat.to_csv(filename, index=False)
    return Nsamp