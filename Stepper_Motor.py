import serial, time
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as numpy
import matplotlib.pyplot as plt

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

def writeData(data):
    data = '<' + data + '>'
    arduino.write(data.encode('utf-8'))

# while True:
print(menu)
inp = input("<Mode>, <Angle>: ")
writeData(inp)