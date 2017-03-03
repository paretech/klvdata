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

from datetime import datetime, timezone
from struct import pack
from common import bytes_to_int
from common import hexstr_to_bytes
from elementparser import ElementParser
from element import Element
from setparser import SetParser




class ST0601(SetParser):
    """MISB ST0601 UAS Local Metadata Set
    """
    key = hexstr_to_bytes('06 0E 2B 34 - 02 0B 01 01 – 0E 01 03 01 - 01 00 00 00')
    name = 'UAS Datalink Local Set'

    parsers = {}


@ST0601.add_parser
class Checksum(ElementParser):
    key, name = b'\x01', 'Checksum'


class _datetime(datetime):
    def __bytes__(self):
        return pack('>Q', int(self.timestamp() * 1e6))

    @classmethod
    def utcfromprecisiontimestamp(cls, t):
        return cls.utcfromtimestamp(int(t/1e6))

    @classmethod
    def fromprecisiontimestamp(cls, t, tz=None):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """

        return cls.fromtimestamp(int(t/1e6), tz)


class Timestamp:
    def __init__(self, ts):
        self.bad = datetime.fromtimestamp(bytes_to_int(ts)/1e6, tz=timezone.utc)

    def __bytes__(self):
        return pack('>Q', int(self.bad.timestamp() * 1e6))



@ST0601.add_parser
class PrecisionTimeStamp(Element):
    key, name = b'\x02', 'Precision Time Stamp'

    def __init__(self, value):
        super().__init__(self.key, datetime.fromtimestamp(bytes_to_int(value)/1e6, tz=timezone.utc))

    def __str__(self):
        return str("{}: {}".format(self.name, self.value.isoformat(sep=' ')))


