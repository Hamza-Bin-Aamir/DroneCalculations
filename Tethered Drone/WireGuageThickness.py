import argparse

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
CuResistivity = 1.724e-8 # Ω*m
CuDensity = 8960 # kg/m^3

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

