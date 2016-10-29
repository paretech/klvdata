#!/usr/bin/env python3

# Copyright 2016 Matthew Pare. All rights reserved.

import klvcms

from collections import OrderedDict
from datetime import datetime

class PacketParser(klvcms.BasePacket):
    element_converters = dict()

    def parse_nested_elements(self):
        # Add recognized element for security metadata
        # @TODO Move to MISB ST0601 parser. Does not belong in base
        # @TODO Clean up code...
        if 48 in self.elements:
            self.elements[48].elements = OrderedDict((item.key, klvcms.BaseElement(item)) for item in klvcms.BaseParser(self.elements[48].value, 1))

    def _get_parser(self, item):
        # TODO: Review use of self.__class__
        return self.__class__.element_converters.get(self._bytes_to_int(item.key), klvcms.BaseElement)

    def __str__(self):
        return '\n'.join(str(value[1]) for value in self.get_items())

class StreamParser(klvcms.BaseParser):
    def __init__(self, source):
        super().__init__(source, 16)

    def __next__(self):
        self.parse()

        return PacketParser(self)

def prepare_converter(cls):
    # Set converter docstring
    cls.__doc__ = "MISB ST0601 {} Converter".format(cls.name)

    PacketParser.element_converters[cls.tag] = cls

    return cls

@prepare_converter
class LSChecksum(klvcms.BaseElement):
    tag, name  = 1, 'Checksum'

    def converter(self, item):
        return item.value

    def __str__(self):
        return "{:2}: '{}' ({} bytes) \"{}\"".format(self.key, self.name, self.length, klvcms.bytes2hexdump(self.value))

@prepare_converter
class LSPrecisionTimeStamp(klvcms.BaseElement):
    tag, name = 2, 'Precision Time Stamp'

    def converter(self, item):
        self.units = 'micro seconds'
        return datetime.utcfromtimestamp(self._bytes_to_int(item.value)*1e-6)

@prepare_converter
class LSMissionID(klvcms.BaseElement):
    tag, name = 3, 'Mission ID'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class LSPlatformTailNumber(klvcms.BaseElement):
    tag, name = 4, "Platform Tail Number"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class LSPlatformHeadingAngle(klvcms.BaseElement):
    tag, name = 5, "Platform Heading Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0 #degrees
        max_value = 360 #degrees

        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class LSPlatformPitchAngle(klvcms.BaseElement):
    tag, name = 6, "Platform Pitch Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -20 #degrees
        max_value = +20 #degrees

        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class LSPlatformRollAngle(klvcms.BaseElement):
    tag, name = 7, "Platform Roll Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -50 #degrees
        max_value = +50 #degrees

        # TODO: Add "out of range" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

# MISB ST0601 Tag 8

# MISB ST0601 Tag 9

@prepare_converter
class LSPlatformDesignation(klvcms.BaseElement):
    tag, name = 10, "Platform Designation"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class LSImageSourceSensor(klvcms.BaseElement):
    tag, name = 11, "Image Source Sensor"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class LSImageCoordinateSystem(klvcms.BaseElement):
    tag, name = 12, "Image Coordinate System"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class LSSensorLatitude(klvcms.BaseElement):
    tag, name = 13, "Sensor Latitude"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -90
        max_value = +90

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class LSSensorLongitude(klvcms.BaseElement):
    tag, name = 14, "Sensor Longitude"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -180
        max_value = +180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class LSSensorTrueAltitude(klvcms.BaseElement):
    tag, name = 15, "Sensor True Altitude Parser"

    def converter(self, item):
        self.units = 'meters'
        min_value = -900
        max_value = +19000
        offset = 900

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value) - offset

@prepare_converter
class LSSensorHorizonalFieldOfView(klvcms.BaseElement):
    tag, name = 16, "Horizontal Field of View"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 180

        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class LSSensorHorizontalFieldOfView(klvcms.BaseElement):
    tag, name = 16, "Horizontal Field of View"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class LSSensorVerticalFieldOfView(klvcms.BaseElement):
    tag, name = 17, "Vertical Field of View"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)


@prepare_converter
class LSSensorRelativeAzimuthAngle(klvcms.BaseElement):
    tag, name = 18, "Sensor Relative Azimuth Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 360

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class LSSensorRelativeElevationAngle(klvcms.BaseElement):
    tag, name = 19, "Sensor Relative Elevation Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -180
        max_value = +180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class LSSensorRelativeRollAngle(klvcms.BaseElement):
    tag, name = 20, "Sensor Relative Roll Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = +360

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class LSSlantRange(klvcms.BaseElement):
    tag, name = 21, "Slant Range"

    def converter(self, item):
        self.units = 'meters'
        min_value = 0
        max_value = +5e6

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        read_file = sys.argv[1]
    else:
        read_file = 'DynamicConstantMISMMSPacketData_modified.bin'

    with open(read_file, 'rb') as f:
        for packet in StreamParser(f):
            print(packet)
