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


from element import Element
from datetime import datetime
from common import bytes_to_int
from common import hexstr_to_bytes

from packetparser import PacketParser

from parser import Parser


@PacketParser.add_parser
class UASLocalSet:
    key = hexstr_to_bytes('06 0E 2B 34 - 02 0B 01 01 – 0E 01 03 01 - 01 00 00 00')
    name = 'UAS Datalink Local Set'

    tags = {}

    @classmethod
    def add_parser(cls, obj):
        cls.tags[obj.key] = obj

        return obj

    def __init__(self, _value, depth=-1):
        self._value = {}

        for tag, value in Parser(_value, key_length=1):
            self._value[tag] = self.tags.get(tag, UnknownLocalSetElement)(value)


class LocalSetElement(Element):
    def __init__(self, value):
        super().__init__(self.key, value)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)


class UnknownLocalSetElement(LocalSetElement):
    key = b'\x09'


@UASLocalSet.add_parser
class Checksum(LocalSetElement):
    key, name = b'\x01', 'Checksum'


@UASLocalSet.add_parser
class PrecisionTimeStamp(LocalSetElement):
    key, name = b'\x02', 'Precision Time Stamp'

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(int(bytes_to_int(self.value)/1e6))

    def __str__(self):
        return "{}: {}".format(self.name, self.datetime.isoformat(sep=' '))
