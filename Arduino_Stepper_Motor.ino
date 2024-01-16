#include "Motor.h"

// for serial communication
const byte numChars = 32;
char receivedData[numChars];
char tempChars[numChars];

int mode = 0;
int angle = 0;

bool newData = false;

Motor motor(400);

void setup() {
    Serial.begin(115200); // init serial for communication with board
    delay(1);
    motor.initPins();
    digitalWrite(DIR_PIN, motor.motorDirection);
}

void loop() {
    while (Serial.available()) {
        readData(); // read serial data
        if (newData == true) { // parse data for mode and angle
            strcpy(tempChars, receivedData);
            parseData();
            newData = false;
        }

        digitalWrite(EN_PIN, LOW);
        switch (mode)
        {
        case 1: // change motor direction
            motor.motorChangeDir();
            Serial.println("Toggled motor direction");
            break;

        case 2: // step motor at slowest speed
            motor.motorMicroStep(angle);
            break;

        case 3: // satellite profile
            motor.motorMicroStep(angle);
            motor.motorChangeDir();
            motor.motorMicroStep(angle);
            motor.motorChangeDir();
            break;

        default:
            break;
        }
        motor.resetPins();
        mode = 0;
        angle = 0;
        clearSerialBuffer();
    }
}

void readData() {
    static bool recvInProgress = false;
    static byte idx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char dataChar;

    while (Serial.available() > 0 && newData == false) {
        dataChar = Serial.read();

        if (recvInProgress == true) {
            if (dataChar != endMarker) {
                receivedData[idx] = dataChar;
                idx++;
                if (idx >= numChars) {
                    idx = numChars - 1;
                }
            }
            else {
                receivedData[idx] = '\0'; // terminates the string
                recvInProgress = false;
                idx = 0;
                newData = true;
            }
        }
        else if (dataChar == startMarker) {
            recvInProgress = true;
        } 
    }
}

void parseData() { // accepts data as <int mode, int angle>
    char * strtokIdx;

    strtokIdx = strtok(tempChars, ",");
    mode = atoi(strtokIdx);

    strtokIdx = strtok(NULL, ",");
    angle = atoi(strtokIdx);
}

void printData() {
    if (newData == true) {
        Serial.print("Received data: ");
        Serial.println(receivedData);
        newData = false;
    }
}

void clearSerialBuffer() {
    while (Serial.available() > 0) {
        Serial.read();
    }
}