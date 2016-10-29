#!/usr/bin/env python3

# Copyright 2016 Matthew Pare. All rights reserved.

import sys
import struct
import io
import warnings

# TODO: Keep as iter but return more useful object...
class BaseParser(object):

    """Base class for parsing Key Length Value (KLV) structured binary data.

    """

    def __init__(self, source, size):
        if isinstance(source, io.IOBase):
            instream = source
        else:
            instream = io.BytesIO(source)

        if getattr(instream, 'read', None) is None:
            raise TypeError('Parser must be a stream like object, not ' '{itype}'.format(itype=instream.__class__.__name__))

        self.s = instream
        self.size = size

    def __iter__(self):
        self.packet_count = 0

        return self

    def __next__(self):
        self.parse()

        # TODO: How about you return a BaseElement?
        return self

    def parse(self):
        self.raw = bytearray()
        self.packet_count += 1

        self.key = self.read(self.size)

        # TODO: Set length as the original bytes
        # TODO: Turns out for debugging it is good not to over write this value
        #       never know when you need to know how many bytes are about to be
        #       read...
        self.length = struct.unpack('>B', self.read(1))[0]

        # TODO: Use method to convert self.length from BER bytes to int length
        if self.length > 127:
            self.length = int.from_bytes(self.read(self.length & 0x7F), 'big')

        self.value = self.read(self.length)

    def read(self, size):
        if size == 0:
            warnings.warn("0 length read requested", UserWarning)

        data = self.s.read(size)

        if not data:
            raise StopIteration

        self.raw += data

        return data

class BaseElement:
    def __init__(self, item):
        self.key = self._bytes_to_int(item.key)
        self.length = item.length
        self.value = self.converter(item)


    def converter(self, item):
        self.name = 'Unknown Tag Name'

        self.unit = ''

        return item.value

    def _scale_value(self, min_value, max_value, value, signed=False):
        value_range = max_value - min_value

        int_range = 2**(len(value) * 8) - 1

        return value_range/int_range * self._bytes_to_int(value, signed)

    @staticmethod
    def _bytes_to_int(value, signed=False):
        return int.from_bytes(value, byteorder='big', signed=signed)

    @staticmethod
    def _bytes_to_str(value):
        return value.decode('UTF-8')

    def __str__(self):
        return "{:2}: '{}' ({} bytes) \"{}\"".format(self.key, self.name, self.length, self.value)


def calc_checksum(data):
    length = len(data) - 2
    wordsize, mod = divmod(length, 2)

    words = sum(struct.unpack(">{:d}H".format(wordsize), data[0:length-mod]))

    if mod:
        words += data[length-1] << 8

    return struct.pack('>H', words & 0xFFFF)

# Previously named "pretty_print"
def bytes2hexdump(value):
    return " ".join(["{:02X}".format(byte) for byte in value])

