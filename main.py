import qrsdetect as hb #Assuming we named the file 'heartbeat.py'
import matplotlib.pyplot as plt

dataset = hb.get_data("data2.csv")
hb.process(dataset, 0.75, 100)

bpm = hb.measures['bpm']

dataset = hb.get_data('data2.csv')
dataset = dataset[6000:12000].reset_index(drop=True) #For visibility take a subselection of the entire signal from samples 6000 - 12000 (00:01:00 - 00:02:00)

filtered = hb.butter_lowpass_filter(dataset.hart, 2.5, 100.0, 5)#filter the signal with a cutoff at 2.5Hz and a 5th order Butterworth filter

#Plot it
plt.subplot(211)
plt.plot(dataset.hart, color='Blue', alpha=0.5, label='Original Signal')
plt.legend(loc=4)
plt.subplot(212)
plt.plot(filtered, color='Red', label='Filtered Signal')
plt.ylim(200,800) #limit filtered signal to have same y-axis as original (filter response starts at 0 so otherwise the plot will be scaled)
plt.legend(loc=4)
plt.show()

#To view all objects in the dictionary, use "keys()" like so:
# print(hb.measures.keys())