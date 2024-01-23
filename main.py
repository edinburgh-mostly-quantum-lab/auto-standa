from arduinomotor import Motor
import powermeter
import profiles

import os
import asyncio
import time
import datetime
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

menu = '''Select option:
0. Reset current angle to zero
1. Toggle motor direction
2. Step motor: Full step
3. Step motor: Half step
4. Step motor: Quarter step
5. Step motor: Eighth step
6. Step motor: Sixteenth step
7. Rotate to loss level
8. Motor profile: Satellite Sweep
9. Calibrate
Q. Quit'''

def clear():
    if os.name == 'posix':  # macOS and Linux
        _ = os.system('clear')
    
    elif os.name == 'nt': # Windows
        _ = os.system('cls')

def initDevices():
    try:
        motor = Motor(port='/dev/ttyACM0')
    except:
        motor = Motor(port='/dev/ttyACM1')
    motor.initMotor()

    powerMeter = powermeter.PowerMeter(port='/dev/usbtmc0')
    powerMeter.initPowerMeter()

    return motor, powerMeter

def parseInput(input): # seperate input into mode, fullAngle, stepAngle
    inputList = input.strip().split(',')
    mode = inputList[0]
    try:
        fullAngle = inputList[1]
    except:
        fullAngle = 0
    return mode, fullAngle

def printStatus(motor, powerMeter):
    if motor.port:
        motorStatus = 'Motor found at ' + motor.port
    else:
        motorStatus = 'No motor found'
    print(motorStatus)
    if powerMeter.port:
        powerMeterStatus = 'Power meter found at ' + powerMeter.port
    else:
        powerMeterStatus = 'No power meter found'
    print(powerMeterStatus)
    try:
        print('Current power: ' + str(powerMeter.read()) + ' W')
    except:
        print('Current power: 0 W')

    if motor.currentDirection == 0:
        dirMessage = 'Motor direction: Forwards'
    else:
        dirMessage = 'Motor direction: Backwards'
    print(dirMessage)
    print('Current motor angle: ' + str(motor.currentAngle) + '°')

def plotData(fileName, xVals, yVals, xlabel, ylabel):
    plt.figure(fileName)
    plt.plot(xVals, yVals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fileName + '.png')

def writeToCSV(data):
    pass

def main():
    motor, powerMeter = initDevices()
    filePath = 'data/'
    if not os.path.exists:
        os.mkdir(filePath)
        
    while True:
        clear()
        printStatus(motor=motor, powerMeter=powerMeter)
        print(menu)

        userInput = input('<Mode>,<Angle>: ')
        if userInput == 'q' or userInput == 'Q':
            break

        mode, angle = parseInput(input=userInput)

        match int(mode):
            case 0: # reset angle
                motor.currentAngle = 0

            case 1: # toggle motor direction
                motor.toggleMotorDirection()

            case num if 1 < num < 7: # step motor at varying speeds
                motor.stepMotor(mode=mode, angle=angle)

            case 7:
                if os.path.isfile('calibration.json'):
                    targetLoss = angle
                    # load calibration file
                    with open('calibration.json', 'r') as file:
                        data = json.load(file)

                    # find closest loss value
                    closestLoss = min(data, key=lambda x: abs(data[x] - targetLoss))
                    
                    targetAngle = data[closestLoss]

                    deltaAngle = targetAngle - motor.currentAngle
                    if deltaAngle < 0:
                        motor.toggleMotorDirection()
                        deltaAngle = -1*deltaAngle
                        motor.stepMotor(6,deltaAngle)
                        time.sleep(1)
                        motor.toggleMotorDirection()
                        
                else:
                    print("No calibration file found")

            case 8: # satellite profile, step 5 deg, wait, record power, step,
                fileName = filePath + str(datetime.datetime.now().timestamp())

                # power, loss, timeStamp = profiles.satelliteProfile(motor, powerMeter)

                # plotData(fileName, timeStamp, loss, 'Timestamp', 'Loss (dB)')

                # data = np.column_stack((power, loss, timeStamp))
                # DF = pd.DataFrame(data)
                # DF.to_csv(fileName + '.csv')
                pass
                
            case 9: # calibration profile
                fileName = filePath + str(datetime.datetime.now().timestamp())

                asyncio.run(motor.asyncStepMotor(mode=6, angle=720))
                power, loss, timeStamp = asyncio.run(powerMeter.measure(duration=5000))

                date = [datetime.fromtimestamp(ts) for ts in timeStamp]
                seconds = [(dt - date[0]).total_seconds() for dt in date]

                # find the index where the steep rise begins
                threshold = 0.01
                rise_start_index = np.argmax(np.gradient(loss) > threshold)

                # truncate the data up to the identified index
                truncTime = seconds[:rise_start_index]
                truncLoss = loss[:rise_start_index]

                maxTime = max(truncTime)
                minTime = min(truncTime)
                timeRange = maxTime - minTime

                # normalise between 0 and 359
                angle = [(value - minTime) / timeRange * 359 for value in truncTime]

                # build dictionary of angles and loss
                angleRound = [round(num) for num in angle]
                df = pd.DataFrame({
                    'loss': truncLoss,
                    'angle': angleRound
                })
                angleDict = df.groupby('angle').mean()['loss'].to_dict()
                
                # write dictionary to file
                with open('calibration.json', 'w') as file:
                    json.dump(angleDict, file, indent=2)
                plotData('calibration.png', angleDict.keys(), angleDict.values(), 'Angle (°)', 'Loss (dB)')

            case _:
                print('Invalid input')

if __name__ == '__main__':
    main()