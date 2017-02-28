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

from common import ber_encode


class Element:
    """Construct a key, length, value tuplet.

    Elements provide the basic mechanisms to constitute the basic encoding
    requirements of key, length, value tuplet as specified by STMPE 336.

    The length is dynamically calculated based off the value.

    Attributes:
        key (bytes): STMPE 336 key
        value (bytes): STMPE 336 value
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

        self._items = None

    @property
    def length(self):
        """bytes: Return the BER encoded byte length of self.value."""
        return ber_encode(len(self))

    def __bytes__(self):
        """Return the MISB encoded representation of a Key, Length, Value element."""
        return bytes(self.key) + bytes(self.length) + bytes(self.value)

    def __len__(self):
        """Return the defined length or integer byte length of self.value."""
        return len(self.value)

    def __repr__(self):
        """Return as-code string used to re-create the object."""
        args = ', '.join(map(repr, (self.key, self.value)))
        return '{}({})'.format(self.__class__.__name__, args)


class ElementParser(Element):
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


