import serial

arduinoPort = '/dev/ttyACM0'
arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)
arduino.write('<6,360>'.encode('utf-8'))

# arduinoPort = '/dev/ttyACM0'
# arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)

# def sendSerial(data):
#     data = '<' + str(data) + '>'
#     try:
#         arduino.write(data.encode('utf-8'))
#     except:
#         print("Simulating arduino: Sending " + data)

# def stepMotor(mode, angle):
#     sendSerial(str(mode) + ',' + str(angle))

# def main():
# arduinoPort = '/dev/ttyACM0'
# arduino = serial.Serial(port=arduinoPort, baudrate=115200, timeout=0.1)
# arduino.write('<6,90>'.encode('utf-8'))

# if __name__ == '__main__':
#     main()