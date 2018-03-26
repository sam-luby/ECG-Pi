import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#run pip3 install Adafruit-GPIO & pip3 install Adafruit-MCP3008 if packages not found



SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

print('Reading MCP3008 values, press Ctrl-C to quit...')
while True:
    value = mcp.read_adc(0)
    print(value)
    time.sleep(0.5)
        
    