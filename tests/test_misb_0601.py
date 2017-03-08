#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2017 Matthew Pare (paretech@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

import unittest
from common import hexstr_to_bytes


class ParserSingleShort(unittest.TestCase):
    def test_checksum(self):
        # From MISB ST0902.5
        interpretation = "0xAA43"
        tlv_hex_bytes = hexstr_to_bytes("01 02 AA 43")
        value = tlv_hex_bytes[2:]

        from misb0601 import Checksum
        self.assertEquals(str(Checksum(value).value), interpretation)
        self.assertEquals(bytes(Checksum(value)), tlv_hex_bytes)

    def test_precisiontimestamp(self):
        # From MISB ST0902.5
        interpretation = "2009-01-12 22:08:22+00:00"
        tlv_hex_bytes = hexstr_to_bytes("02 08 00 04 60 50 58 4E 01 80")
        value = tlv_hex_bytes[2:]

        from misb0601 import PrecisionTimeStamp
        self.assertEquals(str(PrecisionTimeStamp(value).value), interpretation)
        self.assertEquals(bytes(PrecisionTimeStamp(value)), tlv_hex_bytes)

        # From MISB ST0601.9
        interpretation = "2008-10-24 00:13:29.913000+00:00"
        tlv_hex_bytes = hexstr_to_bytes("02 08 00 04 59 F4 A6 AA 4A A8")
        value = tlv_hex_bytes[2:]

        from misb0601 import PrecisionTimeStamp
        self.assertEquals(str(PrecisionTimeStamp(value).value), interpretation)
        self.assertEquals(bytes(PrecisionTimeStamp(value)), tlv_hex_bytes)

    def test_MissionID(self):
        # From MISB ST0902.5
        interpretation = "Mission 12"
        tlv_hex_bytes = hexstr_to_bytes("03 0A 4D 69 73 73 69 6F 6E 20 31 32")
        value = tlv_hex_bytes[2:]

        from misb0601 import MissionID
        self.assertEquals(str(MissionID(value).value), interpretation)
        self.assertEquals(bytes(MissionID(value)), tlv_hex_bytes)

        # From MISB ST0601.9
        interpretation = "MISSION01"
        tlv_hex_bytes = hexstr_to_bytes("03 09 4D 49 53 53 49 4F 4E 30 31]")
        value = tlv_hex_bytes[2:]

        from misb0601 import MissionID
        self.assertEquals(str(MissionID(value).value), interpretation)
        self.assertEquals(bytes(MissionID(value)), tlv_hex_bytes)

    def test_PlatformTailNumber(self):
        # From MISB ST0601.9
        interpretation = "AF-101"
        tlv_hex_bytes = hexstr_to_bytes("04 06 41 46 2D 31 30 31")
        value = tlv_hex_bytes[2:]

        from misb0601 import PlatformTailNumber
        self.assertEquals(str(PlatformTailNumber(value).value), interpretation)
        self.assertEquals(bytes(PlatformTailNumber(value)), tlv_hex_bytes)

    def test_PlatformHeadingAngle(self):

        # From MISB ST0601.9
        # @TODO: Limit display precision and add units as per example.
        interpretation = "159.97436484321355"
        tlv_hex_bytes = hexstr_to_bytes("05 02 71 C2")
        value = tlv_hex_bytes[2:]

        from misb0601 import PlatformHeadingAngle
        self.assertEquals(str(PlatformHeadingAngle(value).value), interpretation)
        self.assertEquals(bytes(PlatformHeadingAngle(value)), tlv_hex_bytes)
        self.assertAlmostEquals(float(PlatformHeadingAngle(value).value), 159.974, 3)

    def test_PlatformPitchAngle(self):

        # From MISB ST0601.9
        # @TODO: Limit display precision and add units as per example.
        interpretation = "-0.4315317239905987"
        tlv_hex_bytes = hexstr_to_bytes("06 02 FD 3D")
        value = tlv_hex_bytes[2:]

        from misb0601 import PlatformPitchAngle
        self.assertEquals(str(PlatformPitchAngle(value).value), interpretation)
        self.assertEquals(bytes(PlatformPitchAngle(value)), tlv_hex_bytes)
        self.assertAlmostEquals(float(PlatformPitchAngle(value).value), -0.4315, 4)



if __name__ == '__main__':
    unittest.main()
