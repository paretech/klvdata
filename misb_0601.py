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


class LocalSetElement(Element):
    def __init__(self, value):
        super().__init__(self._key, value)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)


class Checksum(LocalSetElement):
    _key, _name = 1, 'Checksum'


class PrecisionTimeStamp(LocalSetElement):
    _key, _name = b'\x02', 'Precision Time Stamp'

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(int(bytes_to_int(self.value)/1e6))

    def __str__(self):
        return "{}: {}".format(self._name, self.datetime.isoformat(sep=' '))
