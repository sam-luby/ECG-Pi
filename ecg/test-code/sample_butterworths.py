from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import numpy as np


# Filter coefficients function
def butterworth(cutoff, fs, btype, order=5):
    btype = btype
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype, analog=False)
    return b, a


def butter_filter(data, cutoff, fs, btype, order=5):
    btype = btype
    b, a = butterworth(cutoff, fs, btype, order=order)
    y = lfilter(b, a, data)
    return y

def butter_bandpass(data, low, high, freq, order):
    nyq = 0.5*freq
    low = low/nyq
    high = high/nyq
    b,a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y


# Filter requirements.
fs = 256.0       # sample rate, Hz
cutoff_low = 5  # desired cutoff frequency of the filter, Hz
cutoff_high = 10
cutoff = cutoff_low
order = 6

btype_low = 'low'
btype_high = 'high'
btype = btype_low

# Get the filter coefficients so we can check its frequency response.
b, a = butterworth(cutoff, fs, btype, order)

# Plot the frequency response (top graph).
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.1*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_filter(data, cutoff, fs, btype, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()