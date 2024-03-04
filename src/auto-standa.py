import sys
import standamotor

data = sys.argv[1]

motor = standamotor.connect_motor()
target_noise = float(data)
standamotor.rotate_to_noise(motor=motor, target_noise=target_noise)
