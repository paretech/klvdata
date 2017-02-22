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
        x1 = -(2 ** (length * 8 - 1) - 1)
        x2 = +(2 ** (length * 8 - 1) - 1)
    else:
        x1 = 0
        x2 = +(2 ** (length * 8) - 1)

    y1, y2 = minimum, maximum

    m = (y2 - y1) / (x2 - x1)

    x = bytes_to_int(value, signed)

    return m * (x - x1) + y1  # Return y


def float_to_bytes(value, length, minimum, maximum, signed=True):
    """Convert the fixed point value self.value to a floating point value."""
    if signed:
        x1 = -(2 ** (length * 8 - 1) - 1)
        x2 = +(2 ** (length * 8 - 1) - 1)
    else:
        x1 = 0
        x2 = +(2 ** (length * 8) - 1)

    y1, y2 = minimum, maximum

    m = (y2 - y1) / (x2 - x1)

    y = value

    return int_to_bytes((1 / m) * (y - y1) + x1, length)  # Return x


def calc_checksum(data):
    length = len(data) - 2
    word_size, mod = divmod(length, 2)

    words = sum(struct.unpack(">{:d}H".format(word_size), data[0:length - mod]))

    if mod:
        words += data[length - 1] << 8

    return struct.pack('>H', words & 0xFFFF)