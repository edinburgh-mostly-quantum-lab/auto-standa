#include "Arduino.h"
#include "digitalWriteFast.h"
// https://www.arduino.cc/reference/en/libraries/digitalwritefast/

class Motor {
    public:
        int motorMode;
        int motorDirection = LOW;
        bool motorState = 0;
        uint64_t fullRev;
        
    public:
        Motor(uint64_t x);
        void driveMotor();
        void motor(int motorMode);
        void motorChangeDir();
        void motorConst(int t_interval);
        void motorAcc(int t_minInterval, int t_maxInterval);
        void motorAngle(uint16_t t_angle, int t_rotations, int t_interval);
        void motorSatSweep(int t_seconds);
        void motorCalibrate();
        void resetFun(bool t_state);

    private:
        bool reset = false;

    private:
        uint64_t degToStep(int t_deg);
};