from ThorlabsPM100 import ThorlabsPM100, USBTMC
import dataclasses
import typing

from standamotor import *

Power = typing.NewType("Power", float)

@dataclasses.dataclass
class PowerMeter:
    port: str
    powermeter: ThorlabsPM100
    current_power: Power = None
    ref_power: Power = None

def connect_power_meter() -> PowerMeter:
    for port_num in range(0,11):
        port = '/dev/usbtmc' + str(port_num)
        try:
            inst = USBTMC(device=port)
            powermeter = PowerMeter(
                port = port,
                powermeter = ThorlabsPM100(inst=inst)
            )
        except:
            powermeter = PowerMeter(
                port = None,
                powermeter = None
            )
        else:
            break
    return powermeter

def print_power_meter_status(powermeter: PowerMeter) -> None:
    if powermeter.port:
        print("Power meter connected at port:", powermeter.port)
        print("Reference power:", powermeter.ref_power, "W")
        powermeter.current_power = powermeter.powermeter.read
        print("Power:", powermeter.current_power, "W")
    else:
        print("Power meter not found")

def set_ref_power(powermeter: PowerMeter):
    powermeter.ref_power = Power(powermeter.powermeter.read)

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