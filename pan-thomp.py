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


file = 'sample-data/skx-data-10ksamp.txt'
with open(file) as file_object:
    #next(file_object)
    lines = file_object.readlines()
for i, line in enumerate(lines):
    lines[i] = float(line.strip())
    line = float(line.strip())

# scaling preprocess
def data_scaling(dataset):
    range = np.max(dataset) - np.min(dataset)
    dataset = 1024*((dataset - np.min(dataset)) / range)
    dataset = pd.DataFrame(dataset, columns=['ecgdat'])
    return dataset


data = data_scaling(lines)
data = data[2000:4000].reset_index()

## Add some noise
data['noise'] = data['ecgdat'] + np.random.normal(0, 0.75, len(data))


############################
#     Signal Filtering     #
############################
fs = 150
nyq = 0.5 * fs
# T = 40.0         # seconds
T = (1/fs)*len(lines)
fc_high = 15
fc_low = 5
B, A = butter(2, fc_low / nyq, btype='low') #2nd order BW LowPassFilter
filtered_signal = lfilter(B, A, data['noise'], axis=0)
B, A = butter(2, fc_high / nyq,  btype='high') #2nd order BW HighPassFilter
filtered_signal = lfilter(B, A, filtered_signal, axis=0)

# some amplification
data['filtered'] = filtered_signal*10

n = len(filtered_signal)
print("Length n samples:", n)
t = np.linspace(0, T, n, endpoint=False)

# Plot input signal & filtered signal
plt.subplot(2, 1, 1)
plt.plot(t[1:n], data['noise'][1:n], 'b-', linewidth = 0.5, label='noisy')
plt.plot(t[1:n], data['filtered'][1:n], 'r-', linewidth=1, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)


############################
#  Derivation % Squaring   #
############################
h = [-1., -2., 0., 2., 1.]
derivated_signal = signal.convolve(filtered_signal, h)
derivated_signal = derivated_signal**2
data['derivated'] = derivated_signal[:n]


################################
## Moving Window/Rolling Mean ##
################################
def moving_average(data, hrw, fs):
    mov_avg = pd.Series(data.rolling(window=int(hrw * fs)).mean()) # pandas new rolling mean method, but slower than deprecated method
    # mov_avg = pd.rolling_mean(dataset, window=int(hrw * fs))
    avg_heart_rate = np.mean(data)
    mov_avg = [avg_heart_rate if math.isnan(x) else x for x in mov_avg]
    # print(mov_avg)
    return [1000 + x * 2.5 for x in mov_avg]


data['avg'] = moving_average(data['derivated'], 0.125, fs)
# print(data[0:10])


# detects and locates the x location (time) of the ECG's R peaks
def detect_R_peaks(data):
    window = []
    R_peak_locations = [] #locations of R peaks in given dataset
    count = 0
    avg = data['avg'].tolist()
    deriv = data['derivated'].tolist()
    dat = data['ecgdat'].tolist()
    # print(avg[0:10])

    # TODO Some calculation errors in here [count seems to be wrong]
    for ecg_val in deriv:
        rollingmean = int(avg[count])
        # print("Roll-mean:", rollingmean, dat[count])
        if (int(ecg_val) <= rollingmean) and (len(window) <= 1): # Here is the update in (ecg_val <= rollingmean)
            count += 1
        elif int(ecg_val) > rollingmean:
            window.append(ecg_val)
            count += 1
        else:
            # print("WIndow length:", len(window), "Window index max:", window.index(max(window)))
            # print(count)
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



detect_R_peaks(data)
calculate_RR_intervals(fs)
calculate_bpm()

plt.subplot(2, 1, 2)
# plt.plot(t[1:n], data['filtered'][1:n], 'b-', label='data')
plt.plot(data['derivated'], 'b-', linewidth=1)
plt.plot( data['avg'], 'g-')
plt.scatter(results['R_peak_X_locations'], results['R_peak_Y_locations'], color='red', label="Average heart rate: %.2f BPM" % results['bpm'])
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()