# Dependencies: pip install pyserial ThorlabsPM100 matplotlib

import serial, os, time, csv, datetime, json, asyncio
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

statusMessage = ''
fileName = ''

# Init motor properties
currentAngle = 0
currentDirection = 0

menu = '''Select option:
0. Reset current angle to zero
1. Toggle motor direction
2. Step motor: Full step
3. Step motor: Half step
4. Step motor: Quarter step
5. Step motor: Eighth step
6. Step motor: Sixteenth step
7. Motor profile: Satellite Sweep
8. Calibrate
9. Quit'''

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
        arduinoMessage = 'Arduino not found'
    else:
        arduinoStatus = 1
        arduinoMessage = 'Arduino found at ' + arduinoPort
else:
    arduinoStatus = 1
    arduinoMessage = 'Arduino found at ' + arduinoPort

# Check if power meter is detected
try:
    powerMeterPort = ''
    inst = USBTMC(device=powerMeterPort)
except:
    powerMeterStatus = 0
    powerMeterMessage = 'Power meter not found'
else:
    powerMeter = ThorlabsPM100(inst=inst)
    powerMeterStatus = 1
    powerMeterMessage = 'Power meter found at ' + powerMeterPort

def sendSerial(data):
    data = '<' + str(data) + '>'
    try:
        arduino.write(data.encode('utf-8'))
    except:
        # print("Simulating arduino: Sending " + data)
        pass
    else:
        print("Sending: " + data)

def toggleDir():
    global currentDirection
    sendSerial('1')
    currentDirection = 1 - currentDirection

def stepMotor(mode, angle):
    sendSerial(str(mode) + ',' + str(angle))
    calcAngle(angle)
    time.sleep(0.5)

def calcAngle(deltaAngle):
    deltaAngle = int(deltaAngle)
    global currentAngle, currentDirection
    if currentDirection == 1:
        deltaAngle = -1 * deltaAngle
        
    currentAngle = currentAngle + int(deltaAngle)
    if currentAngle >= 360:
        currentAngle = currentAngle - 360
    elif currentAngle < 0:
        currentAngle = currentAngle + 360
    if currentAngle == 360:
        currentAngle = 0

def printStatus():
    global currentAngle, currentDirection, arduinoMessage, powerMeter, powerMeterStatus, powerMeterMessage
    print(arduinoMessage)
    print(powerMeterMessage)

    try:
        print('Current power: ' + str(powerMeter.read) + ' W')
    except:
        print('Current power: 0 W')

    if currentDirection == 0:
        dirMessage = 'Motor direction: Forwards'
    else:
        dirMessage = 'Motor direction: Backwards'
    print(dirMessage)
    
    print('Current motor angle: ' + str(currentAngle) + '°')

def parseInput(input): # seperate input into mode, fullAngle, stepAngle
    inputList = input.strip().split(',')
    mode = inputList[0]
    try:
        fullAngle = inputList[1]
    except:
        fullAngle = 0
    try:
        stepAngle = inputList[2]
    except:
        stepAngle = 0

    return mode, fullAngle, stepAngle

def powerDataAcq():
    global powerMeter, currentAngle
    with open(fileName  + '.csv', 'a') as f:
        try:
            powerMeterReading = powerMeter.read
        except:
            powerMeterReading = 0

        timeStamp = datetime.datetime.now().timestamp()

        data=[powerMeterReading, currentAngle, timeStamp]
        writer = csv.writer(f)
        writer.writerow(data)

def calibrate():
    global currentAngle, powerMeter
    lossAngle = {}
    try:
        refPower = powerMeter.read
    except:
        refPower = 20

    for x in range(0, int(360/5)):
        try:
            power = powerMeter.read
        except:
            power = refPower - x
            
        loss = -10*np.log10(np.divide(power, refPower))
        lossAngle.update({loss:currentAngle})
        stepMotor(6, 5)

    with open('calibration.json', 'w') as f: 
        f.write(json.dumps(lossAngle))

    plotData(lossAngle.values(), lossAngle.keys(), 'Angle (°)', 'Loss (dB)')

    # time.sleep(0.5)
    # toggleDir()
    # time.sleep(0.5)
    # stepMotor(2, 350)
    # time.sleep(0.5)
    # toggleDir()

def plotData(xVals, yVals, xlabel, ylabel):
    plt.plot(xVals, yVals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fileName + '.png')

def satellitePass():
    data = []
    with open('calibration.json') as f:
        lossAngle = json.load(f)

    for x, (loss, angle) in enumerate(lossAngle.items()):
        stepMotor(6, 5)
        timeStamp = datetime.datetime.now().timestamp()
        data.append([loss, angle, timeStamp])
    
    with open(fileName  + '.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    lossList = [losses[0] for losses in data]
    angleList = [angles[1] for angles in data]
    timeList = [times[2] for times in data]
    print(angleList)
    print(lossList)
    print(timeList)
    plotData(angleList, lossList, 'Angle (°)', 'Loss (dB)')

def clear():
    if os.name == 'posix':  # macOS and Linux
        _ = os.system('clear')
    
    elif os.name == 'nt': # Windows
        _ = os.system('cls')

async def powerMeterRead(duration):
    global powerMeter
    data = []
    for x in range(0,duration):
        if powerMeterStatus == 1:
            powerMeterReading = powerMeter.read
        else:
            powerMeterReading = x
        timeStamp = datetime.datetime.now().timestamp()
        await asyncio.sleep(1)
        data.append({powerMeterReading: timeStamp})
    return data

def writeToCSV(data):
    fileName = str(datetime.datetime.now())
    with open(fileName  + '.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

async def calibrateMotor():
    global currentAngle
    stepMotor(6,360)

async def main():
    global currentAngle, fileName
    while True:
        fileName = str(datetime.datetime.now())

        # clear()
        printStatus()
        print(menu)

        userInput = input('<Mode>,<Full Angle>,<Angle Step>: ')
        mode, fullAngle, stepAngle = parseInput(userInput)

        match int(mode):
            case 0: # reset angle
                currentAngle = 0

            case 1: # toggle motor direction
                toggleDir()

            case num if 1 < num < 7: # step motor at varying speeds
                stepMotor(mode, fullAngle)
                # powerDataAcq()

            case 7: # satellite profile, step 5 deg, wait, record power, step,
                satellitePass()
                
            case 8:
                async for powerData in powerMeterRead(12):
                    await calibrateMotor()

                with open('calibration.json', 'w') as f: 
                    f.write(json.dumps(powerData, indent=2))

            case 9: # quit
                break

            case _:
                print('Invalid input')

if __name__ == '__main__':
    asyncio.run(main())