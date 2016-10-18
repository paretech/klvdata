#!/usr/bin/env python3

import klvcms
import pdb
from pprint import pprint

if __name__ == '__main__':
    with open('DynamicConstantMISMMSPacketData.bin', 'rb') as f:
        for packet in klvcms.TestParser(f, 16):
            packet.print_tags()


