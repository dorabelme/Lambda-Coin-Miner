#!/usr/bin/env python3

"""Main."""

import sys
import os
from cpu import *

# os.system('python ls8.py')

if len(sys.argv) == 2:  # CPU file + file to be ran
    cpu = CPU()
    cpu.load(sys.argv[1])
    cpu.run()
else:
    print('Error: Please provide filename to execute instructions')
    sys.exit(1)
