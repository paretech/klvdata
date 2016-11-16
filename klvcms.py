#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Matthew Pare (paretech@gmail.com)
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

import struct
import warnings

from collections import OrderedDict

# TODO: make _IterParser and Parser classes
class Parser(object):
    """Base class for parsing Key Length Value (KLV) structured binary data.
    """

    def __init__(self, source, key_length=16):
        self.source = source
        self.key_length = key_length

    def __iter__(self):
        return self

    def __next__(self):
        self.key = bytes_to_int(self.__read(self.key_length))

        first_length_octet = self.__read(1)

        self.length = bytes_to_int(first_length_octet)

        if self.length > 127:
            additional_bytes = self.length & 0x7F
            remaining_length_octets = self.__read(additional_bytes)
            self.length = bytes_to_int(remaining_length_octets)

        self.value = self.__read(self.length)

        return self

    def __read(self, size):
        if size == 0:
            warnings.warn("0 length read requested", UserWarning)

            return None

        data = self.source.read(size)

        if not data:
            raise StopIteration

        return data

def bytes_to_int(value, signed=False):
    return int.from_bytes(bytes(value), byteorder='big', signed=signed)

def int_to_bytes(value, length, signed=False):
    return int(value).to_bytes(length, byteorder='big', signed=signed)

def bytes_to_str(value):
    return bytes(value).decode('UTF-8')

def str_to_bytes(value):
    return bytes(str(value), 'UTF-8')

def bytes_to_hex_dump(value):
    return " ".join(["{:02X}".format(byte) for byte in bytes(value)])

def bytes_to_float(value, minimum, maximum, signed=True):
    """Convert the fixed point value self.value to a floating point value."""
    length = len(bytes(value))

    if signed:
        x1 = -(2**(length * 8 - 1) - 1)
        x2 = +(2**(length * 8 - 1) - 1)
    else:
        x1 = 0
        x2 = +(2**(length * 8) - 1)

    y1, y2 = minimum, maximum

    m = (y2 - y1) / (x2 - x1)

    x = bytes_to_int(value, signed)

    return m*(x - x1) + y1 # Return y

def float_to_bytes(value, length, minimum, maximum, signed=True):
    """Convert the fixed point value self.value to a floating point value."""
    if signed:
        x1 = -(2**(length * 8 - 1) - 1)
        x2 = +(2**(length * 8 - 1) - 1)
    else:
        x1 = 0
        x2 = +(2**(length * 8) - 1)

    y1, y2 = minimum, maximum

    m = (y2 - y1) / (x2 - x1)

    y = value

    return int_to_bytes((1/m) * (y - y1) + x1, length) # Return x

def calc_checksum(data):
    length = len(data) - 2
    wordsize, mod = divmod(length, 2)

    words = sum(struct.unpack(">{:d}H".format(wordsize), data[0:length-mod]))

    if mod:
        words += data[length-1] << 8

    return struct.pack('>H', words & 0xFFFF)

