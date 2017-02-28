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

from datetime import datetime
from common import bytes_to_int
from common import hexstr_to_bytes
from element import ElementParser
from setparser import SetParser


class ST0601(SetParser):
    """MISB ST0601 UAS Local Metadata Set
    """
    key = hexstr_to_bytes('06 0E 2B 34 - 02 0B 01 01 – 0E 01 03 01 - 01 00 00 00')
    name = 'UAS Datalink Local Set'

    # Every
    parsers = {}


@ST0601.add_parser
class Checksum(ElementParser):
    key, name = b'\x01', 'Checksum'


@ST0601.add_parser
class PrecisionTimeStamp(ElementParser):
    key, name = b'\x02', 'Precision Time Stamp'

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(int(bytes_to_int(self.value)/1e6))

    def __str__(self):
        return str("{}: {}".format(self.name, self.datetime.isoformat(sep=' ')))
