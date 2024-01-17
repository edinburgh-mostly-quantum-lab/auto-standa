import serial, os, time
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as numpy
import matplotlib.pyplot as plt

# Check if arduino is detected
try:
    arduinoPort = '/dev/ttyACM0'
    arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)
except:
    try:
        arduinoPort = '/dev/ttyACM1'
        arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)
    except:
        arduinoStatus = 0
        arduinoMessage = "Arduino not found"
    else:
        arduinoStatus = 1
        arduinoMessage = "Arduino found at " + arduinoPort
else:
    arduinoStatus = 1
    arduinoMessage = "Arduino found at " + arduinoPort 

# Check if power meter is detected
try:
    powerMeterPort = "/dev/usbtmc0"
    inst = USBTMC(device=powerMeterPort)
except:
    powerMeterStatus = 0
    powerMeterMessage = "Power meter not found"
else:
    powerMeter = ThorlabsPM100(inst=inst)
    powerMeterStatus = 1
    powerMeterMessage = "Power meter found at " + powerMeterPort

currentAngle = 0
currentDirection = 0

menu = """Select option:
0. Reset current angle to zero
1. Toggle motor direction
2. Step motor: Full step
3. Step motor: Half step
4. Step motor: Quarter step
5. Step motor: Eighth step
6. Step motor: Sixteenth step
7. Motor profile: Satellite Sweep"""

def writeData(data):
    data = '<' + data + '>'
    try:
        arduino.write(data.encode('utf-8'))
    except:
        print("Simulating arduino: Sending " + data)

def printStatus():
    global currentAngle, currentDirection, arduinoMessage, powerMeterMessage
    print(arduinoMessage)
    print(powerMeterMessage)
    if currentDirection == 0:
        dirMessage = "Motor direction: Clockwise"
    else:
        dirMessage = "Motor direction: Counter-clockwise"
    print(dirMessage)
    print("Current motor angle: " + str(currentAngle))

def calcAngle(deltaAngle):
    deltaAngle = int(deltaAngle)
    global currentAngle, currentDirection
    if currentDirection == 0:
        deltaAngle = -1 * deltaAngle
        
    currentAngle = currentAngle + int(deltaAngle)
    if currentAngle >= 360:
        currentAngle = currentAngle - 360
    elif currentAngle < 0:
        currentAngle = currentAngle + 360

def toggleDir():
    global currentDirection
    writeData("1")
    currentDirection = 1 - currentDirection

def stepMotor(mode, angle):
    writeData(str(mode + "," + angle))
    calcAngle(angle)
    time.sleep(0.5)

def parseInput(input): # seperate input into mode, fullAngle, stepAngle
    inputList = input.strip().split(",")
    mode = inputList[0]
    fullAngle = inputList[1]
    # stepAngle = inputList[2]

    return mode, fullAngle

def powerDataAcq():
    with open('data.txt', 'w') as f:
        f.write(str(powerMeter.read()) + " ")

def main():
    global currentAngle
    while True:
        # os.system('clear')
        printStatus()
        print(menu)

        userInput = input("<Mode>,<Full Angle>,<Angle Step>: ")
        mode, fullAngle = parseInput(userInput)
        match int(mode):
            case 0: # reset angle
                currentAngle = 0

            case 1:
                toggleDir()

            case num if 1 < num < 7:
                stepMotor(mode, fullAngle)

            # case 7: # satellite profile, step 5 deg, wait, record power, step,
            #     stepMotor()

            case 9: # quit
                break

            case _:
                print("Invalid input")

if __name__ == '__main__':
    main()