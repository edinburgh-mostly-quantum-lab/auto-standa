import serial, time
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import pyvisa

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

# inst = USBTMC(device="/dev/usbtmc0")
# power_meter = ThorlabsPM100(inst=inst)

menu = """Select option:
0. Quit
1. Turn off motor
2. Toggle motor direction
3. Enable motor: constant velocity
4. Enable motor: accelerate
5. Enable motor: angle
6. Motor profile: Satellite Sweep
7. Calibrate motor
"""

def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    time.sleep(0.05)
    data = arduino.readline() 
    return data 

while True:
    option = input(menu)
    if option == 0:
        break
    else:
        value = write_read(option)
        # print(power_meter.read)
