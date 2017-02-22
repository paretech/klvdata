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
    def __init__(self, key, value):
        self.key = key
        self.value = value

    @property
    def length(self):
        """Return the BER encoded byte length of self.value."""
        return ber_encode(len(self))

    def __len__(self):
        """Return the defined length or integer byte length of self.value."""
            return len(self.value)

    def __bytes__(self):
        """Return the MISB encoded representation of a Key, Length, Value element."""
        return bytes(self.key) + self.length + bytes(self.value)

    def __repr__(self):
        args = ', '.join(map(repr, (self.key, self.value)))
        return '{}({})'.format(self.__class__.__name__, args)
