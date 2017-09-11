#!/usr/bin/env python
import sys, klvdata;
for packet in klvdata.StreamParser(sys.stdin.buffer.read()): packet.structure()

# python -c "import sys; import klvdata; for packet in klvdata.StreamParser(sys.stdin.buffer.read()): packet.structure()"
