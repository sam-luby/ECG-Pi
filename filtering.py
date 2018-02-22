from __future__ import division

from numpy.fft import fft
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import numpy as np

file = 'ecg.txt'
with open(file) as file_object:
    lines = file_object.readlines()

for i, line in enumerate(lines):
    lines[i] = float(line.strip())
    line = float(line.strip())

noise = np.random.normal(0, 0.75, len(lines))
lines = lines + noise

fs = 256
fc = 11
B, A = butter(2, fc / (fs/2), btype='low') #2nd order BW LPF
filtered_signal = lfilter(B, A, lines, axis=0)

T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
filtered_signal = lfilter(B, A, filtered_signal, axis=0)

#plot FFT of noisy signal
plt.subplot(2, 1, 1)
y = np.fft.fft(filtered_signal)
plt.plot(t[1:n] ,y[1:n])


plt.subplot(2, 1, 2)
plt.plot(t[1:n], lines[1:n], 'b-', label='data')
plt.plot(t[1:n], filtered_signal[1:n], 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()