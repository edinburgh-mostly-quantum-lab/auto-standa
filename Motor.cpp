#include "Motor.h"

Motor::Motor(uint64_t t_fullRevStep) {
    fullRevStep = t_fullRevStep;
}

void Motor::driveMotor() { // drives motor in alternating HIGH LOW to step motor
    motorState = 1 - motorState; // flip state
    digitalWrite(STEP_PIN, motorState);
    delay(1);
    motorState = 1 - motorState; // flip state
    digitalWrite(STEP_PIN, motorState);
    delay(1);
}

void Motor::motorChangeDir() {
    motorDirection = 1 - motorDirection;
    digitalWrite(DIR_PIN, motorDirection);
}

void Motor::motorMicroStep(int t_deg) {
    digitalWrite(MS1_PIN, HIGH); //Pull MS1, MS2, MS3 high to set logic to 1/16th microstep resolution
    digitalWrite(MS2_PIN, HIGH);
    digitalWrite(MS3_PIN, HIGH);

    uint64_t steps = 16*degToStep(t_deg);

    for (int s=0; s<steps; s++) {
        driveMotor();
    }
}

uint64_t Motor::degToStep(int t_deg) {
    uint64_t steps = (fullRevStep * t_deg) / 360;
    return steps;
}

void Motor::initPins() {
    pinMode(DIR_PIN, OUTPUT);       // enable pin to control motor direction
    pinMode(STEP_PIN, OUTPUT);      // enable pin to control motor steps
    pinMode(MS1_PIN, OUTPUT);
    pinMode(MS2_PIN, OUTPUT);
    pinMode(MS3_PIN, OUTPUT);
    pinMode(EN_PIN, OUTPUT);
}

void Motor::resetPins() {
    digitalWrite(STEP_PIN, LOW);
    digitalWrite(MS1_PIN, LOW);
    digitalWrite(MS2_PIN, LOW);
    digitalWrite(MS3_PIN, LOW);
    digitalWrite(EN_PIN, HIGH);
}