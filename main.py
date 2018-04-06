import pan_thomp as pt
import heart_rate_analysis as hrv
import to_thingspeak as thingspeak
import from_arduino as ard
import from_MCP3008 as mcp
import os
import sys
import datetime

##############
#   Params   #
##############
# MODE:
# 1 -> Arduino
# 2 -> RaspberryPI
# 3 -> Debug mode [use pre-recorded data]
mode = 2
T = 30
fs = 250
fc_low = 5
fc_high = 35
now = datetime.datetime.now()
file_suffix= now.strftime("%d-%m-%Y_%Hh%Mm.csv")
Nsamp = T*fs

##############
#    Main    #
##############
if mode == 1:
    filename = ("sample-data/" + "Arduino_" + str(T) + "secs_" + file_suffix)
    #Nsamp = ard.get_data_from_arduino(T, filename)
    results = pt.run_pan_thomp(filename, fs, fc_high, fc_low, Nsamp)      # Run Pan Thompkins algorithm on collected ECG data
    results = hrv.run_hrv_analysis(results)
    thingspeak.update_channel(results)
    #os.remove(filename)                                     # Remove file after processing
elif mode == 2:
    filename = ("sample-data/" + "RPI_" + str(T) + "secs_" + file_suffix)
    commandline = "sudo ./from_MCP3008 " + filename
    os.system(commandline)
    #Nsamp = mcp.get_data_from_MCP(T, filename)
    results = pt.run_pan_thomp(filename, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    results = hrv.run_hrv_analysis(results)
    #os.remove(filename)
elif mode == 3:
    filename = "sample-data/140BPMoutput.csv"
    results = pt.run_pan_thomp(filename, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    results = hrv.run_hrv_analysis(results)
    thingspeak.update_channel(results)
else:
    print("Enter correct mode")

