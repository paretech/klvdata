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

import warnings

from klvdata.common import packet_checksum
from klvdata.element import UnknownElement

from klvdata.klvparser import KLVParser


class StreamParser:
    """Iterate over the KLV packets in a source.

    With verify_checksum=True, packets whose parser defines checksum_tag (such
    as the MISB ST 0601 UAS Local Set) are checked against their checksum item
    exactly as they were received. Packets that fail are skipped with a
    warning.
    """
    parsers = {}

    def __init__(self, source, verify_checksum=False):
        self.source = source
        self.verify_checksum = verify_checksum

        # All keys in parser are expected to be 16 bytes long.
        self.iter_stream = KLVParser(self.source, key_length=16)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            key, value = next(self.iter_stream)
            parser = self.parsers.get(key)

            if parser is None:
                # Even if KLV is not known, make best effort to parse and preserve.
                # Element is an abstract super class, do not create instances on Element.
                return UnknownElement(key, value)

            if self.verify_checksum and getattr(parser, 'checksum_tag', None) is not None:
                raw = key + self.iter_stream.length_bytes + value
                if not checksum_matches(raw, parser.checksum_tag):
                    warnings.warn('{}: checksum mismatch, packet skipped'.format(parser.name))
                    continue

            return parser(value)

    @classmethod
    def add_parser(cls, obj):
        """Decorator method used to register a parser to the class parsing repertoire.

        obj is required to implement key attribute supporting bytes as returned by KLVParser key.
        """

        cls.parsers[bytes(obj.key)] = obj

        return obj


def checksum_matches(packet, checksum_tag=b'\x01'):
    """Return True if the 2-byte checksum item at the end of packet matches it.

    packet is a complete SMPTE ST 336 packet (16-byte key, BER length, value)
    whose last item is the checksum, as in MISB ST 0601: tag, length 2, then
    the lower 16 bits of the running sum over everything before the checksum
    value (see MISB ST 0601, Item 1).
    """
    packet = bytes(packet)
    if len(packet) < 4 or packet[-4:-2] != bytes(checksum_tag) + b'\x02':
        return False
    return packet_checksum(packet) == packet[-2:]
