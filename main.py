from pathlib import Path
import os
import argparse
import time
from anyNoteCLI import CLI

parser = argparse.ArgumentParser(description='parser', prog="anyNote")
parser.add_argument('command', nargs = '+', help='anynote command: init, remote ...')
parser.add_argument("-r","--read", type=ascii, help='read')
parser.add_argument("-t","--traverse", help='traverse hiarchy tree', action="store_true")
#parser.add_argument("-w","--write", help='write',action="store_true")
#parser.add_argument("-rep","--replace", help='replace',action="store_true")
#parser.add_argument("-ev","--edit_vim", help='edit vim',action="store_true")
#parser.add_argument("-en","--edit_nano", help='edit nano',action="store_true")
args = parser.parse_args()
arg_dict = vars(args)
#print(args)
CLI(arg_dict.pop('command'), arg_dict)