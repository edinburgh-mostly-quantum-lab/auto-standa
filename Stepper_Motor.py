import serial, os
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as numpy
import matplotlib.pyplot as plt

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.1)

# Check if power meter is detected
try: 
    inst = USBTMC(device="/dev/usbtmc0")
    powerMeter = ThorlabsPM100(inst=inst)
    powerMeterStatus = 1
    powerMeterMessage = "Power meter found"
except:
    powerMeterStatus = 0
    powerMeterMessage = "Power meter not found"

menu = """Select option:
0. Quit
1. Toggle motor direction
2. Step motor at slowest speed
3. Motor profile: Satellite Sweep"""

def writeData(data):
    data = '<' + data + '>'
    arduino.write(data.encode('utf-8'))

while True:
    # os.system('clear')
    print(powerMeterMessage)
    print(menu)
    userInput = input("<Mode>,<Angle>: ")
    match userInput:
        case "0":
            break

        case "2":
            arduinoStatus = arduino.readline().decode('ascii').strip()
            print("Arduino status: " + arduinoStatus)
            if powerMeterStatus:
                uPow = powerMeter.read()
                print(powerMeter)

        case _:
            print("Invalid input")

    writeData(userInput)