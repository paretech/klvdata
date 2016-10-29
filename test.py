#!/usr/bin/env python3

# Copyright 2016 Matthew Pare. All rights reserved.

import st0601
import pdb
import sys
from pprint import pprint
from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = 'DynamicConstantMISMMSPacketData_modified.bin'

    with open(f, 'rb') as f:
        for packet in st0601.TestParser(f, 16):
            for tag, value in packet.get_items():
                print(value)
