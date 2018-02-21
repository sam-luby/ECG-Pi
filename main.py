import qrsdetect as qrs


file = 'ecg_sample.csv'

with open(file) as file_object:
    lines = file_object.readlines()

for i, line in enumerate(lines):
        lines[i] = float(line.strip())
        line = float(line.strip())

ecg = qrs.plot_peak_detection(lines, 128)