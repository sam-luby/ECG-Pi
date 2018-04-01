from scipy.signal import butter, lfilter
import numpy as np
from scipy.signal.waveforms import chirp, sweep_poly
from scipy import signal
from pylab import figure, plot, show, xlabel, ylabel, subplot, grid, title, \
                    yscale, savefig, clf

import matplotlib.pyplot as plt

FIG_SIZE = (7.5, 3.75)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def make_linear(f0, t1, f1, filename=None, fig_size=FIG_SIZE):
    t = np.linspace(0, t1, 5001)
    w = chirp(t, f0=f0, f1=f1, t1=t1, method='linear')

    figure(1, figsize=fig_size)
    clf()

    subplot(2,1,1)
    plot(t, w)
    tstr = "Linear Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1)
    title(tstr)

    # subplot(2,1,2)
    # plot(t, f0 + (f1-f0)*t/t1, 'r')
    # grid(True)
    # ylabel('Frequency (Hz)')
    # xlabel('time (sec)')
    # if filename is None:
    #     show()
    # else:
    #     savefig(filename)

    return w


f0 = 0
f1 = 20
t1 = 10
t = np.linspace(0, t1, 5001)
sig = make_linear(f0, t1, f1)

f_low = 8
f_high = 12
fs = 100

filtered_signal = butter_bandpass_filter(sig, 0.2, 0.6, fs, 3)
subplot(2, 1, 2)

plot(t, filtered_signal)
show()


# b, a = signal.butter(5, rads, 'low')
# W, h = signal.freqs(b, a)
# plt.subplot(2,1,2)
# plt.semilogx(W, 20 * np.log10(abs(h)))
# plt.title('Butterworth filter frequency response')
# plt.xlabel('Frequency [radians / second]')
# plt.ylabel('Amplitude [dB]')
# plt.margins(0, 0.01)
# plt.grid(which='both', axis='both')
# plt.axvline(rads, color='green') # cutoff frequency
# plt.show()
#

# B, A = butter(2, normal_cutoff, btype='low') #2nd order BW LPF

# filtered_signal = lfilter(b, a, sig)
# subplot(2, 1, 2)
# plot(t, filtered_signal)
# show()