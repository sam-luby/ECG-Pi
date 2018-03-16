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



# def get_dataset(filename):
#     dataset = pd.read_csv(filename)
#     return dataset


# File IO
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
    return dataset


lines = data_scaling(lines)
data = lines[2000:4000]
# data = pd.DataFrame(data, columns=['ecgdata'])

## Add some noise
noise = np.random.normal(0, 0.75, len(data))
noisy_signal = data + noise

print(len(lines))
print(len(data))
print(len(noisy_signal))

############################
#     Signal Filtering     #
############################
fs = 250
nyq = 0.5 * fs
# T = 40.0         # 5 seconds
T = (1/fs)*len(lines)
fc_high = 15
fc_low = 5
B, A = butter(2, fc_low / nyq, btype='low') #2nd order BW LowPassFilter
filtered_signal = lfilter(B, A, noisy_signal, axis=0)
B, A = butter(2, fc_high / nyq,  btype='high') #2nd order BW HighPassFilter
filtered_signal = lfilter(B, A, filtered_signal, axis=0)
filtered_signal = filtered_signal*10

n = len(filtered_signal)
Ts = 1/n
t = np.linspace(0, T, n, endpoint=False)

# Plot input signal & filtered signal
plt.subplot(2, 1, 1)
plt.plot(t[1:n], noisy_signal[1:n], 'b-', label='noisy')
plt.plot(t[1:n], filtered_signal[1:n], 'r-', linewidth=2, label='filtered data')
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


################################
## Moving Window/Rolling Mean ##
################################
def moving_average(dataset, hrw, fs):
    # mov_avg = pd.Series(dataset.ecgdat).rolling(window=int(hrw * fs)).mean() # pandas new rolling mean method, but slower than deprecated method
    mov_avg = pd.rolling_mean(dataset, window=int(hrw * fs))
    avg_heart_rate = (np.mean(dataset))
    mov_avg = [avg_heart_rate if math.isnan(x) else x for x in mov_avg]
    return [x * 5 for x in mov_avg]
    #dataset['ecgdat_moving_avg'] = mov_avg

mov_avg = moving_average(derivated_signal, 1, fs)


plt.subplot(2, 1, 2)
# plt.plot(t[1:n], filtered_signal[1:n], 'b-', label='data')
plt.plot(t[1:n], derivated_signal[1:n], 'g-', linewidth=2, label='Derivated Signal')
plt.plot(t[1:n], mov_avg[1:n], 'r-', label='Moving Average')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()

