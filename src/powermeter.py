from ThorlabsPM100 import ThorlabsPM100, USBTMC
import dataclasses
import typing

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
    try:
        if powermeter.port:
            print("Power meter connected at port:", powermeter.port)
        else:
            print("Power meter not found")
        print("Reference power:", powermeter.ref_power, "W")
        powermeter.current_power = powermeter.powermeter.read
        print("Power:", powermeter.current_power, "W")
    except:
        pass

def set_ref_power(powermeter: PowerMeter):
    powermeter.ref_power = Power(powermeter.powermeter.read)