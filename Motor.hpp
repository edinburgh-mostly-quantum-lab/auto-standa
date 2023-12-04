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
        void motorConst(int t_interval);
        void motorAcc(int t_minInterval, int t_maxInterval);
        void motorAngle(uint16_t t_angle, int t_interval);
        void resetFun(bool t_state);

    private:
        bool reset = false;

    private:
        uint64_t degToStep(int t_deg);
};