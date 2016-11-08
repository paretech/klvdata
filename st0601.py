#!/usr/bin/env python3

# Copyright 2016 Matthew Pare. All rights reserved.

import klvcms

from collections import OrderedDict
from datetime import datetime

class PacketParser(klvcms.BasePacket):
    element_converters = dict()

    def _get_parser(self, item):
        # TODO: Review use of self.__class__
        return self.__class__.element_converters.get(self._bytes_to_int(item.key), klvcms.BaseConverter)

class StreamParser(klvcms.BaseParser):
    def __init__(self, source):
        super().__init__(source, 16)

    def __next__(self):
        self.parse()

        return PacketParser(self)

def register(obj):
    PacketParser.element_converters[obj.tag] = obj
    return obj

@register
class Checksum(klvcms.BaseConverter):
    tag, name  = 1, 'Checksum'

    length = 2

    def converter(self, item):
        return item.value

    def __str__(self):
        return "{:2}: '{}' ({} bytes) \"{}\"".format(self.key, self.name, self.length, self._bytes_to_hex_dump(self.value))

@register
class PrecisionTimeStamp(klvcms.BaseConverter):
    tag, name = 2, 'Precision Time Stamp'

    min_value, max_value, units = 0, 2**64 - 1, 'microseconds'
    length, signed = 8, False

    def converter(self, item):
        return datetime.utcfromtimestamp(self._bytes_to_int(item.value)*1e-6)

    def __int__(self):
        pass

@register
class MissionID(klvcms.BaseConverter):
    tag, name = 3, 'Mission ID'

    min_value, max_value, units = 1, 127, 'string'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@register
class PlatformTailNumber(klvcms.BaseConverter):
    tag, name = 4, "Platform Tail Number"

    min_value, max_value, units = 1, 127, 'string'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@register
class PlatformHeadingAngle(klvcms.BaseConverter):
    tag, name = 5, "Platform Heading Angle"

    min_value, max_value, units = 0, 360, 'degrees'
    length, signed = 2, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class PlatformPitchAngle(klvcms.BaseConverter):
    tag, name = 6, "Platform Pitch Angle"

    min_value, max_value, units = -20, +20, 'degrees'
    length, signed = 2, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class PlatformRollAngle(klvcms.BaseConverter):
    tag, name = 7, "Platform Roll Angle"

    min_value, max_value, units = -50, +50, 'degrees'
    length, signed = 2, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class PlatformTrueAirspeed(klvcms.BaseConverter):
    tag, name = 8, "Platform True Airspeed"

    min_value, max_value, units = 0, +255, 'meters'
    length, signed = 1, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

# MISB ST0601 Tag 9

@register
class PlatformDesignation(klvcms.BaseConverter):
    tag, name = 10, "Platform Designation"

    min_value, max_value, units = 1, 127, 'string'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@register
class ImageSourceSensor(klvcms.BaseConverter):
    tag, name = 11, "Image Source Sensor"

    min_value, max_value, units = 1, 127, 'string'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@register
class ImageCoordinateSystem(klvcms.BaseConverter):
    tag, name = 12, "Image Coordinate System"

    min_value, max_value, units = 1, 127, 'string'

    def converter(self, item):
        return self._bytes_to_str(item.value)

@register
class SensorLatitude(klvcms.BaseConverter):
    tag, name = 13, "Sensor Latitude"

    min_value, max_value, units = -90, +90, 'degrees'
    length, signed = 4, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorLongitude(klvcms.BaseConverter):
    tag, name = 14, "Sensor Longitude"

    min_value, max_value, units = -180, +180, 'degrees'
    length, signed = 4, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorTrueAltitude(klvcms.BaseConverter):
    tag, name = 15, "Sensor True Altitude"

    min_value, max_value, units = -900, +19e3, 'meters'
    length, signed = 2, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorHorizontalFieldOfView(klvcms.BaseConverter):
    tag, name = 16, "Sensor Horizontal Field of View"


    min_value, max_value, units = 0, +180, 'degrees'
    length, signed = 2, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorHorizontalFieldOfView(klvcms.BaseConverter):
    tag, name = 16, "Sensor Horizontal Field of View"

    min_value, max_value, units = 0, +180, 'degrees'
    length, signed = 2, False


    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorVerticalFieldOfView(klvcms.BaseConverter):
    tag, name = 17, "Sensor Vertical Field of View"

    min_value, max_value, units = 0, +180, 'degrees'
    length, signed = 2, False


    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorRelativeAzimuthAngle(klvcms.BaseConverter):
    tag, name = 18, "Sensor Relative Azimuth Angle"

    min_value, max_value, units = 0, +360, 'degrees'
    length, signed = 4, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorRelativeElevationAngle(klvcms.BaseConverter):
    tag, name = 19, "Sensor Relative Elevation Angle"

    min_value, max_value, units = -180, +180, 'degrees'
    length, signed = 4, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SensorRelativeRollAngle(klvcms.BaseConverter):
    tag, name = 20, "Sensor Relative Roll Angle"

    min_value, max_value, units = 0, +360, 'degrees'
    length, signed = 4, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class SlantRange(klvcms.BaseConverter):
    tag, name = 21, "Slant Range"

    min_value, max_value, units = 0, +5e6, 'meters'
    length, signed = 4, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class TargetWidth(klvcms.BaseConverter):
    tag, name = 22, "Target Width"

    min_value, max_value, units = 0, +10e3, 'meters'
    length, signed = 2, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class FrameCenterLatitude(klvcms.BaseConverter):
    tag, name = 23, "Frame Center Latitude"

    min_value, max_value, units = -90, +90, 'degrees'
    length, signed = 4, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class FrameCenterLongitude(klvcms.BaseConverter):
    tag, name = 24, "Frame Center Longitude"

    min_value, max_value, units = -180, +180, 'degrees'
    length, signed = 4, True

    def converter(self, item):
        return self._fixed_to_float(item.value)

@register
class FrameCenterElevation(klvcms.BaseConverter):
    tag, name = 25, "Frame Center Elevation"

    min_value, max_value, units = -900, +19e3, "meters"
    length, signed = 2, False

    def converter(self, item):
        return self._fixed_to_float(item.value)

# MISB Tags 26-64

# TODO Work on 26-32, 40-42, 59, 48 first...

@register
class SecurityLocalMetadataSet(klvcms.BaseConverter):
    tag, name = 48, "Security Local Metadata Set"

    def converter(self, item):
        # TODO Create ST0102 module and parse constituent elements.
        return self._bytes_to_hex_dump(item.value)

@register
class UASLSVersionNumber(klvcms.BaseConverter):
    tag, name = 65, "UAS LS Version Number"

    def converter(self, item):
        return 'MISB ST 0601.{}'.format(self._bytes_to_int(item.value))

@register
class MIISCoreIdentifier(klvcms.BaseConverter):
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

