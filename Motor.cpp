#include "Motor.hpp"

#include "Chrono.h"
//https://github.com/SofaPirate/Chrono

// map pins to pin numbers on board
#define DIR_PIN 2
#define STEP_PIN 3

// init Chrono objects for time keeping
Chrono motorConstChrono(Chrono::MICROS);
Chrono motorAccChrono(Chrono::MICROS);
Chrono motorStepChrono(Chrono::MICROS);

Motor::Motor(uint64_t x) {
    fullRev = x;
}

void Motor::driveMotor() {
    motorState = 1 - motorState; // flip state
    digitalWrite(STEP_PIN, motorState);
}

void Motor::motor(int motorMode) {
    switch (motorMode)
    {
    case 0: // motor off
        motorState = LOW;
        digitalWrite(STEP_PIN, motorState);
        break;

    case 1: // motor constant speed
        motorConst(100);
    break;

    case 2: // motor accelerate
        motorAcc(50, 500);
        break;

    case 3: // motor step in degrees
        motorStep(degToStep(degNum), 100);
        break;
    
    default:
        Serial.println("Error: Invalid mode for motor");
        break;
    }
}

void Motor::motorConst(int duration) {
    // chrono
    if (motorConstChrono.hasPassed(duration)) {
        motorConstChrono.restart();

        driveMotor();        
    }
}

void Motor::motorAcc(int minDuration, int maxDuration) {
    static int duration = maxDuration;
    static int cycleAcc = 200;

    // reset function state if direction changes
    if (reset) {
        duration = maxDuration;
        cycleAcc = 200;
        resetFun(false);
    }

    // chrono
    if (motorAccChrono.hasPassed(duration)) {
        motorAccChrono.restart();

        driveMotor();  

        // decreasing duration
        if (cycleAcc <= 0) {
            cycleAcc = 200;
            if (duration > minDuration) {
                duration--;
            }
        }
        cycleAcc--;
    }
}

uint64_t Motor::degToStep(int deg) {
    uint64_t steps = (fullRev * deg) / 360;
    return steps;
}

void Motor::motorStep(uint64_t steps, int duration) {
    static long double stepCount = steps;

    // reset function state if direction changes
    if (reset) {
        stepCount = steps;
        resetFun(false);
    }

    // chrono
    if (motorStepChrono.hasPassed(duration)) {
        motorStepChrono.restart();

        // decreasing steps
        if (stepCount > 0) {
            Motor::driveMotor();
            stepCount--;
        }
    }
}

void Motor::motorRevs(int revolutions) {
    
}

void Motor::resetFun(bool state) {
    if (state == true) {
        reset = true;
    }
    else
    {
        reset = false;
    }
}