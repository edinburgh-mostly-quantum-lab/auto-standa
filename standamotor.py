import time
import libximc.highlevel as ximc

class Motor():
    def __init__(self, port=None) -> None:
        self.motor = None
        self.port = port
        self.fullStep = 28800
        self.currentAngle = None

    def initMotor(self):
        try:
            device_uri = 'xi-com:' + self.port
            self.motor = ximc.Axis(device_uri)
        except:
            pass

    def degToStep(self, deg):
        step = (deg * self.fullStep) / 360
        return step

    def stepMotor(self, deg):
        step = self.degToStep(deg=deg)
        self.motor.open_device()
        self.motor.command_movr(step, 0)
        self.calcTime(step=step)
        self.motor.close_device()

    def calcTime(self, step):
        pass

    def getAngle(self):
        self.currentAngle = self.motor.get_position()