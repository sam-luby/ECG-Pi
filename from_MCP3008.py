import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import pandas as pd

#run pip3 install Adafruit-GPIO & pip3 install Adafruit-MCP3008 if packages not found

# retrieve data from ADC using SPI interface
def get_data_from_MCP(T, filename):
    fs = 250
    i = 0
    Nsamp = T*fs
    milestones = []
    SPI_PORT = 0
    SPI_DEVICE = 0
    for x in range(1, 11):  # List to store Nsamp/multiples of 10 for %age calc
        milestones.append(int(x * (Nsamp / 10)))
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    values = []
    percentage = 10

    print('Reading MCP3008 values, press Ctrl-C to quit...')
    while True and i < Nsamp:
        value = mcp.read_adc(0)
        values.append(value)
        i+=1
        if i in milestones:  # percentage completed indication for user
            print("Collecting data, {}% complete.".format(percentage))
            percentage += 10
        time.sleep(0.004)   # not the best
    print(len(values))
    print("Recording complete, processing ECG data...")
    dat = pd.DataFrame(values)
    dat.to_csv(filename, index=False)
    return Nsamp
        
