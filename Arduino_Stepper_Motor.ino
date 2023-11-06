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

int userInput;

// init LED control variables
bool enableLED;
bool enableFlash;

// init motor control variables
bool enableMotor = false;
int motorDirection = LOW;

// void templateFunction(int duration) {
//     // time keeping to enable multitasking, change millis() to micros() for microsecond timing
//     static unsigned long chrono = millis();
//     if (millis() - chrono < duration) return;
//     chrono = millis();
//     // main function body here //
// }

void setup() {
    Serial.begin(115200);           // init serial for communication with board
    pinMode(LED_BUILTIN, OUTPUT);   // enable built-in LED
    pinMode(DIR_PIN, OUTPUT);       // enable pin to control motor direction
    pinMode(STEP_PIN, OUTPUT);      // enable pin to control motor steps

    digitalWrite(DIR_PIN, motorDirection);

    Serial.println(
        "Select option:\n"
        "1. Toggle LED on\n"
        "2. Toggle LED flash\n"
        "3. Toggle motor direction\n"
        "4. Toggle motor"
    );
}

void loop() {
    if (Serial.available()) {
        userInput = Serial.parseInt();
        switch (userInput)
        {
        case 1: // toggle LED
            if (enableLED == true) {
                enableLED = false;
            }
            else {
                enableLED = true;
            }
            break;
        case 2: // toggle LED flash
            if (enableFlash == true) {
                enableFlash = false;
            }
            else {
                enableFlash = true;
            }
            break;
        case 3: // toggle motor direction
            if (motorDirection == LOW) {
                motorDirection = HIGH;
            }
            else {
                motorDirection = LOW;
            }
            break;
        case 4: // toggle motor
            if (enableMotor == true) {
                enableMotor = false;
            }
            else {
                enableMotor = true;
            }
            break;
        default:
            Serial.println("Error: Please enter a valid input");
        }
    }

    LED(1000); // if LED and flash enabled, LED will flash every second
    // motorAngle(10);
    // motorAcc(20,100);
    digitalWrite(DIR_PIN, motorDirection);
    motor(45);
}

void LED(int duration) {
    // takes milliseconds for input
    static int ledState = HIGH;
    {
        if (enableLED == true) {

            if (enableFlash == true) {
                // time keeping
                static unsigned long chrono = millis();
                if (millis() - chrono < duration) return;
                chrono = millis();

                if (ledState == HIGH) {
                    ledState = LOW;
                }
                else {
                    ledState = HIGH;
                }
            }
            else {
                ledState = HIGH;
            }
        }
        else {
            ledState = LOW; // turns off LED if enableLED == flase
        }
        digitalWrite(LED_BUILTIN, ledState);
    }
}

void motorDir() {

}

void motor(int duration) {
    // takes microseconds for input
    if (enableMotor == true) {
        static int motorState = HIGH;

        // time keeping
        static unsigned long chrono = micros();
        if (micros() - chrono < duration) return;
        chrono = micros();

        // alternate between LOW and HIGH for driving motor
        if (motorState == HIGH) {
            motorState = LOW;
        }
        else {
            motorState = HIGH;
        }
        digitalWrite(STEP_PIN, motorState);
    }
}

void motorAcc(int minDuration, int maxDuration) {
    // takes microseconds for input
    if (enableMotor == true) {
        static int motorState = HIGH;
        static int cycle = 200; // cycle resets and duration decreases when cycle = 0

        static unsigned long duration = maxDuration;

        // time keeping
        static unsigned long chrono = micros();
        if (micros() - chrono < duration) return;
        chrono = micros();

        // alternate between LOW and HIGH for driving motor
        if (motorState == HIGH) {
            motorState = LOW;
        }
        else {
            motorState = HIGH;

            cycle--;
            if (cycle <= 0 ) {
                cycle = 200;
                if (duration > minDuration) {
                    duration--;
                }
            }
        }
        digitalWrite(STEP_PIN, motorState);
    }
}