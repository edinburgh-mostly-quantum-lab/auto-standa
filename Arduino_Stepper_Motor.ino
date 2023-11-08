// RS Pro 5350401 Motor
// step angle: 0.9°

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

// init LED control variables
// bool enableLED = false;
// bool enableFlash = false;

// init motor control variables
// int motorMode = 1;
int motorDirection = LOW;
// bool reset;

// void templateFunction(int duration) {
//     // time keeping to enable multitasking, change millis() to micros() for microsecond timing
//     static unsigned long chrono = millis();
//     if (millis() - chrono < duration) return;
//     chrono = millis();
//     // main function body here //
// }

void motorNew(int motorMode, int maxDuration, unsigned long optional = 0);

void setup() {
    Serial.begin(115200);           // init serial for communication with board
    pinMode(LED_BUILTIN, OUTPUT);   // enable built-in LED
    pinMode(DIR_PIN, OUTPUT);       // enable pin to control motor direction
    pinMode(STEP_PIN, OUTPUT);      // enable pin to control motor steps

    digitalWrite(DIR_PIN, motorDirection);

    // Serial.println(
    //     "Select option:\n"
    //     "1. Toggle LED on\n"
    //     "2. Toggle LED flash\n"
    //     "3. Turn off motor\n"
    //     "4. Toggle motor direction\n"
    //     "5. Enable motor: constant velocity\n"
    //     "6. Enable motor: accelerate\n"
    //     "7. Enable motor: step"
    // );
}

void loop() {
    // reset = false;
    // if (Serial.available()) {
    //     userInput();
    // }

    // LED(1000); // if LED and flash enabled, LED will flash every second
    // motor(45,200);

    // motorNew(2,500,45);
    motorNew(3, 100, 1200);
}

void motorNew(int motorMode, int maxDuration, unsigned long optional) {
    // time keeping
    static unsigned long duration = maxDuration;
    static unsigned long chrono = micros();
    if (micros() - chrono < duration) return;
    chrono = micros();

    static int motorState = HIGH;

    switch (motorMode)
    {
    case 1: // constant speed
        motorState = 1 - motorState;
        digitalWrite(STEP_PIN, motorState);
        break;

    case 2: // accelerating
        static int cycle = 200;
        static int minDuration = optional;
        // int minDuration = optional;

        if (cycle <= 0) {
            cycle = 200;
            if (duration > minDuration && duration % 2 = 0) {
                duration--;
            }
        }
        cycle--;

        motorState = 1 - motorState;
        digitalWrite(STEP_PIN, motorState);
        break;

    case 3: // step
        static int initStep = optional;
        static int stepCount = optional;

        // Serial.println(stepCount);

        if (stepCount <= 0) {
            // Serial.println("Steps complete");
            motorMode = 0;
        }
        else {
            if (motorState) {
                stepCount--;
            }

            motorState = 1 - motorState;
            digitalWrite(STEP_PIN, motorState);
        }
        break;
    
    
    default:
        motorState = LOW;
        digitalWrite(STEP_PIN, motorState);
        break;
    }

    // digitalWrite(STEP_PIN, motorState);
    // Serial.println(duration);
}

// void motor(int minDuration, int maxDuration) {
//     // takes microseconds for input
//     static unsigned long duration = maxDuration;
//     if (reset) {
//         duration = maxDuration;
//     }
//     else if (motorMode >= 1 && motorMode <= 3) {
//         static int motorState = HIGH;
//         static int cycle = 200; // cycle resets and duration decreases when cycle = 0

//         // time keeping
//         static unsigned long chrono = micros();
//         if (micros() - chrono < duration) return;
//         chrono = micros();

//         // alternate between LOW and HIGH for driving motor
//         motorState = 1 - motorState;

//         if (motorMode == 2) { // acceleration mode
//             cycle--;
//             if (cycle <= 0) {
//                 cycle = 200;
//                 if (duration > minDuration) {
//                     duration--;
//                 }
//             }
//         }
//         digitalWrite(STEP_PIN, motorState);
//     }
// }


// void userInput() {
//     int option = Serial.parseInt();
//     switch (option)
//     {
//     case 1: // toggle LED
//         enableLED = !enableLED;
//         Serial << "LED state: " << enableLED << '\n';
//         break;

//     case 2: // toggle LED flash
//         enableFlash = !enableFlash;
//         Serial << "Flash state: " << enableFlash << '\n';
//         break;

//     case 3: // toggle motor
//         motorMode = 0;
//         Serial << "Motor state: " << motorMode << '\n';
//         break;

//     case 4: // toggle motor direction
//         // reset motor cycles and retain motorMode value
//         reset = true;
//         switch (motorMode)
//         {
//         case 1:
//             option = 5;
//             break;
//         case 2:
//             option = 6;
//             break;
//         default:
//             break;
//         }

//         // alternate between LOW and HIGH for motor direction
//         motorDirection = 1 - motorDirection;
//         digitalWrite(DIR_PIN, motorDirection);

//         Serial << "Motor direction: " << motorDirection << '\n';
//         break;

//     case 5: // motor with constant velocity
//         motorMode = 1;
//         Serial << "Motor state: " << motorMode << '\n';
//         break;

//     case 6: // motor with accelerating velocity
//         reset = true;
//         motorMode = 2;
//         Serial << "Motor state: " << motorMode << '\n';
//         break;

//     default:
//         Serial.println("Error: Please enter a valid input");
//     }
// }

// void LED(int duration) {
//     // takes milliseconds for input
//     static int ledState = HIGH;
//     if (enableLED) {
//         if (enableFlash) {
//             // time keeping
//             static unsigned long chrono = millis();
//             if (millis() - chrono < duration) return;
//             chrono = millis();

//             // alternate between LOW and HIGH for enabling LED
//             ledState = 1 - ledState;
//         }
//         else {
//             ledState = HIGH;
//         }
//     }
//     else {
//         ledState = LOW; // turns off LED if enableLED == flase
//     }
//     digitalWrite(LED_BUILTIN, ledState);
// }