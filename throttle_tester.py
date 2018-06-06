import Adafruit_MCP4725
import time

dac = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)

dac.set_voltage(125)
time.sleep(2)
dac.set_voltage(2250)
time.sleep(2)
#dac.set_voltage(4096)
#time.sleep(4)
dac.set_voltage(125)
