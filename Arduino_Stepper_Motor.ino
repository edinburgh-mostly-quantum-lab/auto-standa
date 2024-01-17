// Pin layout: Driver board -> Wire colour -> Arduino
// DIR  -> Red    -> 2
// STEP -> Red    -> 3
// GND  -> Black  -> GND (DIGITAL)
// MS3  -> Green  -> 8
// MS2  -> Orange -> 9
// MS1  -> White  -> 10
// EN   -> Yellow -> 12

#include "Motor.h"

// for serial communication
const byte numChars = 32;
char receivedData[numChars];
char tempChars[numChars];
bool newData = false;

int mode = 0;
int angle = 0;

Motor motor(400);

void setup() {
    Serial.begin(115200); // init serial for communication with board
    delay(1);
    motor.initPins();
    digitalWrite(DIR_PIN, motor.motorDirection);
}

void loop() {
    while (Serial.available()) {
        readData();             // read serial data
        if (newData == true) {  // parse data for mode and angle
            strcpy(tempChars, receivedData);
            parseData();
            newData = false;
        }
        digitalWrite(EN_PIN, LOW);
        switch (mode) {
            case 1: // change motor direction
                motor.motorChangeDir();
                break;

            case 2:
                motor.motorFullStep(angle);
                break;

            case 3:
                motor.motorHalfStep(angle);
                break;

            case 4:
                motor.motorQuarterStep(angle);
                break;

            case 5:
                motor.motorEighthStep(angle);
                break;

            case 6:
                motor.motorSixteenthStep(angle);
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

void readData() { // incomming serial data must encapsulated in < >
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
    mode = atoi(strtokIdx);     // motor mode

    strtokIdx = strtok(NULL, ",");
    angle = atoi(strtokIdx);    // angle for motor step
}

void clearSerialBuffer() {
    while (Serial.available() > 0) {
        Serial.read();
    }
}