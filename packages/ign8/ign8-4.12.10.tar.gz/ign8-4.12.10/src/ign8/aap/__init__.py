from . import aap
import argparse

def main():
    parser = argparse.ArgumentParser(description="ignite automation on Redhat AAP", usage="ign8_aap <action> \n\n \
               \
               version : 0.0.1 aap  \n                                              \
               actions:\n                                                      \
               status        status on aap \n  \
               \
               2024 ign8.it\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "status":
        aap.status()
