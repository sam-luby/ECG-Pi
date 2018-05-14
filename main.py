import pan_tomp as pt
import heart_rate_variability_analysis as hrv
import to_thingspeak as thingspeak
import from_arduino as ard
# import from_MCP3008 as mcp
import os
import sys
import datetime
import analyse_results
import time
import argparse

##############
#   Params   #
##############
# MODE:
# 1 -> Arduino
# 2 -> RaspberryPI
# 3 -> Debug mode [use pre-recorded data]



mode = 3
T = 30
fs = 250

fc_low = 0.025*fs
fc_high = 0.075*fs
now = datetime.datetime.now()
file_suffix= now.strftime("%d-%m-%Y_%Hh%Mm.csv")
Nsamp = int(T*fs)
# Nsamp = 450000

##############
#    Main    #
##############
if mode == 1:
    filename = ("sample-data/" + "Arduino_" + str(T) + "secs_" + file_suffix)
    Nsamp = ard.get_data_from_arduino(T, fs, filename)
    results = pt.run_pan_tomp(filename, fs, fc_high, fc_low, Nsamp)      # Run Pan Thompkins algorithm on collected ECG data
    # results = hrv.run_hrv_analysis(results)
    # thingspeak.update_channel(results)
    # analyse_results.keep_or_delete_data(filename, results)

elif mode == 2:
    filename = ("sample-data/" + "RPI_" + str(T) + "secs_" + file_suffix)
    commandline = "sudo ./from_MCP3008 " + filename
    os.system(commandline)
    #Nsamp = mcp.get_data_from_MCP(T, filename)
    results = pt.run_pan_tomp(filename, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    results = hrv.run_hrv_analysis(results)
    # thingspeak.update_channel(results)
    # analyse_results.keep_or_delete_data(filename, results)

elif mode == 3:
    filename = "sample-data/60BPMoutput.csv"

    print("Recording ECG data for {} seconds.".format(T))
    time.sleep(3)
    i = 0
    while i < 10:
        i+=1
        print("Collecting data, " + str(i*10) + "% complete.")
        time.sleep(3)


    results = pt.run_pan_tomp(filename, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    # dat = pt.open_data_file(filename)
    # ecg = pt.data_scaling(dat)
    # pt.plot_input(ecg, Nsamp, T, fs)
    results = hrv.run_hrv_analysis(results)
    print("\n")
    print("Measured Heart Rate: " + str(round(results['bpm'], 2)) + "bpm")
    print("Calculated RMSSD: " + str(round(results['rmssd'], 2)) + "ms")
    print("Calculated SDNN: " + str(round(results['sdnn'], 2)) + "ms")
    print("Calculated pNNx: " + str(round(results['pNNx'], 2)) + "%")
    # print(type(results))
    thingspeak.update_channel(results)
    analyse_results.keep_or_delete_data(filename, results)
else:
    print("Enter correct mode")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", required=True, help="Mode: 1=Arduino, 2=RPI, 3=Debug")
    ap.add_argument("-t", "--time", required=True, help="Period to record for")
    ap.add_argument("-f", "--freq", required=True, help="Sampling Rate")
    args = vars(ap.parse_args())
    # print(args)

    mode = int(args['mode'])
    T = int(args['time'])
    fs = int(args['freq'])
