#!/usr/bin/env python

import klvdata

if __name__ == "__main__":
with open('./data/DynamicConstantMISMMSPacketData.bin', 'rb') as f:
	for packet in klvdata.StreamParser(f):
		packet.structure()
