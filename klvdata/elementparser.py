#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from klvdata.element import Element
from klvdata.common import bytes_to_datetime
from klvdata.common import bytes_to_int
from klvdata.common import bytes_to_float
from klvdata.common import bytes_to_hexstr
from klvdata.common import bytes_to_str
from klvdata.common import imapb_to_float
from klvdata.common import datetime_to_bytes
from klvdata.common import float_to_bytes
from klvdata.common import str_to_bytes
from klvdata.common import int_to_bytes
from klvdata.common import float_to_imapb


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
        super().__init__(self.key, value)

    @property
    @classmethod
    @abstractmethod
    def key(cls):
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


class BytesElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(BytesValue(value))

    def __bytes__(self):
        """Return the MISB encoded representation of a Key, Length, Value element."""
        if isinstance(self.value, int):
            bytesvalue = int_to_bytes(self.value)
        else:
            bytesvalue = bytes(self.value)
        return bytes(self.key) + bytes(self.length) + bytesvalue


class BytesValue(BaseValue):
    def __init__(self, value):
        self.value = value

    def __bytes__(self):
        if isinstance(self.value, int):
            return int_to_bytes(self.value, length=1 if self.value <= 255 else 2)
        else:
            return bytes(self.value)

    def __str__(self):
        return bytes_to_hexstr(self.value, start='0x', sep='')


class DateTimeElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(DateTimeValue(value))


class DateTimeValue(BaseValue):
    def __init__(self, value):
        self.value = bytes_to_datetime(value)

    def __bytes__(self):
        return datetime_to_bytes(self.value)

    def __str__(self):
        return self.value.isoformat(sep=' ')


class StringElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(StringValue(value, self._encoding))

    @property
    def _encoding(cls):
        return 'UTF-8'


class StringValue(BaseValue):
    def __init__(self, value, _encoding = 'UTF-8'):
        self._encoding = _encoding
        try:
            self.value = bytes_to_str(value, _encoding)
        except UnicodeDecodeError:
            self.value = value

    def __bytes__(self):
        return str_to_bytes(self.value, self._encoding)

    def __str__(self):
        return str(self.value)


class IntegerElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(IntegerValue(value, self._size, self._signed))

    @property
    @classmethod
    @abstractmethod
    def _signed(cls):
        pass

    @property
    @classmethod
    @abstractmethod
    def _size(cls):
        pass

class IntegerValue(BaseValue):
    def __init__(self, value, _size, _signed):
        self._size = _size
        self._signed = _signed
        if isinstance(value, int):
            self.value = value
        else:
            try:
                self.value = bytes_to_int(value, _signed)
            except TypeError:
                self.value = value

    def __bytes__(self):
        return int_to_bytes(self.value, self._size, self._signed)

    def __str__(self):
        return str(self.value)

class MappedElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        if isinstance(value, float):
            localvalue = float_to_bytes(value, self._domain, self._range)
        elif isinstance(value, int):
            localvalue = float_to_bytes(float(value), self._domain, self._range)
        else:
            localvalue = value
        if int.from_bytes(localvalue, byteorder='big', signed=True) == self._error:
            super().__init__(StringValue(('%s (%s)'%(bytes_to_hexstr(localvalue, start='0x', sep=''),'Standard error indicator')).encode('UTF-8')))
        else:
            super().__init__(MappedValue(localvalue, self._domain, self._range))

    def __bytes__(self):
        """Return the MISB encoded representation of a Key, Length, Value element."""
        return bytes(self.key) + bytes(self.length) + bytes(self.value)


    @property
    @classmethod
    @abstractmethod
    def _domain(cls):
        pass

    @property
    @classmethod
    @abstractmethod
    def _range(cls):
        pass

    @property
    def _error(cls):
        pass

class MappedValue(BaseValue):
    def __init__(self, value, _domain, _range):
        self._domain = _domain
        self._range = _range

        try:
            self.value = bytes_to_float(value, self._domain, self._range)
        except TypeError:
            self.value = value

    def __bytes__(self):
        return float_to_bytes(self.value, self._domain, self._range)

    def __str__(self):
        return format(self.value)

    def __float__(self):
        return self.value

class EnumElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(EnumValue(value, self._enum))

    @property
    @classmethod
    @abstractmethod
    def _enum(cls):
        pass

class EnumValue(BaseValue):
    def __init__(self, value, _enum):
        if isinstance(value, bytes):
            self.value = bytes_to_int(value)
        else:
            self.value = value
        self._enum = _enum

    def __bytes__(self):
        return int_to_bytes(self.value)

    def __str__(self):
        try:
            return self._enum[self.value]
        except KeyError:
            return str(self.value)

class IMAPBElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(IMAPBValue(value, self._range))

    @property
    @classmethod
    @abstractmethod
    def _range(cls):
        pass
    
class IMAPBValue(BaseValue):
    def __init__(self, value, _range):
        self._range = _range
        self._length = len(value)
        self.value = imapb_to_float(value, self._range)

    def __bytes__(self):
        return float_to_imapb(self.value, self._length, self._range)

    def __str__(self):
        return str(self.value)

class LocationElementParser(ElementParser, metaclass=ABCMeta):
    def __init__(self, value):
        super().__init__(LocationValue(value))
    
class LocationValue(BaseValue):
    def __init__(self, value):
        self.value = (imapb_to_float(value[0:4], (-90, 90)), 
                    imapb_to_float(value[4:8], (-180, 180)),
                    imapb_to_float(value[8:10], (-900, 19000)))

    def __bytes__(self):
        return (float_to_imapb(self.value(0), 4, (-90, 90)) + 
                float_to_imapb(self.value(1), 4, (-180, 180)) + 
                float_to_imapb(self.value(1), 2, (-900, 19000)))

    def __str__(self):
        return str(self.value)