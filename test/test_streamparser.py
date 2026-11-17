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


class ParserSingleLong(unittest.TestCase):
    def test_singlepacket(self):

        # Example from MISB ST 0902.5
        with open('./data/DynamicConstantMISMMSPacketData.bin', 'rb') as f:
            packet = f.read()

        from klvdata.streamparser import StreamParser
        from klvdata import misb0601
        from klvdata import misb0102

        for packet in StreamParser(packet):
            # packet.structure()
            pass


class ChecksumVerify(unittest.TestCase):
    """MISB ST 0601 Item 1 checksum (issue #58)."""

    def setUp(self):
        with open('./data/DynamicOnlyMISMMSPacketData.bin', 'rb') as f:
            self.good = f.read()
        # Its checksum item still says 0xAA43; the content sums to 0x3E1E.
        with open('./data/DynamicConstantMISMMSPacketData.bin', 'rb') as f:
            self.stale = f.read()

    def parse(self, data, **kwargs):
        from klvdata.streamparser import StreamParser
        from klvdata import misb0601
        return list(StreamParser(data, **kwargs))

    def test_checksum_valid(self):
        good, = self.parse(self.good)
        stale, = self.parse(self.stale)
        self.assertTrue(good.checksum_valid())
        self.assertFalse(stale.checksum_valid())

    def test_default_does_not_verify(self):
        self.assertEqual(len(self.parse(self.stale + self.good)), 2)

    def test_verify_skips_bad_packets(self):
        flipped = bytearray(self.good)
        flipped[40] ^= 0x01
        with self.assertWarns(UserWarning):
            packets = self.parse(self.stale + bytes(flipped) + self.good, verify_checksum=True)
        self.assertEqual(len(packets), 1)
        self.assertEqual(bytes(packets[0]), self.good)

    def test_verify_uses_length_as_received(self):
        # Same packet with a long-form BER length (0x81 0x61 instead of 0x61).
        from klvdata.common import packet_checksum
        value = self.good[17:]
        packet = self.good[:16] + b'\x81' + bytes([len(value)]) + value[:-2]
        packet += packet_checksum(packet + b'\x00\x00')
        self.assertEqual(len(self.parse(packet, verify_checksum=True)), 1)


if __name__ == "__main__":
    unittest.main()
