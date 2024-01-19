import serial, time, asyncio

class Motor():
    def __init__(self, port=None):
        self.motor = None
        self.port = port
        self.currentAngle = 0
        self.currentDirection = 0

    def initMotor(self):
        try:
            self.motor = serial.Serial(port=self.port, baudrate=115200, timeout=0.1)
        except:
            print("No power meter found")
        else:
            time.sleep(2)
        return self.motor
    
    def sendSerial(self, data):
        data = '<' + str(data) + '>'
        try:
            self.motor.write(data.encode('utf-8'))
        except:
            print("Simulating arduino: Sending " + data)

    def toggleMotorDirection(self):
        self.sendSerial('1')
        self.currentDirection = 1 - self.currentDirection
        return self.currentDirection

    def calcAngle(self, deltaAngle):
        deltaAngle = int(deltaAngle)
        if self.currentDirection == 1:
            deltaAngle = -1 * deltaAngle

        self.currentAngle = self.currentAngle + int(deltaAngle)
        if self.currentAngle >= 360:
            self.currentAngle = self.currentAngle - 360
        elif self.currentAngle < 0:
            self.currentAngle = self.currentAngle + 360
        if self.currentAngle == 360:
            self.currentAngle = 0
        return self.currentAngle

    def stepMotor(self, mode, angle):
        self.sendSerial(str(mode) + ',' + str(angle))
        self.calcAngle(angle)
        time.sleep(0.5)