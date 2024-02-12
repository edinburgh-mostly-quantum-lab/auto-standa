import motormotor
import Arduino_Stepper_Motor.powermeter as powermeter

import time
import asyncio

async def measurePower(powerMeter, duration):
    power, loss, timeStamp = powerMeter.measure(duration)
    return power, loss, timeStamp

async def calibrateMotor(motor):
    motor.stepMotor(6,360)

async def calibrateProfile(motor, powerMeter):
    asyncio.run(calibrateMotor(motor))
    power, loss, timeStamp = asyncio.run(measurePower(powerMeter, 2500))
    return power, loss, timeStamp

# async def satelliteMotor():
#     motor.stepMotor(6,360)
#     time.sleep(13)
#     motor.toggleMotorDirection()
#     time.sleep(1)
#     motor.stepMotor(6,360)
#     time.sleep(13)
#     motor.toggleMotorDirection()

# async def satellitePower():
#     powerMeter.measure(2500)

# async def satelliteProfile():
#     asyncio.run(satelliteMotor())
#     power, loss, timeStamp = asyncio.run(measurePower(2500))
#     return power, loss, timeStamp