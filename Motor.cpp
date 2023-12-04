#include "Motor.h"
#include "Chrono.h"
//https://github.com/SofaPirate/Chrono

// map pins to pin numbers on board
#define DIR_PIN 2
#define STEP_PIN 3

// init Chrono objects for time keeping
Chrono motorConstChrono(Chrono::MICROS);
Chrono motorAccChrono(Chrono::MICROS);
Chrono motorStepChrono(Chrono::MICROS);
Chrono motorSatSweepChrono(Chrono::MICROS);

Motor::Motor(uint64_t t_fullRevStep) {
    fullRevStep = t_fullRevStep;
}

void Motor::driveMotor() {
    motorState = 1 - motorState; // flip state
    digitalWriteFast(STEP_PIN, motorState);
}

void Motor::motor(int motorMode, int a, int b, int c) {
    switch (motorMode)
    {
    case 0: // motor off
        motorState = LOW;
        digitalWriteFast(STEP_PIN, motorState);
        break;

    case 1: // motor constant speed
        motorConst(a);
        break;

    case 2: // motor accelerate
        motorAcc(a, b);
        break;

    case 3: // motor step in degrees
        motorStep(a, b, c);
        break;
    
    default:
        Serial.println("Error: Invalid mode for motor");
        break;
    }
}

void Motor::motorChangeDir() {
    motorDirection = 1 - motorDirection;
    digitalWriteFast(DIR_PIN, motorDirection);
}

void Motor::motorConst(int t_interval) {
    // chrono
    if (motorConstChrono.hasPassed(t_interval)) {
        motorConstChrono.restart();

        driveMotor();        
    }
}

void Motor::motorAcc(int t_minInterval, int t_maxInterval) {
    static int interval = t_maxInterval;
    static int cycleAcc = 200;

    // reset function state if direction changes
    if (reset) {
        interval = t_maxInterval;
        cycleAcc = 200;
        resetFun(false);
    }

    // chrono
    if (motorAccChrono.hasPassed(interval)) {
        motorAccChrono.restart();

        driveMotor();

        // decreasing duration
        if (cycleAcc <= 0) {
            cycleAcc = 200;
            if (interval > t_minInterval) {
                interval--;
            }
        }
        cycleAcc--;
    }
}

uint64_t Motor::degToStep(int t_deg) {
    uint64_t steps = (fullRevStep * t_deg) / 360;
    return steps;
}

void Motor::motorStep(uint16_t t_angle, int t_count, int t_interval) {
    static int count = t_count;
    static uint64_t steps = degToStep(t_angle);

    // reset function state if direction changes
    if (reset) {
        steps = degToStep(t_angle);
        count = t_count;
        resetFun(false);
    }

    // chrono
    if (motorStepChrono.hasPassed(t_interval)) {
        motorStepChrono.restart();

        if (count > 0) {
            // decreasing steps
            if (steps > 0) {
                driveMotor();
                steps--;
            }
            else {
                count--;
                steps = degToStep(t_angle);
            }
        }
    }
}

void Motor::resetFun(bool t_state) {
    if (t_state == true) {
        reset = true;
    }
    else {
        reset = false;
    }
}