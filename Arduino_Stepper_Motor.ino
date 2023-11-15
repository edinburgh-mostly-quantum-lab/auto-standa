#include "Chrono.h"

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

// variables
int motorMode = 1;
int motorDirection = LOW;
bool motorState = 0;
bool ledState = 0;
float revolutions = 2.5;
uint16_t fullRev = 12800;
uint64_t stepNum = fullRev * revolutions;
double degNum = 360;

// init Chrono objects for time keeping
Chrono ledChrono;
Chrono motorConstChrono(Chrono::MICROS);
Chrono motorAccChrono(Chrono::MICROS);
Chrono motorStepChrono(Chrono::MICROS);

void setup() {
    // Serial.begin(115200);           // init serial for communication with board
    pinMode(LED_BUILTIN, OUTPUT);   // init serial for communication with board
    pinMode(DIR_PIN, OUTPUT);       // enable pin to control motor direction
    pinMode(STEP_PIN, OUTPUT);      // enable pin to control motor steps

    digitalWrite(DIR_PIN, motorDirection);
    digitalWrite(LED_BUILTIN, ledState);
}

void loop() {
    // motorConst(50);
    // motorAcc(50, 500);
    motorStep(degToStep(degNum), 50);
    // LED(1000);
}

void LED(int duration) {
    if (ledChrono.hasPassed(duration)) {
        ledChrono.restart();
        ledState = 1 - ledState;
        digitalWrite(LED_BUILTIN, ledState);
    }
}

void driveMotor() {
    motorState = 1 - motorState;
    digitalWrite(STEP_PIN, motorState);
}

void motorConst(int duration) {
    if (motorConstChrono.hasPassed(duration)) {
        motorConstChrono.restart();

        driveMotor();        
    }
}

void motorAcc(int minDuration, int maxDuration) {
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

uint64_t degToStep(uint16_t deg) {
    uint64_t steps = (fullRev * deg) / 360;
    return steps;
}

void motorStep(uint64_t steps, int duration) {
    static uint64_t stepCount = steps;
    // static uint64_t stepCount = (fullRev * deg) / 360;
    if (motorStepChrono.hasPassed(duration)) {
        motorStepChrono.restart();

        // decreasing steps
        if (stepCount > 0) {
            driveMotor();
            stepCount--;
        }
    }
}