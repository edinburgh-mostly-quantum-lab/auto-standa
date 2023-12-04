import serial, time

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

menu = """Select option:
0. Quit
1. Turn off motor
2. Toggle motor direction
3. Enable motor: constant velocity
4. Enable motor: accelerate
5. Enable motor: angle
"""

def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    time.sleep(0.05) 
    data = arduino.readline() 
    return data 

while True:
    option = input(menu)
    if option == 0:
        break
    else:
        value = write_read(option)
