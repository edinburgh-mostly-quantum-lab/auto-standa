import os
import time
import dataclasses
import typing
import json
import libximc.highlevel as ximc
from ThorlabsPM100 import ThorlabsPM100, USBTMC

def clear() -> None:
    if os.name == 'nt':
        _ = os.system("cls")
    else:
        _ = os.system("clear")

Angle = typing.NewType("Angle", int)
Step = typing.NewType("Step", int)
NoiseDB = typing.NewType("NoiseDB", float)

@dataclasses.dataclass
class Motor:
    full_step: Step
    port: str = None
    motor: ximc.Axis = None
    current_step: Step = None
    current_angle: Angle = None
    current_noise: NoiseDB = None
    noise_map: "list[dict[NoiseDB:Step]]" = None

@dataclasses.dataclass
class PowerMeter:
    port: str
    powermeter: ThorlabsPM100
    current_power: str = None

menu_dict = {
    "0": "Set zero point",
    "1": "Rotate motor by angle",
    "2": "Rotate motor by step",
    "3": "Calibrate noise map",
    "Q": "Quit"
}

def connect_motor() -> Motor:
    port_num = 0
    while True:
        port = '/dev/ttyACM' + str(port_num)
        motor = Motor(
            full_step = 28800,
            port = port,
            motor = ximc.Axis('xi-com:' + port),
        )
        try:
            motor.motor.open_device()
            motor.motor.get_status()
            motor.motor.close_device()
        except:
            port_num += 1
        else:
            break
    return motor

def connect_power_meter() -> PowerMeter:
    port_num = 0
    while True:
        port = '/dev/usbtmc' + str(port_num)
        try:
            inst = USBTMC(device=port)     
        except:
            port_num += 1
        else:
            break
    powermeter = PowerMeter(
        port = port,
        powermeter = ThorlabsPM100(inst=inst)
    )
    return powermeter

def angle_to_step(angle: Angle, full_step: Step) -> Step:
    step = int(angle / 360 * full_step)
    return step

def step_to_angle(step: Step, full_step: Step) -> Angle:
    angle = int(step / full_step * 360)
    return angle

def get_motor_status(motor: Motor) -> None:
    motor.motor.open_device()
    motor.current_step = motor.motor.get_status().CurPosition
    motor.current_angle = step_to_angle(step=motor.current_step, full_step=motor.full_step)
    motor.motor.close_device()

def print_motor_status(motor: Motor) -> None:
    get_motor_status(motor=motor)
    print("Standa motor ready")
    print("Port:", motor.port)
    print("Current angle:", motor.current_angle)
    print("Current step:", motor.current_step)
    print("Estimated noise level:", motor.current_noise)

def print_power_meter_status(powermeter: PowerMeter) -> None:
    print("Power meter ready")
    print("Port:", powermeter.port)
    powermeter.current_power = powermeter.powermeter.read
    print("Power:", powermeter.current_power, "W")

def step_motor(motor: Motor, step: Step) -> None:
    moving = ''
    motor.motor.open_device()
    motor.motor.command_movr(step, 0)
    time.sleep(0.5)
    while moving != 'MoveState.0':
        moving = str(motor.motor.get_status().MoveSts)
    motor.motor.close_device()
    print("Motor operation complete")

def main() -> None:
    while True:
        clear()
        motor = connect_motor()
        print_motor_status(motor=motor)
        powermeter = connect_power_meter()
        print_power_meter_status(powermeter=powermeter)
        print("Select option:")
        for key, value in menu_dict.items():
            print(key + ")", value)
        user_input = input()

        if user_input.lower() == 'q':
            break

        option = int(user_input)
        while option == 1 or option == 2:
            clear()
            print_motor_status(motor=motor)
            user_input = input("Selected option: " + menu_dict.get(str(option)) + "\nEnter number or q to return to previous menu: ")
            if user_input.lower() == 'q':
                option = 0
                break
            try:
                step = int(user_input)
            except:
                print("Invalid input")
            else:
                if option == 1:
                    step = angle_to_step(angle=step, full_step=motor.full_step)
                step_motor(motor=motor, step=step)

if '__main__' == __name__:
    main()