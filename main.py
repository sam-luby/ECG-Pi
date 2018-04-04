import pan_thomp as pt
import from_arduino as ard
#import from_MCP3008 as mcp
import mcp_new as mcp
import os
import sys
import datetime

##############
#   Params   #
##############
# MODE:
# 1 -> Arduino
# 2 -> RaspberryPI
mode = 1
T = 30
fs = 250
fc_low = 5
fc_high = 35
now = datetime.datetime.now()
file_suffix= now.strftime("%d-%m-%Y %Hh%Mm.csv")
Nsamp = T*fs

##############
#    Main    #
##############
if mode == 1:
    filename = ("sample-data/" + "Arduino " + str(T) + "secs " + file_suffix)
    Nsamp = ard.get_data_from_arduino(T, filename)
    pt.run_pan_thomp(filename, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    #os.remove(filename)                                     # Remove file after processing
elif mode == 2:
    filename = ("sample-data/" + "RPI " + str(T) + "secs " + file_suffix)
    #Nsamp = mcp.get_data_from_MCP(T, filename)
    pt.run_pan_thomp(filename, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    #os.remove(filename)
else:
    print("Enter correct mode")

