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


class ParserSingleShort(unittest.TestCase):
    # def test_security_timestamp(self):
    #     key = b'\x02'
    #     length = b'\x08'
    #     value = b'\x00\x04\x60\x50\x58\x4E\x01\x80'
    #     klv = self.key + self.length + self.value
    #
    #     from misb0601 import PrecisionTimeStamp
    #     self.element = PrecisionTimeStamp(self.value)

    def test_st0102(self):
        # Test parameters from MISB ST0902.5 Annex C for "Dynamic and Constant" MISMMS Packet Data
        key = b'\x30'
        length = b'\x1c'
        value = b'\x01\x01\x01\x02\x01\x07\x03\x05//USA\x0c\x01\x07\r\x06\x00U\x00S\x00A\x16\x02\x00\n'
        klv = key + length + value

        from misb0102 import ST0102

        # Basic Properties
        self.assertEquals(ST0102(value).key, key)
        self.assertEquals(ST0102(value).length, length)
        self.assertEquals(ST0102(value).value, value)
        self.assertEquals(bytes(ST0102(value)), klv)

        # Specific to value under test
        self.assertEquals(len(ST0102(value).items()), 6)

    def test_st0601(self):
        key = b'\x06\x0e+4\x02\x0b\x01\x01\x0e\x01\x03\x01\x01\x00\x00\x00'
        length = b'\x1e'
        value = b'0\x1c\x01\x01\x01\x02\x01\x07\x03\x05//USA\x0c\x01\x07\r\x06\x00U\x00S\x00A\x16\x02\x00\n'
        klv = key + length + value

        from misb0601 import ST0601

        # Basic Properties
        self.assertEquals(ST0601(value).key, key)
        self.assertEquals(ST0601(value).length, length)
        self.assertEquals(ST0601(value).value, value)
        self.assertEquals(bytes(ST0601(value)), klv)

if __name__ == '__main__':
    unittest.main()
