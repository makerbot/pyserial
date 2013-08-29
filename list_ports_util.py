import argparse
import sys

import serial.tools.list_ports as lp

arg_parser = argparse.ArgumentParser(
        'Calls serial.tools.list_ports.list_ports_by_vid_pid()')

arg_parser.add_argument(
    '--vid',
    '-v',
    action='store',
    default='23C1',
    help="The VID in hex")

arg_parser.add_argument(
    '--pid',
    '-p',
    action='store',
    default=None,
    help="The PID in hex")

args = sys.argv[1:]
arguments = arg_parser.parse_args(args)

vid = int('0x' + arguments.vid, 16)
pid = int('0x' + arguments.pid, 16) if None != arguments.pid else None

print list(lp.list_ports_by_vid_pid(vid, pid))