#!/usr/bin/env python3

# Copyright 2016 Matthew Pare. All rights reserved.

import klvcms

from collections import OrderedDict
from datetime import datetime

class PacketParser(klvcms.BasePacket):
    element_converters = dict()

    def _get_parser(self, item):
        # TODO: Review use of self.__class__
        return self.__class__.element_converters.get(self._bytes_to_int(item.key), klvcms.BaseElement)

class StreamParser(klvcms.BaseParser):
    def __init__(self, source):
        super().__init__(source, 16)

    def __next__(self):
        self.parse()

        return PacketParser(self)

def prepare_converter(cls):
    # TODO: Make this work, consider exceptions like ID, MIIS
    # cls.name = ' '.join(re.findall('[A-Z][^A-Z]*', cls.__name__))

    cls.__doc__ = "MISB ST0601 {} Converter".format(cls.name)

    PacketParser.element_converters[cls.tag] = cls

    return cls

@prepare_converter
class Checksum(klvcms.BaseElement):
    tag, name  = 1, 'Checksum'

    def converter(self, item):
        return item.value

    def __str__(self):
        return "{:2}: '{}' ({} bytes) \"{}\"".format(self.key, self.name, self.length, self._bytes_to_hex_dump(self.value))

@prepare_converter
class PrecisionTimeStamp(klvcms.BaseElement):
    tag, name = 2, 'Precision Time Stamp'

    def converter(self, item):
        self.units = 'micro seconds'
        return datetime.utcfromtimestamp(self._bytes_to_int(item.value)*1e-6)

@prepare_converter
class MissionID(klvcms.BaseElement):
    tag, name = 3, 'Mission ID'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class PlatformTailNumber(klvcms.BaseElement):
    tag, name = 4, "Platform Tail Number"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class PlatformHeadingAngle(klvcms.BaseElement):
    tag, name = 5, "Platform Heading Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0 #degrees
        max_value = 360 #degrees

        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class PlatformPitchAngle(klvcms.BaseElement):
    tag, name = 6, "Platform Pitch Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -20 #degrees
        max_value = +20 #degrees

        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class PlatformRollAngle(klvcms.BaseElement):
    tag, name = 7, "Platform Roll Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value, max_value = -50, +50 #degrees

        # TODO: Add "out of range" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class PlatformTrueAirspeed(klvcms.BaseElement):
    tag, name = 8, "Platform True Airspeed"

    def converter(self, item):
        self.units = "meters"
        min_value, max_value = 0, +255

        return self._scale_value(min_value, max_value, item.value)

# MISB ST0601 Tag 9

@prepare_converter
class PlatformDesignation(klvcms.BaseElement):
    tag, name = 10, "Platform Designation"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class ImageSourceSensor(klvcms.BaseElement):
    tag, name = 11, "Image Source Sensor"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class ImageCoordinateSystem(klvcms.BaseElement):
    tag, name = 12, "Image Coordinate System"

    def converter(self, item):
        return self._bytes_to_str(item.value)

@prepare_converter
class SensorLatitude(klvcms.BaseElement):
    tag, name = 13, "Sensor Latitude"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -90
        max_value = +90

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class SensorLongitude(klvcms.BaseElement):
    tag, name = 14, "Sensor Longitude"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -180
        max_value = +180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class SensorTrueAltitude(klvcms.BaseElement):
    tag, name = 15, "Sensor True Altitude"

    def converter(self, item):
        self.units = 'meters'
        min_value = -900
        max_value = +19000
        offset = -900

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value) + offset

@prepare_converter
class SensorHorizontalFieldOfView(klvcms.BaseElement):
    tag, name = 16, "Sensor Horizontal Field of View"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 180

        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class SensorHorizontalFieldOfView(klvcms.BaseElement):
    tag, name = 16, "Sensor Horizontal Field of View"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class SensorVerticalFieldOfView(klvcms.BaseElement):
    tag, name = 17, "Sensor Vertical Field of View"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)


@prepare_converter
class SensorRelativeAzimuthAngle(klvcms.BaseElement):
    tag, name = 18, "Sensor Relative Azimuth Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = 360

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class SensorRelativeElevationAngle(klvcms.BaseElement):
    tag, name = 19, "Sensor Relative Elevation Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = -180
        max_value = +180

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class SensorRelativeRollAngle(klvcms.BaseElement):
    tag, name = 20, "Sensor Relative Roll Angle"

    def converter(self, item):
        self.units = 'degrees'
        min_value = 0
        max_value = +360

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class SlantRange(klvcms.BaseElement):
    tag, name = 21, "Slant Range"

    def converter(self, item):
        self.units = 'meters'
        min_value = 0
        max_value = +5e6

        # TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class TargetWidth(klvcms.BaseElement):
    tag, name = 22, "Target Width"

    def converter(self, item):
        min_value, max_value, self.units = 0, +10e3, "meters"

        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class FrameCenterLatitude(klvcms.BaseElement):
    tag, name = 23, "Frame Center Latitude"

    def converter(self, item):
        min_value, max_value, self.units = -90, +90, "degrees"

        return self._scale_value(min_value, max_value, item.value, signed=True)

@prepare_converter
class FrameCenterLongitude(klvcms.BaseElement):
    tag, name = 24, "Frame Center Longitude"

    def converter(self, item):
        min_value, max_value, self.units = -180, +180, "degrees"

        return self._scale_value(min_value, max_value, item.value)

@prepare_converter
class FrameCenterElevation(klvcms.BaseElement):
    tag, name = 25, "Frame Center Elevation"

    def converter(self, item):
        min_value, max_value, self.units = -900, +19e3, "meters"
        offset = min_value

        return self._scale_value(min_value, max_value, item.value) + offset

# MISB Tags 26-64

# TODO Work on 26-32, 40-42, 59, 48 first...

@prepare_converter
class SecurityLocalMetadataSet(klvcms.BaseElement):
    tag, name = 48, "Security Local Metadata Set"

    def converter(self, item):
        # TODO Create ST0102 module and parse constituent elements.
        return self._bytes_to_hex_dump(item.value)

@prepare_converter
class UASLSVersionNumber(klvcms.BaseElement):
    tag, name = 65, "UAS LS Version Number"

    def converter(self, item):
        return 'MISB ST 0601.{}'.format(self._bytes_to_int(item.value))

@prepare_converter
class MIISCoreIdentifier(klvcms.BaseElement):
    tag, name = 94, "MIIS Core Identifier"

    def converter(self, item):
        return self._bytes_to_hex_dump(item.value)

if __name__ == '__main__':
    import sys

    def parse_stream(s):
        for packet in StreamParser(s):
            print(packet)

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'rb') as f:
            parse_stream(f)
    else:
        parse_stream(sys.stdin.buffer)

