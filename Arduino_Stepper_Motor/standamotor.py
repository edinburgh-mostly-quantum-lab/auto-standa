import time
import libximc.highlevel as ximc

class Motor():
    def __init__(self, port=None) -> None:
        self.motor = None
        self.port = port
        self.fullStep = 28800
        self.fullStepTime = None
        self.currentAngle = None
        self.currentDirection = 0

    def initMotor(self):
        try:
            device_uri = 'xi-com:' + self.port
            self.motor = ximc.Axis(device_uri)
        except:
            pass

    def degToStep(self, deg):
        step = (deg * self.fullStep) / 360
        return step
    
    def toggleMotorDirection(self):
        self.currentDirection = 1 - self.currentDirection
        return self.currentDirection

    def stepMotor(self, deg):
        if self.currentDirection == 1:
            deg = -1*deg
        step = self.degToStep(deg=deg)
        self.motor.open_device()
        self.motor.command_movr(step, 0)
        self.calcTime(step=step)
        self.motor.close_device()

    def stepToAngle(self, deg):
        if self.currentDirection == 1:
            deg = -1*deg
        step = self.degToStep(deg=deg)
        self.motor.open_device()
        self.motor.command_move(step, 0)
        self.motor.command_move()

    def calcTime(self, step):
        stepTime = (step * self.fullStepTime) / self.fullStep
        return stepTime

    def getAngle(self):
        self.currentAngle = self.motor.get_position()
        return self.currentAngle