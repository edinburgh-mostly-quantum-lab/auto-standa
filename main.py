import motor
import powermeter
import profiles

import os
import asyncio
import datetime
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

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

def clear():
    if os.name == 'posix':  # macOS and Linux
        _ = os.system('clear')
    
    elif os.name == 'nt': # Windows
        _ = os.system('cls')

def initDevices():
    arduino = motor.Motor(port='/dev/ttyACM0')
    arduino.initMotor()

    powerMeter = powermeter.PowerMeter(port='/dev/usbtmc0')
    powerMeter.initPowerMeter()

    return arduino, powerMeter

def parseInput(input): # seperate input into mode, fullAngle, stepAngle
    inputList = input.strip().split(',')
    mode = inputList[0]
    try:
        fullAngle = inputList[1]
    except:
        fullAngle = 0
    return mode, fullAngle

def printStatus(arduino, powerMeter):
    if arduino.port:
        arduinoStatus = 'Arduino found at ' + arduino.port
    else:
        arduinoStatus = 'No arduino found'
    print(arduinoStatus)
    if powerMeter.port:
        powerMeterStatus = 'Power meter found at ' + powerMeter.port
    else:
        powerMeterStatus = 'No power meter found'
    print(powerMeterStatus)
    try:
        print('Current power: ' + str(powerMeter.read()) + ' W')
    except:
        print('Current power: 0 W')

    if arduino.currentDirection == 0:
        dirMessage = 'Motor direction: Forwards'
    else:
        dirMessage = 'Motor direction: Backwards'
    print(dirMessage)
    print('Current motor angle: ' + str(arduino.currentAngle) + '°')

def plotData(fileName, xVals, yVals, xlabel, ylabel):
    plt.figure(fileName)
    plt.plot(xVals, yVals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fileName + '.png')

def writeToCSV(data):
    pass

def main():
    arduino, powerMeter = initDevices()
    filePath = 'data/'
    if not os.path.exists:
        os.mkdir(filePath)
        
    while True:
        clear()
        printStatus(arduino=arduino, powerMeter=powerMeter)
        print(menu)

        userInput = input('<Mode>,<Angle>: ')
        mode, angle = parseInput(input=userInput)

        match int(mode):
            case 0: # reset angle
                arduino.currentAngle = 0

            case 1: # toggle motor direction
                arduino.toggleMotorDirection()

            case num if 1 < num < 7: # step motor at varying speeds
                arduino.stepMotor(mode=mode, angle=angle)

            case 7: # satellite profile, step 5 deg, wait, record power, step,
                fileName = filePath + str(datetime.datetime.now().timestamp())

                # power, loss, timeStamp = profiles.satelliteProfile(arduino, powerMeter)

                # plotData(fileName, timeStamp, loss, 'Timestamp', 'Loss (dB)')

                # data = np.column_stack((power, loss, timeStamp))
                # DF = pd.DataFrame(data)
                # DF.to_csv(fileName + '.csv')
                pass
                
            case 8: # calibration profile
                fileName = filePath + str(datetime.datetime.now().timestamp())

                asyncio.run(arduino.asyncStepMotor(mode=6, angle=720))
                power, loss, timeStamp = asyncio.run(powerMeter.measure(duration=5000))

                # filter data for full cycle
                peaks, _ = find_peaks(loss, height=0)
                filterLoss = loss[0:peaks[-1]]
                filterTime = timeStamp[0:peaks[-1]]
                maxTime = max(filterTime)
                minTime = min(filterTime)
                timeRange = maxTime - minTime

                # normalise to 0 to 360
                angle = [(value - minTime) / timeRange * 360 for value in filterTime]

                # build dictionary of angles and loss
                angleRound = [round(num) for num in angle]
                df = pd.DataFrame({
                    'loss': filterLoss,
                    'angle': angleRound
                })
                angleDict = df.groupby('angle').mean()['loss'].to_dict()
                
                # write dictionary to file
                with open('calibration.json', 'w') as f:
                    json.dump(angleDict, f, indent=2)
                plotData('calibration.png', angleDict.keys(), angleDict.values(), 'Angle (°)', 'Loss (dB)')

            case 9: # quit
                break

            case _:
                print('Invalid input')

if __name__ == '__main__':
    main()