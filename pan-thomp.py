from __future__ import division
import scipy.signal as signal
import matplotlib.pyplot as plt
from numpy.fft import fft
import scipy
from scipy.signal import butter, lfilter
import numpy as np
import pandas as pd
import math
import warnings

# ignore pandas warning about deprecated function
warnings.simplefilter(action='ignore', category=FutureWarning)
results = {}
file_name = 'sample-data/ecgdata2min.csv'


# open file
def open_data_file(file):
    with open(file) as file_object:
        # next(file_object)
        lines = file_object.readlines()
    for i, line in enumerate(lines):
        lines[i] = float(line.strip())
    return lines


# scaling preprocess
def data_scaling(dataset):
    range = np.max(dataset) - np.min(dataset)
    dataset = 1024*((dataset - np.min(dataset)) / range)
    dataset = pd.DataFrame(dataset, columns=['ecgdat'])
    return dataset


def filter_signal(noisy_signal, high, low, fs):
    fs = 250
    nyq = 0.5 * fs
    fc_high = high
    fc_low = low
    B, A = butter(2, fc_low / nyq, btype='low') #2nd order BW LowPassFilter
    filtered_signal = lfilter(B, A, noisy_signal, axis=0)
    B, A = butter(2, fc_high / nyq, btype='high')  # 2nd order BW HighPassFilter
    filtered_signal = lfilter(B, A, filtered_signal, axis=0)
    # some amplification
    return filtered_signal


def get_time_period(fs):
    T = (1/fs)*len(lines)
    n = len(data['filtered'])
    print("Length n samples:", n)
    t = np.linspace(0, T, n, endpoint=False)
    return n, t


#  TODO Change this (input signal is not really noisy)
# Plot input signal & filtered signal
def plot_input_and_filtered(input, filtered, n ,t):
    # input = data['noise']
    # filtered = data['filtrered']
    plt.subplot(2, 1, 1)
    plt.plot(t[1:n], input[1:n], 'b-', linewidth = 0.5, label='noisy')
    plt.plot(t[1:n], filtered[1:n], 'r-', linewidth=1, label='filtered data')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()
    plt.subplots_adjust(hspace=0.35)


#  derivate and square signal
def derivate_signal(data):
    h = [-1., -2., 0., 2., 1.]
    derivated_signal = signal.convolve(data, h)
    derivated_signal = derivated_signal ** 2
    deriv = derivated_signal[:n]
    return deriv


# rolling mean/moving average
def moving_average(data, hrw, fs):
    # mov_avg = pd.Series(data.rolling(window=int(hrw * fs)).mean()) # pandas new rolling mean method, but slower than deprecated method
    mov_avg = pd.rolling_mean(data, window=int(hrw * fs))
    avg_heart_rate = np.mean(data)
    mov_avg = [avg_heart_rate if math.isnan(x) else x for x in mov_avg]
    avg = [1000 + x * 2.5 for x in mov_avg]
    return avg


# detects and locates the x location (time) of the ECG's R peaks
def detect_R_peaks(data):
    window = []
    R_peak_locations = [] #locations of R peaks in given dataset
    count = 0
    avg = data['avg'].tolist()
    deriv = data['derivated'].tolist()

    for ecg_val in deriv:
        rollingmean = int(avg[count])
        if (int(ecg_val) <= rollingmean) and (len(window) <= 1): # Here is the update in (ecg_val <= rollingmean)
            count += 1
        elif int(ecg_val) > rollingmean:
            window.append(ecg_val)
            count += 1
        else:
            beatposition = count - len(window) + (window.index(max(window)))
            R_peak_locations.append(beatposition)
            window = []
            count += 1
    results['R_peak_X_locations'] = R_peak_locations
    results['R_peak_Y_locations'] = [deriv[x] for x in R_peak_locations]
    print("R PEAK Y LOCS:", results['R_peak_Y_locations'])


# calculate the RR intervals (in milliseconds) [duration between successive R peaks]
def calculate_RR_intervals(fs):
    RR_list = []
    R_peak_locations = results['R_peak_X_locations']
    print("R Peak Locations (x axis):", R_peak_locations)
    count = 0
    # calculate interval between successive RR peaks stored in ecg_results['R_peak_locations'] dictionary element
    while count < (len(R_peak_locations) - 1):
        RR_interval = (R_peak_locations[count + 1] - R_peak_locations[count])
        interval_ms = ((RR_interval / fs) * 1000.0)     #interval is in milliseconds
        RR_list.append(interval_ms)                     #add result to RR intervals list
        count += 1
    results['RR_list'] = RR_list                    #add list to results dictionary


# calculate heart rate (beats per min)
def calculate_bpm():
    RR_list = results['RR_list']                    # get list of RR interval values
    print("RR List:", RR_list)
    results['bpm'] = 60000 / np.mean(RR_list)       # get average of RR intervals, convert from per ms to per min



##############
#    Main    #
##############
lines = open_data_file(file_name)
data = data_scaling(lines)
data = data[0:2500].reset_index()
fs = 250

## Add some noise
data['noise'] = data['ecgdat'] + np.random.normal(0, 0.75, len(data))
data['filtered'] = filter_signal(data['noise'], 15, 5, 250)
n, t = get_time_period(fs)

plot_input_and_filtered(data['noise'], data['filtered'], n, t)

data['derivated'] = derivate_signal(data['filtered'])
data['avg'] = moving_average(data['derivated'], 0.125, fs)

print(data[100:200])

detect_R_peaks(data)
calculate_RR_intervals(fs)
calculate_bpm()

plt.subplot(2, 1, 2)
# plt.plot(t[1:n], data['filtered'][1:n], 'b-', label='data')
plt.plot(data['derivated'], 'b-', linewidth=1)
plt.plot(data['avg'], 'g-')
plt.scatter(results['R_peak_X_locations'], results['R_peak_Y_locations'], color='red', label="Average heart rate: %.2f BPM" % results['bpm'])
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()