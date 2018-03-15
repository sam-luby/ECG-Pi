import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


file = 'sample-data/ecg.txt'
with open(file) as file_object:
    lines = file_object.readlines()

for i, line in enumerate(lines):
    lines[i] = float(line.strip())
    line = float(line.strip())


fs = 256
T = 1/fs

# transfer function
h = [-1., -2., 0., 2., 1.]
filtered_signal = signal.convolve(lines, h)
filtered_signal = filtered_signal**2

# plt.plot(filtered_signal[1:5000])
# plt.show()

T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)


plt.subplot(2, 1, 2)
plt.plot(t[1:n], lines[1:n], 'b-', label='data')
plt.plot(t[1:n], filtered_signal[1:n], 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()