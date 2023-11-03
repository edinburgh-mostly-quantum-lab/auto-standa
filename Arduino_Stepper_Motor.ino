int userInput;
bool enableLED;
bool enableFlash;


void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);

    Serial.println(
        "Select option:\n"
        "1. LED on\n"
        "2. LED off\n"
        "3. LED mode: steady\n"
        "4. LED mode: flash"
    );
}

void loop() {
    if (Serial.available()) {
        userInput = Serial.parseInt();
        switch (userInput)
        {
        case 1:
            enableLED = 1;
            break;
        case 2:
            enableLED = 0;
            break;
        case 3:
            enableFlash = 0;
            break;
        case 4:
            enableFlash = 1;
            break;
        default:
            Serial.println("Error: Please enter a valid input");
        }
    }
    LED(1000);
}

void LED(unsigned long duration) {
    static unsigned long chrono = millis();
    if (millis() - chrono < duration) return;
    chrono = millis();

    static int ledState = LOW;

    if (enableLED == 1) {
        if (enableFlash == 1) {
            if (ledState == HIGH) {
                ledState = LOW;
            }
            else {
                ledState = HIGH;
            }
        } 
        else{
            ledState = HIGH;
        }
    }
    else {
        ledState = LOW;
    }
    digitalWrite(LED_BUILTIN, ledState);
}