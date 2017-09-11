#!/usr/bin/env python

import sys
import klvdata

if __name__ == "__main__":
	for packet in klvdata.StreamParser(sys.stdin.buffer.read()):
		packet.structure()
