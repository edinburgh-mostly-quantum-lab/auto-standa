#include "Arduino.h"
#include "digitalWriteFast.h"
// https://www.arduino.cc/reference/en/libraries/digitalwritefast/

class Motor {
    public:
        int motorMode;
        int motorDirection = LOW;
        bool motorState = 0;
        uint64_t fullRevStep;

        int a;
        int b;
        int c;
        
    public:
        Motor(uint64_t t_fullRevStep);
        void driveMotor();
        void motor(int motorMode, int a = 0, int b = 0, int c = 0);
        void motorChangeDir();
        void motorConst(int t_interval);
        void motorAcc(int t_minInterval, int t_maxInterval);
        void motorStep(uint16_t t_angle, int t_count, int t_interval);
        void resetFun(bool t_state);

    private:
        bool reset = false;

    private:
        uint64_t degToStep(int t_deg);
};