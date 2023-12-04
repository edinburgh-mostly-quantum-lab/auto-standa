#include "Motor.h"

// map pins to pin numbers on board
#define DIR_PIN 2
#define STEP_PIN 3

// for standard C++-like printing
template <typename T>
Print& operator<<(Print& printer, T value)
{
    printer.print(value);
    return printer;
}

Motor stepperMotor(13520);

void setup() {
    Serial.begin(115200); // init serial for communication with board
    delay(1);

    pinMode(LED_BUILTIN, OUTPUT);   // init serial for communication with board
    pinMode(DIR_PIN, OUTPUT);       // enable pin to control motor direction
    pinMode(STEP_PIN, OUTPUT);      // enable pin to control motor steps

    digitalWrite(DIR_PIN, stepperMotor.motorDirection);
}

void loop() {
    if (Serial.available()) {
        int option = Serial.readString().toInt(); 
        switch (option)
        {
        case 1: // turn motor off
            stepperMotor.motorMode = 0;
            stepperMotor.resetFun(true);
            break;

        case 2: // reverse motor direction
            stepperMotor.motorChangeDir();
            stepperMotor.resetFun(true);
            break;

        case 3: // drive motor with constant speed
            stepperMotor.motorMode = 1;
            stepperMotor.resetFun(true);
            break;

        case 4: // accelerate motor
            stepperMotor.motorMode = 2;
            stepperMotor.resetFun(true);
            break;

        case 5: // step motor
            stepperMotor.motorMode = 3;
            stepperMotor.resetFun(true);
            break;

        case 6: // sat sweep profile
            stepperMotor.motorMode = 4;
            stepperMotor.resetFun(true);
            break;
        
        default:
            Serial.println("Error: Invalid input");
            break;
        }
    }
    stepperMotor.motor(stepperMotor.motorMode);
}