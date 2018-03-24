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


# open file and return data
def open_data_file(file):
    with open(file) as file_object:
        next(file_object)
        lines = file_object.readlines()
    for i, line in enumerate(lines):
        lines[i] = float(line.strip())
    return lines


# scaling pre-processing (to allow different data sets)
def data_scaling(dataset):
    range = np.max(dataset) - np.min(dataset)
    dataset = 1024*((dataset - np.min(dataset)) / range)
    dataset = pd.DataFrame(dataset, columns=['ecgdat'])
    return dataset


# bandpass filter the input signal
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
    return filtered_signal*10


# get time interval array used for plotting functions
def get_interval(fs, lines, data):
    T = (1/fs)*len(lines)
    n = len(data['filtered'])
    t = np.linspace(0, T, n, endpoint=False)
    return n, t


#  derivate and square signal
def derivate_signal(data, n):
    h = [-1., -2., 0., 2., 1.]
    derivated_signal = signal.convolve(data, h)
    derivated_signal = (derivated_signal ** 2)/1000
    deriv = derivated_signal[:n]
    return deriv


# rolling mean/moving average
def moving_average(data, hrw, fs):
    # mov_avg = pd.Series(data.rolling(window=int(hrw * fs)).mean()) # pandas new rolling mean method, but slower than deprecated method
    mov_avg = pd.rolling_mean(data, window=int(hrw * fs))
    avg_heart_rate = np.mean(data)
    mov_avg = [avg_heart_rate if math.isnan(x) else x for x in mov_avg]
    avg = [100+ x * 2.5 for x in mov_avg]
    return avg


# detects and locates the locations of the ECG's R peaks
def detect_R_peaks(data):
    window = []
    R_peak_locations = [] #locations of R peaks in given dataset
    count = 0
    mov_avg = data['avg'].tolist()
    deriv = data['derivated'].tolist()

    for ecg_val in deriv:
        avg = int(mov_avg[count])
        if (int(ecg_val) <= avg) and (len(window) <= 1): # Here is the update in (ecg_val <= rollingmean)
            count += 1
        elif int(ecg_val) > avg:
            window.append(ecg_val)
            count += 1
        else:
            beatposition = count - len(window) + (window.index(max(window)))
            R_peak_locations.append(beatposition)
            window = []
            count += 1
    results['R_peak_X_locations'] = R_peak_locations
    results['R_peak_Y_locations'] = [deriv[x] for x in R_peak_locations]


# calculate the RR intervals (in milliseconds) [duration between successive R peaks]
def calculate_RR_intervals(fs):
    RR_list = []
    R_peak_locations = results['R_peak_X_locations']
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
    results['bpm'] = 60000 / np.mean(RR_list)       # get average of RR intervals, convert from per ms to per min


# Plot input signal & filtered signal
def plot_input_and_filtered(input, filtered, n ,t):
    plt.plot(t[1:n], input[1:n], 'b-', linewidth = 0.5, label='Noisy Input Signal')
    plt.plot(t[1:n], filtered[1:n], 'r-', linewidth=1, label='Filtered Signal')
    plt.xlabel('Time [sec]')
    plt.ylabel('Amplitude [ADC Values]')
    plt.grid()
    plt.legend()
    plt.show()

# TODO Scale RPeak Y Locations (so I can use seconds as X axis)
def plot_derivated_and_peaks(derivated, avg, n ,t):
    plt.plot(derivated[1:n], 'b-', linewidth=1, label='Derivated Signal', zorder=1)
    plt.plot(avg[1:n], 'g-', label='Moving Average', zorder=2)
    plt.scatter(results['R_peak_X_locations'], results['R_peak_Y_locations'], color='red', label="Average HR: %.2f BPM" % results['bpm'], zorder=3)
    plt.xlabel('Samples')
    plt.grid()
    plt.legend(loc='upper center', bbox_to_anchor=(0.9, 1.175), fancybox=True, framealpha=1, shadow=True)
    plt.show()