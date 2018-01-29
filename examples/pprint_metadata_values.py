#!/usr/bin/env python3

import klvdata
import pprint

if __name__ == "__main__":
	with open('./data/DynamicConstantMISMMSPacketData.bin', 'rb') as f:
		for packet in klvdata.StreamParser(f):
			metadata=packet.MetadataList()
			pprint.pprint(metadata)
