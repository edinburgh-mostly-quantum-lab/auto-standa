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
        motorAngle(180, 100);
        break;
    
    default:
        Serial.println("Error: Invalid mode for motor");
        break;
    }
}

void Motor::motorConst(int t_interval) {
    // chrono
    if (motorConstChrono.hasPassed(t_interval)) {
        motorConstChrono.restart();

        driveMotor();        
    }
}

void Motor::motorAcc(int t_minInterval, int t_maxInterval) {
    static int duration = t_maxInterval;
    static int cycleAcc = 200;

    // reset function state if direction changes
    if (reset) {
        duration = t_maxInterval;
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
            if (duration > t_minInterval) {
                duration--;
            }
        }
        cycleAcc--;
    }
}

uint64_t Motor::degToStep(int t_deg) {
    uint64_t steps = (fullRev * t_deg) / 360;
    return steps;
}

void Motor::motorAngle(uint16_t t_angle, int t_interval) {
    static long double stepCount = degToStep(t_angle);

    // reset function state if direction changes
    if (reset) {
        stepCount = degToStep(t_angle);
        resetFun(false);
    }

    // chrono
    if (motorStepChrono.hasPassed(t_interval)) {
        motorStepChrono.restart();

        // decreasing steps
        if (stepCount > 0) {
            Motor::driveMotor();
            stepCount--;
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