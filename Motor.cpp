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
    case 0:
        motorState = LOW;
        digitalWrite(STEP_PIN, motorState);
        break;

    case 1:
        motorConst(50);
    break;

    case 2:
        motorAcc(50, 500);
        break;

    case 3:
        motorStep(degToStep(degNum), 50);
        break;
    
    default:
        Serial.println("Error: Invalid mode for motor");
        break;
    }
}

void Motor::motorConst(int duration) {
    if (motorConstChrono.hasPassed(duration)) {
        motorConstChrono.restart();

        driveMotor();        
    }
}

void Motor::motorAcc(int minDuration, int maxDuration) {
    static int duration = maxDuration;
    static int cycleAcc = 200;
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
    if (motorStepChrono.hasPassed(duration)) {
        motorStepChrono.restart();

        // decreasing steps
        if (stepCount > 0) {
            Motor::driveMotor();
            stepCount--;
        }
        else if (stepCount == 0) {
            motorMode = 0;
        }
        
    }
}

void Motor::motorRevs(int revolutions) {
    
}

void Motor::reset() {

}