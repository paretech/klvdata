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

        self.key = BaseValue(self.read(self.size))

        self.length = struct.unpack('>B', self.read(1))[0]

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

class BaseValue:
    def __init__(self, value):
        # @TODO Is key being stored as bytes or int?
        self.value = value

    def __str__(self):
        return pretty_print(self.value)

    def __int__(self):
        # @TODO does it make more sense to use CRC for UL?
        return bytes2int(self.value)

    def __bytes__(self):
        # @TODO Is key being stored as bytes or int? No gurantee you are 
        #   going to get what you intended ATM.
        return self.value

class BaseElement:
    def __init__(self, item):
        # @TODO make KEY class so __bytes__ and __int__ method. int(key) bytes(key)
        self.key = BaseValue(item.key)
        self.length = item.length
        self.value = item.value

    def __str__(self):
        return 'key={}, length={}, value={}'.format(int(self.key), self.length, self.value)

class LSPrecisionTimeStamp(BaseElement):
    pass

ST0601_tags = dict()
ST0601_tags[2] = LSPrecisionTimeStamp

class BasePacket(BaseElement):
    def __init__(self, item):
        BaseElement.__init__(self, item)
        # self.value = {item.key: BaseElement(item) for item in BaseParser(self.value, 1)}
        self.parse_elements()
        self.parse_nested_elements()

        self.validate_packet()

    def parse_elements(self):
        # @TODO move key to int conversion to method
        # self.elements = {int(item.key): ST0601_tags.get(int(item.key),BaseElement)(item) for item in BaseParser(self.value, 1)}
        self.elements = OrderedDict((int(item.key), ST0601_tags.get(int(item.key), BaseElement)(item)) for item in BaseParser(self.value, 1))

    def parse_nested_elements(self):
        # Add recognized element for security metadata
        # @TODO Move to MISB ST0601 parser. Does not belong in base
        # @TODO Handle key error
        # @TODO Clean up code...
        if 48 in self.elements:
            self.elements[48].elements = OrderedDict((item.key, BaseElement(item)) for item in BaseParser(self.elements[48].value, 1))

    def validate_packet(self):
        pass

    def print_tags(self):
        for key, value in self.elements.items():
            print(value)


class TestParser(BaseParser):
    def __next__(self):
        self.parse()

        return BasePacket(self)

class PacketStream(BaseParser):
    def __init__(self, source):
        Parser.__init__(self, source, size=16)

    def __next__(self):
        Parser.__next__(self)

        # ST 0601.8 - 11 All instances of the UAS Datalink LS shall contain
        #     as the final element Tag 1, (Checksum).
        if self.value[-4:-2] != b'\x01\x02':
            warnings.warn("Checksum not final element tag", UserWarning)

        # ST 0601.8 - 08 All instances of a UAS Datalink LS where the computed
        #    checksum is not identical to the included checksum shall be discarded.

        if self.value[-2:] != calc_checksum(self.raw):
            warnings.warn("Invalid Checksum", UserWarning)

        return self

class LSParser():
    def __init__(self, source):
        Parser.__init__(self, source, size=1)

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


def int_key(packet):
    return int.from_bytes(packet.key, 'big')


