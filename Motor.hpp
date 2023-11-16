#include "Arduino.h"

class Motor {
    public:
        int motorMode;
        int motorDirection = LOW;
        bool motorState = 0;
        uint64_t fullRev;
        uint64_t stepNum = (uint64_t) fullRev;
        int degNum = (int) 360;
        
    public:
        Motor(uint64_t x);
        void driveMotor();
        void motor(int motorMode);
        void motorConst(int duration);
        void motorAcc(int minDuration, int maxDuration);
        void motorStep(uint64_t steps, int duration);
        void motorRevs(int revolutions);
        void reset();

    private:
        uint64_t degToStep(int deg);
};