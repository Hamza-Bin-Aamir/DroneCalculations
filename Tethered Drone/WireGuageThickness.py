import argparse

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
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

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
            if Minimum == "NA" | Properties[1] < AWG_LUT[Minimum][1]:
                Minimum = Guage
    
    if Minimum == "NA":
        return ("NA", -1)
    
    return Minimum, AWG_LUT[Minimum][1]


# GLOBAL VARS

Issues = []

parser = argparse.ArgumentParser(prog="Wire Guage Thickness Calculator", description="Calculates the required wire guage for our drone.")
op_mode = parser.add_argument_group("OPERATION MODE", "The method used by the requirement calculator")
op_mode.add_argument("-o", "--op-mode", type=str, default="weight", help="Should we prioritise voltage drop or wire weight")
op_mode.add_argument("-v", "--verbosity", type=int, default="4", help="How \"talkative\" should the program be.")

elec_prop = parser.add_argument_group("ELECTRICAL PROPERTIES", "The physical specifications of the system.")
elec_prop.add_argument("-I", "--current", type=float, help="The maximum load that the system will carry.")
elec_prop.add_argument("-l", "--load", type=float, help="The hover load (as a percentage of maximum load).")
elec_prop.add_argument("-V", "--voltage", type=float, help="The maximum allowable voltage drop.")

dimensions = parser.add_argument_group("DIMENSIONS", "The physical dimensions of the wire.")
dimensions.add_argument("-d", "--distance", type=float, help="The distance (in meters) the wire must cover.")
dimensions.add_argument("-g", "--guage", type=str, help="The guage of the wire (AWG).")

args = parser.parse_args()

if args.op_mode == "weight":
    if not args.current:
        Issues.append("MISSING ARGUMENT: '--current' or '-I' -- You must specify the maximum current of the system.")
    if not args.load:
        Issues.append("MISSING ARGUMENT: '--load' or '-l' -- You must specify how much load the system has on hover (%age of max load).")
    if not args.distance:
        Issues.append("MISSING ARGUMENT: '--distance' or '-d' -- You must specify how long the wire is.")
elif args.op_mode == "voltage":
    if not args.current:
        Issues.append("MISSING ARGUMENT: '--current' or '-I' -- You must specify the maximum current of the system.")
    if not args.load:
        Issues.append("MISSING ARGUMENT: '--load' or '-l' -- You must specify how much load the system has on hover (%age of max load).")
    if not args.distance:
        Issues.append("MISSING ARGUMENT: '--distance' or '-d' -- You must specify how long the wire is.")
    if not args.voltage:
        Issues.append("MISSING ARGUMENT: '--voltage' or '-V' -- You must specify the maximum allowable voltage drop.")
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
    
