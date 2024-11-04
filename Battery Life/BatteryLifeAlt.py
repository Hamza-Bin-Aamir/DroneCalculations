import atexit

YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

atexit.register(print, RESET)

print(YELLOW + "*** MOTOR PARAMETERS ***")
MotorCount = int(input("Please specify the number of motors: "))
MotorAmp = float(input("Please specify the amperage of each motor (A): "))
MotorLoad = float(input("Please specify the %age load at which the motor hovers: ")); MotorLoad /= 100
print("*** BATTERY PARAMETERS ***")
BatteryCapacitymAh = int(input("Please enter the capacity of your battery (mAh): "))
BatteryCapacityAh = BatteryCapacitymAh/1000

print(GREEN + "YOUR BATTERY WILL LAST YOU " + YELLOW + f" {(BatteryCapacityAh/(MotorAmp*MotorCount*MotorLoad)):.2f} HOURS" + GREEN + ".")