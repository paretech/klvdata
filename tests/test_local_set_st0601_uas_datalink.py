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


class LocalSetUAS(unittest.TestCase):
    pass


class ParserSingleShort(LocalSetUAS):
    def setUp(self):
        self.key = b'\x02'
        self.length = b'\x08'
        self.value = b'\x00\x04\x60\x50\x58\x4E\x01\x80'

        self.packet = self.key + self.length + self.value

        from misb_0601 import PrecisionTimeStamp
        self.element = PrecisionTimeStamp(self.value)

    def test_key(self):
        self.assertEquals(self.element.key, self.key)

    def test_ber_length(self):
        from common import ber_decode
        from common import ber_encode
        self.assertEquals(ber_encode(ber_decode(self.length)), self.length)

    def test_length(self):
        self.assertEquals(self.element.length, self.length)

    def test_value(self):
        self.assertEquals(self.element.value, self.value)

    def test_bytes(self):
        self.assertEquals(bytes(self.element), self.packet)

    def test_modify_value(self):
        from datetime import datetime
        from struct import pack

        time = pack('>Q', int(datetime.utcnow().timestamp()*1e6))

        self.packet = self.key + self.length + time
        self.element.value = time

        self.assertEquals(bytes(self.element), self.packet)

    def test_display(self):
        print(repr(self.element))
        print(self.element)

if __name__ == '__main__':
    unittest.main()
