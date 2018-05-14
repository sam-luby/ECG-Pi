import serial
from matplotlib import pyplot as plt
from matplotlib import animation


arduino = serial.Serial('COM4', 115200)
Nsamp = 750
fig = plt.figure(figsize=(10, 5))

# y_lim_low =
# y_lim_high =

ax = plt.axes(xlim=(0,Nsamp), ylim=(280, 420))
# ax.get_xaxis().set_visible(False)
ax.set_xticklabels(map(float, ax.get_xticks() / 100))

plt.title('ECG Real-Time Data')
# plt.xlabel('Time [' + str(Nsamp/250) + " second window]")
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
ax.grid(True)

graph, = ax.plot([], [], 'b')

t = list(range(0, Nsamp))
dat = []

for i in range(0, Nsamp):
    dat.append(0)

def init():
    graph.set_data([], [])
    return graph,

def animate(i):
    global t, dat
    # while arduino.in_waiting() == 0:
    #     pass
    dat.append(float(arduino.readline().decode("utf-8")))
    dat.pop(0)
    graph.set_data(t, dat)

    return graph,

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1, blit=True)

plt.show()     