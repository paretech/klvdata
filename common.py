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

def bytes_to_int(value, signed=False):
    """Return integer given bytes."""
    return int.from_bytes(bytes(value), byteorder='big', signed=signed)


def int_to_bytes(value, length=1, signed=False):
    """Return bytes given integer"""
    return int(value).to_bytes(length, byteorder='big', signed=signed)


def ber_decode(length):
    """Return decoded BER length as integer given bytes."""
    if bytes_to_int(length) < 128:
        # BER Short Form
        return bytes_to_int(length)
    else:
        # BER Long Form
        return bytes_to_int(length[1:])


def ber_encode(length):
    """Return encoded BER length as bytes given integer."""
    if length < 128:
        # BER Short Form
        return int_to_bytes(length)
    else:
        # BER Long Form
        byte_length = ((length.bit_length() - 1) // 8) + 1

        return int_to_bytes(byte_length + 128) + int_to_bytes(length, length=byte_length)
