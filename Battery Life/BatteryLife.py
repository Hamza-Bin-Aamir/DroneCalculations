import argparse
import atexit

YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

atexit.register(print, RESET)

ArgumentParser = argparse.ArgumentParser()
OperationMode = ArgumentParser.add_argument_group("Operation Mode", "Parameters that define how the program will behave.")
OperationMode.add_argument("-v", "--verbosity", default=1, help="How detailed should the program be when printing.")

MotorParameters = ArgumentParser.add_argument_group("Motor Parameters", "Parameters that define the motor's specifications.")
MotorParameters.add_argument("-n", "--motor-count", "--num-motors", type=int, help="Number of motors on the drone.")
MotorParameters.add_argument("-A", "--motor-amps", type=float, help="Amps per motor.")
MotorParameters.add_argument("-l", "--hover-load", type=float, help="The load on the motor at hover (percentage of total amps).")

BatteryParameters = ArgumentParser.add_argument_group("Battery Parameters", "Parameters that define the battery's specifications.")
BatteryParameters.add_argument("-c", "--capacity", type=int, help="Battery capacity in milliAmpereHours")

Arguments = ArgumentParser.parse_args()

Issues = []

0 if Arguments.motor_count else Issues.append("MOTOR COUNT CANNOT BE BLANK (-n or --motor-count).")
0 if Arguments.motor_amps else Issues.append("MOTOR AMPERAGE CANNOT BE BLANK (-A or --motor-amps).")
0 if Arguments.motor_amps else Issues.append("MOTOR LOAD CANNOT BE BLANK (-l or --hover-load)")
0 if Arguments.capacity else Issues.append("BATTERY CAPACITY CANNOT BE BLANK (-c or --capacity)")

if Issues:
    ArgumentParser.print_help()
    print(RED)
    for Issue in Issues:
        print(Issue)
    exit(-1)

CapacityAh = Arguments.capacity / 1000
LoadPercentage = Arguments.hover_load / 100

HourTime = CapacityAh / (Arguments.motor_amps * Arguments.motor_count * LoadPercentage)

print(GREEN + "YOUR BATTERY WILL LAST YOU " + YELLOW + f" {HourTime:.2f} HOURS" + GREEN + ".") if Arguments.verbosity > 1 else 0
print(f"FLIGHT TIME: {HourTime} HOURS") if Arguments.verbosity == 1 else 0
print(f"HourTime") if Arguments.verbosity == 0 else 0