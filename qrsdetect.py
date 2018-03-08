import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import warnings
from scipy.signal import butter, lfilter

# ignore pandas warning about deprecated function
warnings.simplefilter(action='ignore', category=FutureWarning)
ecg_results = {}


# read ecg data from file and return a pandas data set
def get_dataset(filename):
    dataset = pd.read_csv(filename)
    return dataset


# preprocessing to scale data to allow different data sources
def data_scaling(dataset):
    range = np.max(dataset) - np.min(dataset)
    dataset = 4096*((dataset - np.min(dataset)) / range)
    return dataset


# calculates the rolling mean (moving average) of the ecg data
def moving_average(dataset, hrw, fs):
    # mov_avg = pd.Series(dataset.ecgdat).rolling(window=int(hrw * fs)).mean() # pandas new rolling mean method, but slower than deprecated method
    mov_avg = pd.rolling_mean(dataset.ecgdat, window=int(hrw * fs))
    avg_heart_rate = (np.mean(dataset.ecgdat))
    mov_avg = [avg_heart_rate if math.isnan(x) else x for x in mov_avg]
    mov_avg = [x * 1.1 for x in mov_avg]
    dataset['ecgdat_moving_avg'] = mov_avg


# detects and locates the x location (time) of the ECG's R peaks
def detect_R_peaks(dataset):
    window = []
    R_peak_locations = [] #locations of R peaks in given dataset
    count = 0

    for ecg_val in dataset.ecgdat:
        rollingmean = dataset.ecgdat_moving_avg[count]
        if (ecg_val <= rollingmean) and (len(window) <= 1): # Here is the update in (ecg_val <= rollingmean)
            count += 1
        elif ecg_val > rollingmean:
            window.append(ecg_val)
            count += 1
        else:
            # maximum = max(window)
            beatposition = count - len(window) + (window.index(max(window)))
            R_peak_locations.append(beatposition)
            window = []
            count += 1
    ecg_results['R_peak_X_locations'] = R_peak_locations
    ecg_results['R_peak_Y_locations'] = [dataset.ecgdat[x] for x in R_peak_locations]


# calculate the RR intervals (in milliseconds) [duration between successive R peaks]
def calculate_RR_intervals(fs):
    RR_list = []
    R_peak_locations = ecg_results['R_peak_X_locations']
    count = 0
    # calculate interval between successive RR peaks stored in ecg_results['R_peak_locations'] dictionary element
    while count < (len(R_peak_locations) - 1):
        RR_interval = (R_peak_locations[count + 1] - R_peak_locations[count])
        interval_ms = ((RR_interval / fs) * 1000.0)     #interval is in milliseconds
        RR_list.append(interval_ms)                     #add result to RR intervals list
        count += 1
    ecg_results['RR_list'] = RR_list                    #add list to results dictionary


# calculate heart rate (beats per min)
def calculate_bpm():
    RR_list = ecg_results['RR_list']                    # get list of RR interval values
    ecg_results['bpm'] = 60000 / np.mean(RR_list)       # get average of RR intervals, convert from per ms to per min


# plot the ECG data, including:
    # the original ECG signal
    # the moving average (rolling mean) of the ECG signal
    # the detected peaks of the R signal
def plot_processed_ecg(dataset):
    R_peak_X_locations = ecg_results['R_peak_X_locations']
    R_peak_Y_locations = ecg_results['R_peak_Y_locations']
    plt.title('ECG Signal Plot')
    plt.plot(dataset.ecgdat, alpha=1, color='deepskyblue', label="Input Signal")
    plt.plot(dataset.ecgdat_moving_avg, alpha=0.5, color='green', label="Moving Average of Input")
    plt.scatter(R_peak_X_locations, R_peak_Y_locations, color='red', label="Average heart rate: %.2f BPM" % ecg_results['bpm'])
    plt.legend(loc=3, framealpha=0.5)
    plt.show()


# hrw = one-sided window size
# fs = sampling rate (100Hz for sample data)
def process_data(dataset, hrw, fs):
    moving_average(dataset, hrw, fs)
    detect_R_peaks(dataset)
    calculate_RR_intervals(fs)
    calculate_bpm()


# 5th order butterworth low-pass filter
def butterworth_lowpass_coeff(cutoff, fs, order=5):
        nyq = 0.5 * fs  # nyquist frequency
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

def butterworth_lowpass_filter(data, cutoff, fs, order):
        b, a = butterworth_lowpass_coeff(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y