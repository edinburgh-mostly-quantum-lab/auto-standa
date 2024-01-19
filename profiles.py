import motor
import powermeter

import time
import asyncio

async def measurePower(powerMeter, duration):
    power, loss, timeStamp = powerMeter.measure(duration)
    return power, loss, timeStamp

async def calibrateMotor(arduino):
    arduino.stepMotor(6,360)

async def calibrateProfile(arduino, powerMeter):
    asyncio.run(calibrateMotor(arduino))
    power, loss, timeStamp = asyncio.run(measurePower(powerMeter, 2500))
    return power, loss, timeStamp

# async def satelliteMotor():
#     arduino.stepMotor(6,360)
#     time.sleep(13)
#     arduino.toggleMotorDirection()
#     time.sleep(1)
#     arduino.stepMotor(6,360)
#     time.sleep(13)
#     arduino.toggleMotorDirection()

# async def satellitePower():
#     powerMeter.measure(2500)

# async def satelliteProfile():
#     asyncio.run(satelliteMotor())
#     power, loss, timeStamp = asyncio.run(measurePower(2500))
#     return power, loss, timeStamp