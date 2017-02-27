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

from collections import OrderedDict
from pprint import pformat
from klvparser import KLVParser
from element import Element


class SetParser(Element):
    """Parsable Element. Not intended to be used directly. Always as super class."""

    def __init__(self, value):
        """All parser needs is the value, no other information"""
        super().__init__(self.key, value)
        self._items = OrderedDict()
        self._parse()

    def _parse(self):
        """Parse the parent into items. Only called on init."""
        for key, value in KLVParser(self._value, key_length=1):
            self._items[key] = self.get_parser(key)(key, value)

    def items(self):
        """Return ordered dictionary of parsed parent items."""
        return self._items

    @classmethod
    def add_parser(cls, obj):
        """Decorator method used to register a parser to the class parsing repertoire."""
        cls._parsers[obj.key] = obj

        return obj

    @classmethod
    def get_parser(cls, key):
        """Query parsers given key."""
        return cls._parsers.get(key, Element)

    def __repr__(self):
        return pformat(self.items())
