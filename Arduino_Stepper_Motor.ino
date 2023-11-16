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
int motorMode;
int motorDirection = LOW;
bool motorState = 0;
bool ledState = 0;
float revolutions = 5.0;
uint64_t fullRev = 12750;
uint64_t stepNum = (uint64_t) fullRev * revolutions;
int degNum = (int) 360 * revolutions;
bool serial = true;
bool showMenu = true;
bool reset = false;

// init Chrono objects for time keeping
Chrono ledChrono;
Chrono motorConstChrono(Chrono::MICROS);
Chrono motorAccChrono(Chrono::MICROS);
Chrono motorStepChrono(Chrono::MICROS);

void setup() {
    // if (serial) {
        Serial.begin(115200); // init serial for communication with board
        delay(1);
    // }

    pinMode(LED_BUILTIN, OUTPUT);   // init serial for communication with board
    pinMode(DIR_PIN, OUTPUT);       // enable pin to control motor direction
    pinMode(STEP_PIN, OUTPUT);      // enable pin to control motor steps

    digitalWrite(DIR_PIN, motorDirection);
    digitalWrite(LED_BUILTIN, ledState);

    Serial.println(
        "Select option:\n"
        "1. Turn off motor\n"
        "2. Toggle motor direction\n"
        "3. Enable motor: constant velocity\n"
        "4. Enable motor: accelerate\n"
        "5. Enable motor: step"
    );
}

void loop() {
    reset = false;
    if (Serial.available()) {
        int option = Serial.parseInt();
        switch (option)
        {
        case 1:
            motorMode = 0;
            break;

        case 2:
            motorDirection = 1 - motorDirection;
            digitalWrite(DIR_PIN, motorDirection);
            Serial << "Motor direction: " << motorDirection << '\n';
            break;

        case 3:
            motorMode = 1;
            break;

        case 4:
            motorMode = 2;
            break;

        case 5:
            motorMode = 3;
            break;
        
        default:
            Serial.println("Error: Invalid input");
            break;
        }
    }
    motor(motorMode);
}

void LED(int duration) {
    if (ledChrono.hasPassed(duration)) {
        ledChrono.restart();
        ledState = 1 - ledState; // flip state
        digitalWrite(LED_BUILTIN, ledState);
    }
}

// class Motor() {
//     public:
//     void driveMotor()
//     private:
// }

void driveMotor() {
    motorState = 1 - motorState; // flip state
    digitalWrite(STEP_PIN, motorState);
}

void motor(int motorMode) {
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

uint64_t degToStep(int deg) {
    uint64_t steps = (fullRev * deg) / 360;
    return steps;
}

void motorStep(uint64_t steps, int duration) {
    static long double stepCount = steps;
    if (motorStepChrono.hasPassed(duration)) {
        motorStepChrono.restart();

        // decreasing steps
        if (stepCount > 0) {
            driveMotor();
            stepCount--;
        }
        else if (stepCount == 0) {
            motorMode = 0;
        }
        
    }
}