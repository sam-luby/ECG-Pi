#import plotly.plotly as py
import numpy as np
import matplotlib.pyplot as plt

signal_length = 1024
# file = 'ecgresults.txt'
file = 'ecg.txt'

with open(file) as file_object:
    lines = file_object.readlines()

for i, line in enumerate(lines):
    lines[i] = float(line.strip())
    line = float(line.strip())
    print(line)
    print(type(line))


lines = lines[0:signal_length]
plt.plot(lines)
plt.show()