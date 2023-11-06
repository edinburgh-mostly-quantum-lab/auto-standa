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

    Serial.println(
        "Select option:\n"
        "1. LED on\n"
        "2. LED off\n"
        "3. LED mode: steady\n"
        "4. LED mode: flash\n"
        "5. Motor on\n"
        "6. Motor off\n"
        "7. Motor direction: clockwise\n"
        "8. Motor direction: counter-clockwise"
    );
}

void loop() {
    if (Serial.available()) {
        userInput = Serial.parseInt();
        switch (userInput)
        {
        case 1:
            enableLED = true;
            break;
        case 2:
            enableLED = false;
            break;
        case 3:
            enableFlash = false;
            break;
        case 4:
            enableFlash = true;
            break;
        case 5:
            enableMotor = true;
            break;
        case 6:
            enableMotor = false;
            break;
        case 7:
            motorDirection = LOW;   // clockwise
            break;
        case 8:
            motorDirection = HIGH;  // counter-clockwise
            break;
        default:
            Serial.println("Error: Please enter a valid input");
        }
    }

    LED(1000); // if LED and flash enabled, LED will flash every second
    // motor(45); // rotate motor every 45 microseconds
    motorAcc(130,200);
}

void LED(int duration) {
    // takes milliseconds for input
    static int ledState = LOW;
    if (enableLED == true) {
        static unsigned long chrono = millis();
        if (millis() - chrono < duration) return;
        chrono = millis();
    
        if (enableFlash == true) {     // enable flashing LED
            if (ledState == HIGH) {
                ledState = LOW;
            }
            else {
                ledState = HIGH;
            }
        } 
        else{
            ledState = HIGH;        // enable LED
        }
    }
    else {
        ledState = LOW;             // disable LED
    }
    digitalWrite(LED_BUILTIN, ledState);
}

void motor(int duration) {
    // takes microseconds for input
    if (enableMotor == true) {
        static bool high = true;

        digitalWrite(DIR_PIN, motorDirection);

        static unsigned long chrono = micros();
        if (micros() - chrono < duration) return;
        chrono = micros();


        if (high == true) {
            digitalWrite(STEP_PIN, HIGH);
            high = false;
        }
        else {
            digitalWrite(STEP_PIN, LOW);
            high = true;
        }
    }
}

void motorAcc(int minDuration, int maxDuration) {
    // takes microseconds for input
    if (enableMotor == true) {
        static bool high = true; // alternated between HIGH and LOW for driving motor
        static int cycle = 200; // cycle resets and duration decreases when cycle = 0

        digitalWrite(DIR_PIN, motorDirection);

        static unsigned long duration = maxDuration;

        // time keeping
        static unsigned long chrono = micros();
        if (micros() - chrono < duration) return;
        chrono = micros();

        if (high == true) {
            digitalWrite(STEP_PIN, HIGH);
            high = false;
        }
        else {
            digitalWrite(STEP_PIN, LOW);
            high = true;

            cycle--;
            if (cycle <= 0 ) {
                cycle = 200;
                Serial << "duration: " << duration << '\n';
                if (duration > minDuration) {
                    duration--;
                }
            }
        }
    }
}