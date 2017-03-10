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
# SOFTWARE.

import unittest


class BERLength(unittest.TestCase):
    def test_ber_decode_encode(self):
        from common import ber_decode
        from common import ber_encode

        # BER Short Form
        self.assertEquals(ber_encode(ber_decode(b'\x00')), b'\x00')
        self.assertEquals(ber_encode(ber_decode(b'\x01')), b'\x01')
        self.assertEquals(ber_encode(ber_decode(b'\x08')), b'\x08')
        self.assertEquals(ber_encode(ber_decode(b'\x7F')), b'\x7F')

        # BER Long Form
        self.assertEquals(ber_encode(ber_decode(b'\x81\x80')), b'\x81\x80')
        self.assertEquals(ber_encode(ber_decode(b'\x81\xFF')), b'\x81\xFF')
        self.assertEquals(ber_encode(ber_decode(b'\x82\xFF\xFF')), b'\x82\xFF\xFF')
        self.assertEquals(ber_encode(ber_decode(b'\x83\xFF\xFF\xFF')), b'\x83\xFF\xFF\xFF')

        # BER encode using the fewest possible bytes
        self.assertEquals(ber_encode(ber_decode(b'\x80')), b'\x00')
        self.assertEquals(ber_encode(ber_decode(b'\x81\x00')), b'\x00')
        self.assertEquals(ber_encode(ber_decode(b'\x81\x01')), b'\x01')
        self.assertEquals(ber_encode(ber_decode(b'\x81\x7F')), b'\x7F')

    def test_ber_encode_decode(self):
        from common import ber_decode
        from common import ber_encode
        self.assertEquals(ber_decode(ber_encode(0)), 0)
        self.assertEquals(ber_decode(ber_encode(1)), 1)
        self.assertEquals(ber_decode(ber_encode(8)), 8)
        self.assertEquals(ber_decode(ber_encode(127)), 127)
        self.assertEquals(ber_decode(ber_encode(128)), 128)
        self.assertEquals(ber_decode(ber_encode(254)), 254)
        self.assertEquals(ber_decode(ber_encode(255)), 255)
        self.assertEquals(ber_decode(ber_encode(256)), 256)
        self.assertEquals(ber_decode(ber_encode(900)), 900)
        self.assertEquals(ber_decode(ber_encode(9000)), 9000)
        self.assertEquals(ber_decode(ber_encode(90000)), 90000)
        self.assertEquals(ber_decode(ber_encode(900000)), 900000)

    def test_ber_decode_error(self):
        from common import ber_decode

        with self.assertRaises(ValueError):
            ber_decode(b'\x00\x00')

        with self.assertRaises(ValueError):
            ber_decode(b'\x00\x08')

        with self.assertRaises(ValueError):
            ber_decode(b'\x80\x00')

        with self.assertRaises(ValueError):
            ber_decode(b'\x81')

        with self.assertRaises(ValueError):
            ber_decode(b'\x82\xFF')

