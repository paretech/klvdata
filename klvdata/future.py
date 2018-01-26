#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Matthew Pare (paretech@gmail.com)
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

from datetime import datetime, timedelta

import io
from collections import OrderedDict

import klvparser


@register
class Checksum(ConverterElement):
    tag, name = 1, 'Checksum'
    min_length, max_length, signed = 2, 2, False


@register
class PrecisionTimeStamp(DateConverterElement):
    tag, name = 2, 'Precision Time Stamp'
    min_value, max_value, units = datetime.utcfromtimestamp(0), \
                                  datetime.max, 'microseconds'
    min_length, max_length, signed = 8, 8, False


@register
class MissionID(StringConverterElement):
    '''Descriptive Mission Identifier to distinguish event or sortie.

    Value field is Free Text. Maximum 127 characters
    '''
    tag, name = 3, 'Mission ID'
    min_length, max_length = 0, 127


@register
class PlatformTailNumber(StringConverterElement):
    tag, name = 4, "Platform Tail Number"
    min_length, max_length = 0, 127


@register
class PlatformHeadingAngle(MappedConverterElement):
    tag, name = 5, "Platform Heading Angle"

    # TODO: Design problem or thought needed to better structure converters
    #       to support validation during parsing, getting and setting.
    min_value, max_value, units = 0, 360, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class PlatformPitchAngle(MappedConverterElement):
    tag, name = 6, "Platform Pitch Angle"
    min_value, max_value, units = -20, +20, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class PlatformRollAngle(MappedConverterElement):
    tag, name = 7, "Platform Roll Angle"
    min_value, max_value, units = -50, +50, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class PlatformTrueAirspeed(MappedConverterElement):
    tag, name = 8, "Platform True Airspeed"
    min_value, max_value, units = 0, +255, 'meters/second'
    min_length, max_length, signed = 1, 1, False


@register
class PlatformTrueAirspeed(MappedConverterElement):
    tag, name = 9, "Platform Indicated Airspeed"
    min_value, max_value, units = 0, +255, 'meters/second'
    min_length, max_length, signed = 1, 1, False


@register
class PlatformDesignation(StringConverterElement):
    tag, name = 10, "Platform Designation"
    min_length, max_length = 0, 127


@register
class ImageSourceSensor(StringConverterElement):
    tag, name = 11, "Image Source Sensor"
    min_length, max_length = 0, 127


@register
class ImageCoordinateSystem(StringConverterElement):
    tag, name = 12, "Image Coordinate System"
    min_length, max_length = 0, 127


@register
class SensorLatitude(MappedConverterElement):
    tag, name = 13, "Sensor Latitude"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class SensorLongitude(MappedConverterElement):
    tag, name = 14, "Sensor Longitude"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class SensorTrueAltitude(MappedConverterElement):
    tag, name = 15, "Sensor True Altitude"
    min_value, max_value, units = -900, +19e3, 'meters'
    min_length, max_length, signed = 2, 2, False


@register
class SensorHorizontalFieldOfView(MappedConverterElement):
    tag, name = 16, "Sensor Horizontal Field of View"
    min_value, max_value, units = 0, +180, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class SensorVerticalFieldOfView(MappedConverterElement):
    tag, name = 17, "Sensor Vertical Field of View"
    min_value, max_value, units = 0, +180, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class SensorRelativeAzimuthAngle(MappedConverterElement):
    tag, name = 18, "Sensor Relative Azimuth Angle"
    min_value, max_value, units = 0, +360, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class SensorRelativeElevationAngle(MappedConverterElement):
    tag, name = 19, "Sensor Relative Elevation Angle"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class SensorRelativeRollAngle(MappedConverterElement):
    tag, name = 20, "Sensor Relative Roll Angle"
    min_value, max_value, units = 0, +360, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class SlantRange(MappedConverterElement):
    tag, name = 21, "Slant Range"
    min_value, max_value, units = 0, +5e6, 'meters'
    min_length, max_length, signed = 4, 4, False


@register
class TargetWidth(MappedConverterElement):
    tag, name = 22, "Target Width"
    min_value, max_value, units = 0, +10e3, 'meters'
    min_length, max_length, signed = 2, 2, False


@register
class FrameCenterLatitude(MappedConverterElement):
    tag, name = 23, "Frame Center Latitude"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class FrameCenterLongitude(MappedConverterElement):
    tag, name = 24, "Frame Center Longitude"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class FrameCenterElevation(MappedConverterElement):
    tag, name = 25, "Frame Center Elevation"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLatitudePoint1(MappedConverterElement):
    tag, name = 26, "Offset Corner Latitude Point 1"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLongitudePoint1(MappedConverterElement):
    tag, name = 27, "Offset Corner Longitude Point 1"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLatitudePoint2(MappedConverterElement):
    tag, name = 28, "Offset Corner Latitude Point 2"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLongitudePoint2(MappedConverterElement):
    tag, name = 29, "Offset Corner Longitude Point 2"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLatitudePoint3(MappedConverterElement):
    tag, name = 30, "Offset Corner Latitude Point 3"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLongitudePoint3(MappedConverterElement):
    tag, name = 31, "Offset Corner Longitude Point 3"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLatitudePoint4(MappedConverterElement):
    tag, name = 32, "Offset Corner Latitude Point 4"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class OffsetCornerLongitudePoint4(MappedConverterElement):
    tag, name = 33, "Offset Corner Longitude Point 4"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, True


# Tags 34-39 "Atmospheric Conditions"

@register
class TargetLocationLatitude(MappedConverterElement):
    tag, name = 40, "Target Location latitude"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class TargetLocationLongitude(MappedConverterElement):
    tag, name = 41, "Target Location Longitude"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class TargetLocationElevation(MappedConverterElement):
    tag, name = 42, "Target Location Elevation"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


# Tags 43 - 46 "Target Information"

# Tag 47 "Generic Flag"

@register
class SecurityLocalMetadataSet(ConverterElement):
    tag, name = 48, "Security Local Metadata Set"

    def __init__(self, element):
        self.tag = element.key
        self._length = element.length
        self._value = element.value

        self._tags = OrderedDict()
        self.parse_tags()

    def parse_tags(self):
        for tag in klvparser.KLVParser(io.BytesIO(self.value), key_length=1):
            self._tags[tag.key] = UnsupportedTag(tag)

    def __str__(self):
        return super().__str__() + '\n' + '\n'.join(['    ' + str(tag) for tag in self._tags.values()])


# Tags 49 - 64

@register
class UASLSVersionNumber(ConverterElement):
    tag, name = 65, "UAS LS Version Number"

    # TODO: Associate max version with the version of the MISB implemented?
    min_length, max_length, signed = 1, 1, False


# Tags 66 - 81

@register
class CornerLatitudePoint1Full(MappedConverterElement):
    tag, name = 82, "Corner Latitude Point 1 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class CornerLongitudePoint1Full(MappedConverterElement):
    tag, name = 83, "Corner Longitude Point 1 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True

@register
class CornerLatitudePoint2Full(MappedConverterElement):
    tag, name = 84, "Corner Latitude Point 2 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class CornerLongitudePoint2Full(MappedConverterElement):
    tag, name = 85, "Corner Longitude Point 2 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class CornerLatitudePoint3Full(MappedConverterElement):
    tag, name = 86, "Corner Latitude Point 3 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class CornerLongitudePoint3Full(MappedConverterElement):
    tag, name = 87, "Corner Longitude Point 3 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True

@register
class CornerLatitudePoint4Full(MappedConverterElement):
    tag, name = 88, "Corner Latitude Point 4 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class CornerLongitudePoint4Full(MappedConverterElement):
    tag, name = 89, "Corner Longitude Point 4 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


# Tags 90 - 93

# @register
class MIISCoreIdentifier(object):
    tag, name = 94, "MIIS Core Identifier"

    def converter(self, item):
        return self._bytes_to_hex_dump(item.value)


# Tags 95 - 96
