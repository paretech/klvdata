#!/usr/bin/env python3

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
        """Return the integer byte length of self.value."""
        return len(self.value)

    def __bytes__(self):
        """Return the MISB encoded representation of a Key, Length, Value element."""
        return bytes(self.key) + self.length + bytes(self.value)
