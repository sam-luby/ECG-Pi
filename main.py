import matplotlib.pyplot as plt
import sample_butterworths as filt
import numpy as np

file = 'ecg.txt'


with open(file) as file_object:
    lines = file_object.readlines()

for i, line in enumerate(lines):
        lines[i] = float(line.strip())
        line = float(line.strip())

fs = 256
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)


filter = filt.butter_bandpass(lines, 5, 15, 256, 5)
# filter = filt.butter_filter(lines, 20, fs, 'high', 3)

plt.subplot(2, 1, 2)
plt.plot(t[1:n], lines[1:n], 'b-', label='data')
plt.plot(t[1:n], filter[1:n], 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()

