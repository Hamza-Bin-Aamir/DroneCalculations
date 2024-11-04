import atexit
#  CONSTANTS

AWG_LUT = {
    "000"   : (200, 8.5e-5), # Current (A), Thickness (m^2)
    "0"     : (150, 5.35e-5),
    "3"     : (100, 2.67e-5),
    "6"     : (55, 1.33e-5),
    "8"     : (40, 8.37e-6),
    "10"    : (30, 5.26e-6),
    "12"    : (20, 3.31e-6),
    "14"    : (15, 2.08e-6),
}
CU_RESISTIVITY = 1.724e-8 # Ω*m
CU_DENSITY = 8960 # kg/m^3
SAFETY_MARGIN_CURRENT = 0.5
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

atexit.register(print, RESET)

# FUNCTION DEFS

def FindGuage(RequiredAmps: int):
    """
        Finds the lowest guage that will support our required amps
        RequiredAmps: How many amps will the system on average be supporting (don't use instantaneous amperage, only average)
        returns: A tuple (str, float) that contains the (guage, thickness)
    """

    Minimum: str = "NA"

    for Guage, Properties in AWG_LUT.items():
        if Properties[0] >= RequiredAmps:
            if Minimum == "NA":
                Minimum = Guage
            elif Properties[1] < AWG_LUT[Minimum][1]:
                Minimum = Guage
    
    if Minimum == "NA":
        return ("NA", -1)
    
    return Minimum, AWG_LUT[Minimum][1]

def GetVoltageDrop(current:float, distance:float, thickness:float):
    return 2 * current * distance * CU_RESISTIVITY / thickness

print(YELLOW)
print("***OPERATIONAL PARAMETERS***")
NumMotors   = int(input("Please specify the number of motors: "))
MotorAmps   = float(input("Please specify the maximum amperage of the motor: "))
MotorVoltage= float(input("Please specify the operating voltage of the motor: "))

print("***DIMENSIONAL PARAMETERS***")
WeightOfDrone = float(input("Please specify the weight of the drone (kg): "))
WireLength = float(input("Please specify the length of the wire (m): "))

MinGuage, GuageThickness = FindGuage(MotorAmps*NumMotors)
VoltageDrop = GetVoltageDrop(MotorAmps*NumMotors, WireLength, GuageThickness)
Weight = CU_DENSITY* GuageThickness * WireLength

print(RESET + GREEN)

print("***REPORT***")
print(f"The range of the drone is {YELLOW}{WireLength/2:.2f}m{GREEN}.")
print(f"The total weight of the drone will be {YELLOW}{Weight+WeightOfDrone:.2f}kg{GREEN}.")
print(f"The voltage required will be {YELLOW}{MotorVoltage+VoltageDrop:.2f}V{GREEN}.")
print(f"The wire guage requirement is {YELLOW}{MinGuage}{GREEN}.")

print(RESET)