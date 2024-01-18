import asyncio, datetime, serial, time, json, csv
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

powerMeter = ''
arduino = ''

def initDevices():
    global powerMeter, arduino
    powerMeterPort = '/dev/usbtmc0'
    inst = USBTMC(device=powerMeterPort)
    powerMeter = ThorlabsPM100(inst=inst)

    arduinoPort = '/dev/ttyACM0'
    arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)

    time.sleep(2)

async def loopMeaure():
    for x in range(2500):
        power = powerMeter.read
        timeStamp = datetime.datetime.now().timestamp()
        yield power, timeStamp

async def measure():
    refPower = powerMeter.read
    powerList = []
    timeStampList = []
    lossList = []
    async for power, timeStamp in loopMeaure():
        powerList.append(power)
        loss = -10*np.log10(np.divide(power, refPower))
        lossList.append(loss)
        timeStampList.append(timeStamp)

    return powerList, lossList, timeStampList

async def calibrateMotor():
    arduino.write('<6,360>'.encode('utf-8'))

async def satellitePass():
    arduino.write('<6,350>'.encode('utf-8'))
    time.sleep(13)
    arduino.write('<1>'.encode('utf-8'))
    time.sleep(1)
    arduino.write('<6,350>'.encode('utf-8'))
    time.sleep(13)
    arduino.write('<1>'.encode('utf-8'))

def plotData(fileName, xVals, yVals, xlabel, ylabel):
    plt.plot(xVals, yVals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fileName + '.png')

def main():
    fileName = str(datetime.datetime.now())
    initDevices()

    # asyncio.run(calibrateMotor())
    asyncio.run(satellitePass())
    power, loss, timeStamp = asyncio.run(measure())

    plotData(fileName, timeStamp, loss, 'Timestamp', 'Loss (dB)')

    data = np.column_stack((power, loss, timeStamp))
    DF = pd.DataFrame(data)
    DF.to_csv(fileName + '.csv')

if __name__ == '__main__':
    main()