import pan_thomp as pt
import numpy as np
import from_arduino as ard
import pandas as pd
import os


##############
#   Params   #
##############
T = 30
fs = 250
fc_low = 5
fc_high = 15
file_name = 'sample-data/output.csv'

##############
#    Main    #
##############
Nsamp = ard.get_data_from_arduino(T)                        # Gets ECG data from Arduino for T seconds
samples_to_plot = Nsamp                                     # Number of samples to plot
pt.run_pan_thomp(file_name, fs, fc_high, fc_low, Nsamp)     # Run Pan Thompkins algorithm on collected ECG data
# os.remove(file_name)                                        # Remove file after processing