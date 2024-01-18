import json
import datetime
from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import asyncio

fileName = ''

arduinoPort = '/dev/ttyACM0'
arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)

powerMeterPort = '/dev/usbtmc0'
inst = USBTMC(device=powerMeterPort)
powerMeter = ThorlabsPM100(inst=inst)

time.sleep(2)

async def powerMeterRead():
    global powerMeter
    for x in range(0, 2500):
        powerMeterReading = powerMeter.read
        timeStamp = datetime.datetime.now().timestamp()
        yield powerMeterReading, timeStamp
        # data.append({powerMeterReading: timeStamp})
    # return data

def plotData(xVals, yVals, xlabel, ylabel):
    global fileName
    plt.plot(xVals, yVals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fileName + '.png')

async def measure():
    # data = {}
    global fileName
    fileName = str(datetime.datetime.now())
    # data = powerMeterRead()
    refPower = powerMeter.read

    for x in range(0,2500):
        power = powerMeter.read
        timeStamp = datetime.date.now().timetamp()
        loss = -10*np.log10(np.divide(power, refPower))
        yield loss, timeStamp

    # for x in range(0,2500):
    #     power = powerMeter.read
    #     timeStamp = datetime.datetime.now().timestamp()
    #     loss = -10*np.log10(np.divide(power, refPower))
    #     data.update({timeStamp:loss})

    # with open('calibration.json', 'w') as f:
    #     f.write(json.dumps(data, indent=2))

    # plotData(data.keys(), data.values(), 'Timestamp', 'Loss (dB)')

def sendSerial(data):
    global arduino
    data = '<' + str(data) + '>'
    try:
        arduino.write(data.encode('utf-8'))
    except:
        # print("Simulating arduino: Sending " + data)
        pass
    else:
        print(data)

def stepMotor(mode, angle):
    sendSerial(str(mode) + ',' + str(angle))

async def motor():
    stepMotor(6,360)

async def main():
    await asyncio.gather(measure(), motor())

if __name__ == '__main__':
    asyncio.run(main())