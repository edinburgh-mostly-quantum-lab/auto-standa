import libximc.highlevel as ximc
import dataclasses
import typing
import math
import json
import os

from powermeter import *

Angle = typing.NewType("Angle", int)
Step = typing.NewType("Step", int)
NoiseDB = typing.NewType("NoiseDB", float)
Power = typing.NewType("Power", float)

@dataclasses.dataclass
class Noise:
    angle: Angle
    power: Power
    noise: NoiseDB

@dataclasses.dataclass
class Motor:
    full_step: Step
    port: str = None
    motor: ximc.Axis = None
    current_step: Step = None
    current_angle: Angle = None
    current_noise: NoiseDB = None
    noise_map: typing.List[Noise] = None

class dataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def connect_motor() -> Motor:
    for port_num in range(0,11):
        if os.name == 'nt':
            port = r'\\.\COM' + str(port_num)
        else:
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
            motor = Motor(
            full_step = 28800,
            port = None,
            motor = None,
        )
        else:
            get_motor_status(motor=motor)
    return motor

def angle_to_step(angle: Angle, full_step: Step) -> Step:
    step = Step(angle / 360 * full_step)
    return step

def step_to_angle(step: Step, full_step: Step) -> Angle:
    angle = Angle(step / full_step * 360)
    return angle

def get_motor_status(motor: Motor) -> None:
    try:
        motor.motor.open_device()
        position = motor.motor.get_status().CurPosition
        if position < 0:
            position = motor.full_step + position
        if position > motor.full_step:
            position = position - motor.full_step
        motor.current_step = position
        motor.current_angle = step_to_angle(step=motor.current_step, full_step=motor.full_step)
        motor.motor.close_device()
    except:
        pass

def set_zero_point(motor: Motor) -> None:
    try:
        motor.motor.open_device()
        motor.motor.command_zero()
        motor.motor.close_device()
    except:
        pass
    else:
        get_motor_status(motor=motor)

def print_motor_status(motor: Motor) -> None:
    if motor.current_step == motor.full_step:
            set_zero_point(motor=motor)
    if motor.port:
        print("Standa motor connected at port:", motor.port)
    else:
        print("Standa motor not found")
    print("Current angle:", motor.current_angle)
    print("Current step:", motor.current_step, "/", motor.full_step)
    try:
        motor.noise_map = get_noise_map()
    except:
        print("No calibration file found")
    else:
        print("Calibration file found")
    print("Estimated noise level:", motor.current_noise)

def step_motor(motor: Motor, step: Step) -> None:
    try:
        motor.motor.open_device()
        motor.motor.command_movr(int(step), 0)
        motor.motor.command_wait_for_stop(refresh_interval_ms=10)
        motor.motor.close_device()
    except:
        pass
    else:
        get_motor_status(motor=motor)

def rotate_to_angle(motor: Motor, target_angle: Angle = 0) -> None:
    try:
        target_step = angle_to_step(angle=target_angle, full_step=motor.full_step)
        step_delta = target_step - motor.current_step
        step_delta = (step_delta + motor.full_step/2) % motor.full_step - motor.full_step/2
        step_motor(motor=motor, step=step_delta)
    except:
        pass

def rotate_to_noise(motor: Motor, target_noise: Noise) -> None:
    target_angle = min(range(len(motor.noise_map)), key=lambda i: abs(motor.noise_map[i]["noise"] - target_noise))
    rotate_to_angle(motor=motor, target_angle=target_angle)

def calc_noise_level(ref_power: Power, current_power: Power) -> NoiseDB:
    try:
        noise = NoiseDB(-10 * math.log10(current_power/ref_power))
    except:
        noise = None
    return noise

def calibrate_noise_map(ref_power: Power, motor: Motor, powermeter: PowerMeter) -> typing.List[Noise]:
    rotate_to_angle(motor=motor)
    step = angle_to_step(angle=1, full_step=motor.full_step)
    noise_map = typing.List[Noise]
    for i in range(0, 360):
        current_power = powermeter.powermeter.read
        noise_map.append(Noise(
            angle=i,
            power=current_power,
            noise=calc_noise_level(ref_power=ref_power, current_power=current_power)
        ))
        step_motor(motor=motor, step=step)

    noise_map = noise_map[:next((i for i, d in enumerate(noise_map[1:], start=1) if d['noise'] < noise_map[i - 1]['noise']), len(noise_map))]
    
    with open("calibration.json", "w") as file:
        json.dump(noise_map, file, cls=dataclassJSONEncoder, indent=4)
    return noise_map

def get_noise_map() -> typing.List[Noise]:
    with open("calibration.json", "r") as file:
        data = list(json.load(file))
    return data
