#include "Arduino.h"

// map pins to pin numbers on board
#define DIR_PIN 2
#define STEP_PIN 3
#define MS3_PIN 8
#define MS2_PIN 9
#define MS1_PIN 10
#define EN_PIN 12

class Motor {
    public:
        int motorMode;
        int motorDirection = LOW;
        bool motorState = 0;
        uint64_t fullRevStep;

    public:
        Motor(uint64_t t_fullRevStep);
        void motorChangeDir();
        void motorFullStep(int t_deg);
        void motorHalfStep(int t_deg);
        void motorQuarterStep(int t_deg);
        void motorEighthStep(int t_deg);
        void motorSixteenthStep(int t_deg);

        void initPins();
        void resetPins();

    private:
        void driveMotor();
        uint64_t degToStep(int t_deg);
};