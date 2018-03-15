from __future__ import division
import scipy.signal as signal
import matplotlib.pyplot as plt
from numpy.fft import fft
import scipy
from scipy.signal import butter, lfilter
import numpy as np
import pandas as pd



def get_dataset(filename):
    dataset = pd.read_csv(filename)
    return dataset


# File IO
file = 'sample-data/ecg.txt'
with open(file) as file_object:
    next(file_object)
    lines = file_object.readlines()

for i, line in enumerate(lines):
    lines[i] = float(line.strip())
    line = float(line.strip())



## Add some noise
noise = np.random.normal(0, 0.75, len(lines))
noisy_signal = lines + noise


############################
#     Signal Filtering     #
############################
fs = 256
nyq = 0.5 * fs
T = 5.0         # 5 seconds
#T = (1/fs)*len(lines)
fc_high = 11
fc_low = 5
B, A = butter(2, fc_low / nyq, btype='low') #2nd order BW LowPassFilter
filtered_signal = lfilter(B, A, noisy_signal, axis=0)


# B, A = butter(2, fc_high / nyq,  btype='high') #2nd order BW HighPassFilter
# filtered_signal2 = lfilter(B, A, noisy_signal, axis=0)

#filtered_signal = filtered_signal1 + filtered_signal2

#n = len(filtered_signal)
n = int(T * fs) # total number of
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


plt.subplot(2, 1, 2)
plt.plot(t[1:n], filtered_signal[1:n], 'b-', label='data')
plt.plot(t[1:n], derivated_signal[1:n], 'g-', linewidth=2, label='Derivated Signal')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()