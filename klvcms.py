#!/usr/bin/env python3

import sys
import struct
import pdb
import io
from datetime import datetime
import time
import warnings

from collections import OrderedDict, defaultdict
from pprint import pprint

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

        return self

    def parse(self):
        self.raw = bytearray()
        self.packet_count += 1

        self.key = self.read(self.size)

        # TODO: Set length as the original bytes
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
        self.key = bytes2int(item.key)
        self.length = item.length
        self.value = item.value

class LSPrecisionTimeStamp(BaseElement):
    def __str__(self):
        return "test"

ST0601_tags = dict()
ST0601_tags[2] = LSPrecisionTimeStamp

class BasePacket(BaseElement):
    def __init__(self, item):
        BaseElement.__init__(self, item)
        self.parse_elements()
        self.parse_nested_elements()

    def parse_elements(self):
        self.elements = OrderedDict((bytes2int(item.key), ST0601_tags.get(bytes2int(item.key), BaseElement)(item)) for item in BaseParser(self.value, 1))

    def parse_nested_elements(self):
        # Add recognized element for security metadata
        # @TODO Move to MISB ST0601 parser. Does not belong in base
        # @TODO Handle key error
        # @TODO Clean up code...
        if 48 in self.elements:
            self.elements[48].elements = OrderedDict((item.key, BaseElement(item)) for item in BaseParser(self.elements[48].value, 1))

class TestParser(BaseParser):
    def __next__(self):
        self.parse()

        return BasePacket(self)

def pretty_print(value):
    return " ".join(["{:02X}".format(byte) for byte in value])

def bytes2int(value):
    # @TODO Make BYTEORDER a constant
    # @TODO Make SIGNED a constant
    return int.from_bytes(value, byteorder='big', signed=False)

def int2bytes(value, length):
    # @TODO Make BYTEORDER a constant
    # @TODO Make SIGNED a constant
    return value.to_bytes(length, byteorder='big', signed=False)

def calc_checksum(data):
    length = len(data) - 2
    wordsize, mod = divmod(length, 2)

    words = sum(struct.unpack(">{:d}H".format(wordsize), data[0:length-mod]))

    if mod:
        words += data[length-1] << 8

    return struct.pack('>H', words & 0xFFFF)

