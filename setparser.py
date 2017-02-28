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
from collections import OrderedDict
from pprint import pformat
from klvparser import KLVParser
from element import Element


class SetParser(Element, metaclass=ABCMeta):
    """Parsable Element. Not intended to be used directly. Always as super class."""

    def __init__(self, value):
        """All parser needs is the value, no other information"""
        super().__init__(self.key, value)
        self.items = OrderedDict()
        self._parse()

    def _parse(self):
        """Parse the parent into items. Called on init and modification of parent value."""
        for key, value in KLVParser(self.value, key_length=1):
            if key in self.parsers:
                self.items[key] = self.parsers[key](value)
            else:
                # Even if KLV is not known, make best effort to parse and preserve.
                self.items[key] = Element(key, value)

    @classmethod
    def add_parser(cls, obj):
        """Decorator method used to register a parser to the class parsing repertoire.

        obj is required to implement key attribute supporting bytes as returned by KLVParser key.
        """

        # If sublcass of ElementParser does not implement key, dict accepts key of
        # type property object. bytes(obj.key) will raise TypeError. ElementParser
        # requires key as abstract property but no raise until instantiation which
        # does not occur because the value is never recalled and instantiated from
        # parsers.
        cls.parsers[bytes(obj.key)] = obj

        return obj

    @property
    @classmethod
    @abstractmethod
    def parsers(cls):
        # Property must define __getitem__
        pass

    @parsers.setter
    @classmethod
    @abstractmethod
    def parsers(cls):
        # Property must define __setitem__
        pass

    def __repr__(self):
        return pformat(self.items, indent=1)
