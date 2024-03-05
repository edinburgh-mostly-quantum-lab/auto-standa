# AUTO-STANDA

## USAGE
The command "auto-standa" takes an argument that will be used as a target noise level in dB\
The command passes this argument to a python script, that attempts to rotate the standa motor to the target noise level by comparing the target to a list of known noise levels and angles found in calibration.json

## EXAMPLE
`auto-standa 5`\
This will:
- change directory ~/.local/auto-standa
- execute auto-standa.py using a python virtual environment found in this directory
- the python script rotates the motor to 5 dB
