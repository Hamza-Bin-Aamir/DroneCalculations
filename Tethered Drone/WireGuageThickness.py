import argparse
import atexit

# CONSTANTS

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

def FindGuageA(RequiredAmps: int):
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

def FindGuage(RequiredAmps: int, MaxVoltageDrop: float):
    """
        Finds the lowest guage that will support our required amps while maintaining our voltage drop parameters
        RequiredAmps: How many amps will the system on average be supporting (don't use instantaneous amperage, only average)
        returns: A tuple (str, float) that contains the (guage, thickness)
    """
    Minimum: str = "NA"

    for Guage, Properties in AWG_LUT.items():
        if Properties[0] >= RequiredAmps:
            if Minimum == "NA":
                if GetVoltageDrop(args.current, args.distance, Properties[1]) <= MaxVoltageDrop:
                    Minimum = Guage
                else:
                    return ("NA", -1)
            elif Properties[1] < AWG_LUT[Minimum][1]:
                if GetVoltageDrop(args.current, args.distance, Properties[1]) <= MaxVoltageDrop:
                    Minimum = Guage
    
    if Minimum == "NA":
        return ("NA", -1)
    
    return Minimum, AWG_LUT[Minimum][1]


# GLOBAL VARS

Issues = []

parser = argparse.ArgumentParser(prog="Wire Guage Thickness Calculator", description="Calculates the required wire guage for our drone.")
op_mode = parser.add_argument_group("OPERATION MODE", "The method used by the requirement calculator")
op_mode.add_argument("-o", "--op-mode", type=str, default="weight", help="Should we prioritise voltage drop or wire weight")
op_mode.add_argument("-v", "--verbosity", type=int, default=4, help="How \"talkative\" should the program be.")

elec_prop = parser.add_argument_group("ELECTRICAL PROPERTIES", "The physical specifications of the system.")
elec_prop.add_argument("-I", "--current", type=float, help="The maximum load that the system will carry. Unit: Amperes")
elec_prop.add_argument("-l", "--load", type=float, help="The hover load (as a percentage of maximum load). Unit: %age of max load")
elec_prop.add_argument("-V", "--voltage", type=float, help="The maximum allowable voltage drop. Unit: Volts")

dimensions = parser.add_argument_group("DIMENSIONS", "The physical dimensions of the wire.")
dimensions.add_argument("-d", "--distance", type=float, help="The distance (in meters) the wire must cover. Unit: Meters")
dimensions.add_argument("-g", "--guage", type=str, help="The guage of the wire. Unit: AWG")

args = parser.parse_args()

if args.op_mode == "weight":
    if not args.current:
        Issues.append("MISSING ARGUMENT: '--current' or '-I' -- You must specify the maximum current of the system. Unit: Amperes")
    if not args.load:
        Issues.append("MISSING ARGUMENT: '--load' or '-l' -- You must specify how much load the system has on hover. Unit: %age of max load")
    if not args.distance:
        Issues.append("MISSING ARGUMENT: '--distance' or '-d' -- You must specify how long the wire is. Unit: Meters")
elif args.op_mode == "voltage":
    if not args.current:
        Issues.append("MISSING ARGUMENT: '--current' or '-I' -- You must specify the maximum current of the system. Unit: Amperes")
    if not args.load:
        Issues.append("MISSING ARGUMENT: '--load' or '-l' -- You must specify how much load the system has on hover. Unit: %age of max load")
    if not args.distance:
        Issues.append("MISSING ARGUMENT: '--distance' or '-d' -- You must specify how long the wire is. Unit: Meters")
    if not args.voltage:
        Issues.append("MISSING ARGUMENT: '--voltage' or '-V' -- You must specify the maximum allowable voltage drop. Unit: Volts")
else:
    Issues.append("INVALID OPERATION MODE: '--op-mode' or '-o' can only have the values: 'weight' or 'voltage'")

if Issues:
    if args.verbosity > 0:
        parser.print_help()

        print(RED)
        for Issue in Issues:
            print(Issue)
        print(RESET)

        exit(-1)
    else:
        exit(-1)
    
if args.op_mode == "weight":
    ActualCurrent = args.current*min(1,(args.load+(SAFETY_MARGIN_CURRENT*args.load)))
    print(YELLOW + "Calculating minimum wire guage...")
    MinGuage, GuageThickness = FindGuageA(ActualCurrent)

    print("Calculating resultant voltage drop...")
    VoltageDrop = GetVoltageDrop(args.current, args.distance, GuageThickness)
    print("Calculating the weight of the wire...")
    Weight = CU_DENSITY * GuageThickness * args.distance
    print(RESET)

    if args.verbosity > 3:
        print(GREEN)
        print("\t***** DESIGN PARAMETERS *****")
        print("Estimated Required Current Draw:\t", round(ActualCurrent,2), "A", sep=None)
        print("Minimum Guage of the Wire:\t\t", MinGuage, "AWG", sep=None)
        print(f"Guage Thickness:\t\t\t {GuageThickness:.2e}", "m^2", sep=None)
        print("Voltage Drop:\t\t\t\t", round(VoltageDrop,2), "V", sep=None)
        print("Weight of the Wire:\t\t\t", round(Weight,2), "kg", sep=None)
        print("\t*****************************")
        print(RESET)
    elif args.verbosity > 2:
        print("DESIGN PARAMETERS")
        print("Estimated Required Current Draw:", round(ActualCurrent,2), "A", sep=None)
        print("Minimum Guage of the Wire:", MinGuage, "AWG", sep=None)
        print(f"Guage Thickness: {GuageThickness:.2e}", "m^2", sep=None)
        print("Voltage Drop:", round(VoltageDrop,2), "V", sep=None)
        print("Weight of the Wire:", round(Weight,2), "kg", sep=None)
    elif args.verbosity > 1:
        print(f"Guage: {MinGuage}AWG")
        print(f"Voltage Drop: {VoltageDrop:.2f}V")
        print(f"Weight: {Weight:.2f}kg")
    elif args.verbosity > 0:
        print(f"G: {MinGuage}AWG")
        print(f"V: {VoltageDrop:.2f}V")
        print(f"W: {Weight:.2f}kg")
    else:
        print(f"{MinGuage}")
        print(f"{VoltageDrop:.2f}")
        print(f"{Weight:.2f}")

else:
    ActualCurrent = args.current*min(1,(args.load+(SAFETY_MARGIN_CURRENT*args.load)))
    print(YELLOW + "Calculating minimum wire guage (based on voltage)...")
    MinGuage, GuageThickness = FindGuage(ActualCurrent, args.voltage)

    print("Calculating resultant voltage drop...")
    VoltageDrop = GetVoltageDrop(args.current, args.distance, GuageThickness)
    print("Calculating the weight of the wire...")
    Weight = CU_DENSITY * GuageThickness * args.distance
    print(RESET)

    if args.verbosity > 3:
        print(GREEN)
        print("\t***** DESIGN PARAMETERS *****")
        print("Estimated Required Current Draw:\t", round(ActualCurrent,2), "A", sep=None)
        print("Minimum Guage of the Wire:\t\t", MinGuage, "AWG", sep=None)
        print(f"Guage Thickness:\t\t\t {GuageThickness:.2e}", "m^2", sep=None)
        print("Voltage Drop:\t\t\t\t", round(VoltageDrop,2), "V", sep=None)
        print("Weight of the Wire:\t\t\t", round(Weight,2), "kg", sep=None)
        print("\t*****************************")
        print(RESET)
    elif args.verbosity > 2:
        print("DESIGN PARAMETERS")
        print("Estimated Required Current Draw:", round(ActualCurrent,2), "A", sep=None)
        print("Minimum Guage of the Wire:", MinGuage, "AWG", sep=None)
        print(f"Guage Thickness: {GuageThickness:.2e}", "m^2", sep=None)
        print("Voltage Drop:", round(VoltageDrop,2), "V", sep=None)
        print("Weight of the Wire:", round(Weight,2), "kg", sep=None)
    elif args.verbosity > 1:
        print(f"Guage: {MinGuage}AWG")
        print(f"Voltage Drop: {VoltageDrop:.2f}V")
        print(f"Weight: {Weight:.2f}kg")
    elif args.verbosity > 0:
        print(f"G: {MinGuage}AWG")
        print(f"V: {VoltageDrop:.2f}V")
        print(f"W: {Weight:.2f}kg")
    else:
        print(f"{MinGuage}")
        print(f"{VoltageDrop:.2f}")
        print(f"{Weight:.2f}")