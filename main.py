import os

from standamotor import *
from powermeter import *

def clear() -> None:
    if os.name == 'nt':
        _ = os.system("cls")
    else:
        _ = os.system("clear")

menu_dict = {
    "0": "Set zero point",
    "1": "Rotate motor by angle",
    "2": "Rotate motor by step",
    "3": "Rotate to angle",
    "4": "Rotate to noise level",
    "5": "Return to zero",
    "8": "Measure reference power",
    "9": "Calibrate noise map",
    "R": "Refresh",
    "Q": "Quit"
}

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
        if user_input.lower() == 'r':
            pass
        else:
            try:
                option = int(user_input)
            except:
                print("Invalid input")
        
            if option == 0:
                set_zero_point(motor=motor)
                option = -1

            while option >= 1 and option <= 3:
                clear()
                print_motor_status(motor=motor)
                user_input = input("Selected option: " + menu_dict.get(str(option)) + "\nEnter number or q to return to previous menu: ")
                if user_input.lower() == 'q':
                    option = -1
                    break
                try:
                    step = int(user_input)
                except:
                    print("Invalid input")
                else:
                    if option == 1:
                        step = angle_to_step(angle=step, full_step=motor.full_step)
                    if option == 3:
                        rotate_to_angle(motor=motor, target_angle=step)
                    step_motor(motor=motor, step=step)

            if option == 5:
                rotate_to_angle(motor=motor)

            if option == 8:
                set_ref_power(powermeter=powermeter)

            if option == 9:
                calibrate_noise_map(ref_power=powermeter.ref_power, motor=motor, powermeter=powermeter)

if '__main__' == __name__:
    main()