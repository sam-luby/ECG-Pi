import pan_thomp as pt
import numpy as np
import from_arduino as ard
import pandas as pd


##############
#    Main    #
##############

ard.get_data_from_arduino(30)
file_name = 'sample-data/output.csv'
lines = pt.open_data_file(file_name)
data = pt.data_scaling(lines)
data = data[0:5000].reset_index()
fs = 250

## Add some noise
data['noise'] = data['ecgdat'] + np.random.normal(0, 0.75, len(data))
data['filtered'] = pt.filter_signal(data['noise'], 15, 5, 250)
n, t = pt.get_interval(fs, lines, data)
pt.plot_input_and_filtered(data['ecgdat'], data['filtered'], n, t)
data['derivated'] = pt.derivate_signal(data['filtered'], n)
data['avg'] = pt.moving_average(data['derivated'], 0.125, fs)
pt.detect_R_peaks(data)
pt.calculate_RR_intervals(fs)
pt.calculate_bpm()
pt.plot_derivated_and_peaks(data['derivated'], data['avg'], n, t)