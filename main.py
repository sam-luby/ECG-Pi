import pan_thomp as pt
import from_arduino as ard
import from_MCP3008 as mcp
import os
import sys

##############
#   Params   #
##############
# MODE:
# 1 -> Arduino
# 2 -> RaspberryPI
mode = 2
T = 30
fs = 250
fc_low = 5
fc_high = 15
file_name = 'sample-data/mcpout.csv'

##############
#    Main    #
##############
if mode == 1:
    Nsamp = ard.get_data_from_arduino(T)
    pt.run_pan_thomp(file_name, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    os.remove(file_name)                                     # Remove file after processing
elif mode == 2:
    Nsamp = mcp.get_data_from_MCP(T)
    pt.run_pan_thomp(file_name, fs, fc_high, fc_low, Nsamp)  # Run Pan Thompkins algorithm on collected ECG data
    #os.remove(file_name)
else:
    print("Enter correct mode")

