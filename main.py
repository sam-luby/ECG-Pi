import qrsdetect as ecg
import matplotlib.pyplot as plt

#data2 is recorded at 100Hz
file = "data2.csv"
dataset = ecg.get_dataset(file)


# ignore
if (file == "data2.csv"):
    dataset = dataset[6000:8000].reset_index(drop=True)

# preprocessing (scaling)
dataset = ecg.data_scaling(dataset)

ecg.process_data(dataset, 1, 100)
ecg.plot_processed_ecg(dataset)
print("Average heart rate for displayed ECG data: %.2f BPM" % ecg.ecg_results['bpm'])

#filter signal with 5 order lowpass filter [fc = 2.5Hz, fs = 100Hz, order = 5]
filtered = ecg.butterworth_lowpass_filter(dataset.ecgdat, 2.5, 100.0, 5)

#plot signal vs filtered signal
plt.subplot(211)
plt.plot(dataset.ecgdat, color='Blue', alpha=0.5, label='Original Signal')
plt.legend(loc=4)
plt.subplot(212)
plt.plot(filtered, color='Red', label='Filtered Signal')
# plt.ylim(400,600)
plt.legend(loc=4)
plt.show()

#objects in dictionary
print(ecg.ecg_results.keys())
print("R Peak X [Time] Locations:", ecg.ecg_results['R_peak_X_locations'])
print("R Peak Y [Amplitude]:", ecg.ecg_results['R_peak_Y_locations'])
print("RR Intervals [milliseconds]", ecg.ecg_results['RR_list'])