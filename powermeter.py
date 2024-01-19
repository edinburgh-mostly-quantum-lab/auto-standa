from ThorlabsPM100 import ThorlabsPM100, USBTMC
import datetime
import numpy as np

class PowerMeter:
    def __init__(self, port=None):
        self.powermeter = None
        self.port = port

    def initPowerMeter(self):
        try:
            inst = USBTMC(device=self.port)
        except:
            print("No power meter found")
        else:
            self.powermeter = ThorlabsPM100(inst=inst)
        return self.powermeter

    def read(self): # single power measurement
        return self.powermeter.read
    
    # repeated async measurements
    async def loopMeaure(self, duration):
        for x in range(duration):
            power = self.powermeter.read
            timeStamp = datetime.datetime.now().timestamp()
            yield power, timeStamp

    async def measure(self, duration):
        powerList = []
        timeStampList = []
        lossList = []
        if self.powermeter == 0:
            refPower = self.powermeter.read
            async for power, timeStamp in self.loopMeaure(duration=duration):
                powerList.append(power)
                loss = -10*np.log10(np.divide(power, refPower))
                lossList.append(loss)
                timeStampList.append(timeStamp)  
        else:
            refPower = 20
            async for x, (power, timeStamp) in range(duration):
                power = refPower - 0.01*x
                powerList.append(power)
                loss = -10*np.log10(np.divide(power, refPower))
                lossList.append(loss)
                timeStampList.append(timeStamp)
        return powerList, lossList, timeStampList
