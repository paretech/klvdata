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

from common import bytes_to_datetime
from common import bytes_to_str
from common import hexstr_to_bytes

from elementparser import ElementParser
from setparser import SetParser
from streamparser import StreamParser

from elementparser import BytesValue
from elementparser import DateTimeValue
from elementparser import MappedValue
from elementparser import StringValue


@StreamParser.add_parser
class ST0601(SetParser):
    """MISB ST0601 UAS Local Metadata Set
    """
    key = hexstr_to_bytes('06 0E 2B 34 - 02 0B 01 01 – 0E 01 03 01 - 01 00 00 00')
    name = 'UAS Datalink Local Set'

    parsers = {}


@ST0601.add_parser
class Checksum(ElementParser):
    """Checksum used to detect errors within a UAV Local Set packet.

    Checksum formed as lower 16-bits of summation performed on entire
    LS packet, including 16-byte US key and 1-byte checksum length.

    Initialized from bytes value as BytesValue.
    """
    key = b'\x01'
    parser = BytesValue

    def __init__(self, value):
        super().__init__(BytesValue(value))


@ST0601.add_parser
class PrecisionTimeStamp(ElementParser):
    """Precision Timestamp represented in microseconds.

    Precision Timestamp represented in the number of microseconds elapsed
    since midnight (00:00:00), January 1, 1970 not including leap seconds.

    See MISB ST 0603 for additional details.
    """
    key = b'\x02'
    parser = DateTimeValue

    def __init__(self, value):
        super().__init__(DateTimeValue(value))


@ST0601.add_parser
class MissionID(ElementParser):
    """Mission ID is the descriptive mission identifier.

    Mission ID value field free text with maximum of 127 characters
    describing the event.
    """
    key = b'\x03'
    parser = StringValue

    def __init__(self, value):
        super().__init__(StringValue(value))


@ST0601.add_parser
class PlatformTailNumber(ElementParser):
    key = b'\x04'
    parser = StringValue

    def __init__(self, value):
        super().__init__(StringValue(value))


@ST0601.add_parser
class PlatformHeadingAngle(ElementParser):
    key = b'\x05'
    units = "Degrees"
    _domain = (0, 2**16-1)
    _range = (0, 360)
    parser = MappedValue

    from element import Element
    def __init__(self, value):
        super().__init__(MappedValue(value, self._domain, self._range))


# @ST0601.add_parser
# class PlatformPitchAngle(ElementParser):
#     tag, name = 6, "Platform Pitch Angle"
#     min_value, max_value, units = -20, +20, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class PlatformRollAngle(ElementParser):
#     tag, name = 7, "Platform Roll Angle"
#     min_value, max_value, units = -50, +50, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class PlatformTrueAirspeed(ElementParser):
#     tag, name = 8, "Platform True Airspeed"
#     min_value, max_value, units = 0, +255, 'meters/second'
#     min_length, max_length, signed = 1, 1, False
#
#
# @ST0601.add_parser
# class PlatformTrueAirspeed(ElementParser):
#     tag, name = 9, "Platform Indicated Airspeed"
#     min_value, max_value, units = 0, +255, 'meters/second'
#     min_length, max_length, signed = 1, 1, False
#
#
# @ST0601.add_parser
# class PlatformDesignation(ElementParser):
#     tag, name = 10, "Platform Designation"
#     min_length, max_length = 0, 127
#
#
# @ST0601.add_parser
# class ImageSourceSensor(ElementParser):
#     tag, name = 11, "Image Source Sensor"
#     min_length, max_length = 0, 127
#
#
# @ST0601.add_parser
# class ImageCoordinateSystem(ElementParser):
#     tag, name = 12, "Image Coordinate System"
#     min_length, max_length = 0, 127
#
#
# @ST0601.add_parser
# class SensorLatitude(ElementParser):
#     tag, name = 13, "Sensor Latitude"
#     min_value, max_value, units = -90, +90, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class SensorLongitude(ElementParser):
#     tag, name = 14, "Sensor Longitude"
#     min_value, max_value, units = -180, +180, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class SensorTrueAltitude(ElementParser):
#     tag, name = 15, "Sensor True Altitude"
#     min_value, max_value, units = -900, +19e3, 'meters'
#     min_length, max_length, signed = 2, 2, False
#
#
# @ST0601.add_parser
# class SensorHorizontalFieldOfView(ElementParser):
#     tag, name = 16, "Sensor Horizontal Field of View"
#     min_value, max_value, units = 0, +180, 'degrees'
#     min_length, max_length, signed = 2, 2, False
#
#
# @ST0601.add_parser
# class SensorVerticalFieldOfView(ElementParser):
#     tag, name = 17, "Sensor Vertical Field of View"
#     min_value, max_value, units = 0, +180, 'degrees'
#     min_length, max_length, signed = 2, 2, False
#
#
# @ST0601.add_parser
# class SensorRelativeAzimuthAngle(ElementParser):
#     tag, name = 18, "Sensor Relative Azimuth Angle"
#     min_value, max_value, units = 0, +360, 'degrees'
#     min_length, max_length, signed = 4, 4, False
#
#
# @ST0601.add_parser
# class SensorRelativeElevationAngle(ElementParser):
#     tag, name = 19, "Sensor Relative Elevation Angle"
#     min_value, max_value, units = -180, +180, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class SensorRelativeRollAngle(ElementParser):
#     tag, name = 20, "Sensor Relative Roll Angle"
#     min_value, max_value, units = 0, +360, 'degrees'
#     min_length, max_length, signed = 4, 4, False
#
#
# @ST0601.add_parser
# class SlantRange(ElementParser):
#     tag, name = 21, "Slant Range"
#     min_value, max_value, units = 0, +5e6, 'meters'
#     min_length, max_length, signed = 4, 4, False
#
#
# @ST0601.add_parser
# class TargetWidth(ElementParser):
#     tag, name = 22, "Target Width"
#     min_value, max_value, units = 0, +10e3, 'meters'
#     min_length, max_length, signed = 2, 2, False
#
#
# @ST0601.add_parser
# class FrameCenterLatitude(ElementParser):
#     tag, name = 23, "Frame Center Latitude"
#     min_value, max_value, units = -90, +90, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class FrameCenterLongitude(ElementParser):
#     tag, name = 24, "Frame Center Longitude"
#     min_value, max_value, units = -180, +180, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class FrameCenterElevation(ElementParser):
#     tag, name = 25, "Frame Center Elevation"
#     min_value, max_value, units = -900, +19e3, "meters"
#     min_length, max_length, signed = 2, 2, False
#
#
# @ST0601.add_parser
# class OffsetCornerLatitudePoint1(ElementParser):
#     tag, name = 26, "Offset Corner Latitude Point 1"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLongitudePoint1(ElementParser):
#     tag, name = 27, "Offset Corner Longitude Point 1"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLatitudePoint2(ElementParser):
#     tag, name = 28, "Offset Corner Latitude Point 2"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLongitudePoint2(ElementParser):
#     tag, name = 29, "Offset Corner Longitude Point 2"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLatitudePoint3(ElementParser):
#     tag, name = 30, "Offset Corner Latitude Point 3"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLongitudePoint3(ElementParser):
#     tag, name = 31, "Offset Corner Longitude Point 3"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLatitudePoint4(ElementParser):
#     tag, name = 32, "Offset Corner Latitude Point 4"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# @ST0601.add_parser
# class OffsetCornerLongitudePoint4(ElementParser):
#     tag, name = 33, "Offset Corner Longitude Point 4"
#     min_value, max_value, units = -0.075, +0.075, 'degrees'
#     min_length, max_length, signed = 2, 2, True
#
#
# # Tags 34-39 "Atmospheric Conditions"
#
# @ST0601.add_parser
# class TargetLocationLatitude(ElementParser):
#     tag, name = 40, "Target Location latitude"
#     min_value, max_value, units = -90, +90, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class TargetLocationLongitude(ElementParser):
#     tag, name = 41, "Target Location Longitude"
#     min_value, max_value, units = -180, +180, 'degrees'
#     min_length, max_length, signed = 4, 4, True
#
#
# @ST0601.add_parser
# class TargetLocationElevation(ElementParser):
#     tag, name = 42, "Target Location Elevation"
#     min_value, max_value, units = -900, +19e3, "meters"
#     min_length, max_length, signed = 2, 2, False
#
#
# # Tags 43 - 46 "Target Information"
#
# # Tag 47 "Generic Flag"