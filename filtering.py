from __future__ import division

from numpy.fft import fft
import scipy
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
fc_high = 11
fc_low = 5
B, A = butter(2, fc_low / (fs/2), btype='low') #2nd order BW LPF
filtered_signal = lfilter(B, A, lines, axis=0)

T = 5.0         # seconds
# n = len(filtered_signal)
n = int(T * fs) # total number of samples
Ts = 1/n
t = np.linspace(0, T, n, endpoint=False)

# B, A = butter(2, fc_high / (fs/2), btype='high')
# filtered_signal_2 = lfilter(B, A, lines, axis=0)

# filtered_signal = filtered_signal_1 + filtered_signal_2

#plot FFT of noisy signal
# plt.subplot(2, 1, 1)
# Y = np.fft.fft(filtered_signal)/
# plt.plot(t[1:n], Y[1:n])

# yf = scipy.fftpack.fft(filtered_signal)
# xf = np.linspace(0.0, 1.0/(2.0*Ts), n/2)
# fig, ax = plt.subplots()
# plt.subplot(2, 1, 1)
# ax.plot(xf, 2.0/n* np.abs(yf[:n//2]))




plt.subplot(2, 1, 2)
plt.plot(t[1:n], lines[1:n], 'b-', label='noisy')
plt.plot(t[1:n], filtered_signal[1:n], 'r-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()