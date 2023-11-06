// map pins to pin numbers on board
#define DIR_PIN 2
#define STEP_PIN 3

int userInput;

// init LED control variables
bool enableLED;
bool enableFlash;

// init motor control variables
bool enableMotor = true;
int motorDirection = LOW;

// void templateFunction(unsigned long duration) {
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
    motor(45); // rotate motor every 45 microseconds
}

void LED(unsigned long duration) {
    // takes milliseconds for input
    static unsigned long chrono = millis();
    if (millis() - chrono < duration) return;
    chrono = millis();

    static int ledState = LOW;

    if (enableLED == true) {
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

void motor(unsigned long duration) {
    // takes microseconds for input
    static unsigned long chrono = micros();
    if (micros() - chrono < duration) return;
    chrono = micros();

    if (enableMotor == true) {
        digitalWrite(DIR_PIN, motorDirection);

        digitalWrite(STEP_PIN, LOW);
        digitalWrite(STEP_PIN, HIGH);
    }
}