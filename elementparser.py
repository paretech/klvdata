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

from abc import ABCMeta
from abc import abstractmethod
from element import Element
from common import bytes_to_datetime
from common import bytes_to_float
from common import bytes_to_hexstr
from common import bytes_to_str
from common import datetime_to_bytes
from common import float_to_bytes
from common import str_to_bytes

class ElementParser(Element, metaclass=ABCMeta):
    """Construct a Element Parser base class.

    Element Parsers are used to enforce the convention that all Element Parsers
    already know the key of the element they are constructing.

    Element Parser is a helper class that simplifies known element definition
    and makes a layer of abstraction for functionality that all known elements
    can share. The parsing interfaces are cleaner and require less coding as
    their definitions (subclasses of Element Parser) do not need to call init
    on super with class key and instance value.
    """

    def __init__(self, value):
        super().__init__(self.key, value )

    @property
    @classmethod
    @abstractmethod
    def key(cls):
        pass

    @property
    @classmethod
    @abstractmethod
    def parser(cls):
        pass

    def __repr__(self):
        """Return as-code string used to re-create the object."""
        return '{}({})'.format(self.name, bytes(self.value))


class BaseValue(metaclass=ABCMeta):
    """Abstract base class (superclass) used to insure internal interfaces are maintained."""
    @abstractmethod
    def __bytes__(self):
        """Required by element.Element"""
        pass

    @abstractmethod
    def __str__(self):
        """Required by element.Element"""
        pass


class BytesValue(BaseValue):
    def __init__(self, value):
        self.value = value

    def __bytes__(self):
        return bytes(self.value)

    def __str__(self):
        return bytes_to_hexstr(self.value, start='0x', sep='')


class DateTimeValue(BaseValue):
    def __init__(self, value):
        self.value = bytes_to_datetime(value)

    def __bytes__(self):
        return datetime_to_bytes(self.value)

    def __str__(self):
        return self.value.isoformat(sep=' ')


class StringValue(BaseValue):
    def __init__(self, value):
        self.value = bytes_to_str(value)

    def __bytes__(self):
        return str_to_bytes(self.value)

    def __str__(self):
        return str(self.value)


class MappedValue(BaseValue):
    def __init__(self, value, _domain, _range):
        self._domain = _domain
        self._range = _range
        self.value = bytes_to_float(value, self._domain, self._range)

    def __bytes__(self):
        return float_to_bytes(self.value, self._domain, self._range)

    def __str__(self):
        return format(self.value)




