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

from klvdata.common import hexstr_to_bytes
from klvdata.element import UnknownElement
from klvdata.elementparser import BytesElementParser
from klvdata.elementparser import DateTimeElementParser
from klvdata.elementparser import MappedElementParser
from klvdata.elementparser import StringElementParser
from klvdata.setparser import SetParser
from klvdata.streamparser import StreamParser


class UnknownElement(UnknownElement):
    pass


@StreamParser.add_parser
class UASLocalMetadataSet(SetParser):
    """MISB ST0601 UAS Local Metadata Set
    """
    key = hexstr_to_bytes('06 0E 2B 34 - 02 0B 01 01 – 0E 01 03 01 - 01 00 00 00')
    name = 'UAS Datalink Local Set'

    parsers = {}

    _unknown_element = UnknownElement



@UASLocalMetadataSet.add_parser
class Checksum(BytesElementParser):
    """Checksum used to detect errors within a UAV Local Set packet.

    Checksum formed as lower 16-bits of summation performed on entire
    LS packet, including 16-byte US key and 1-byte checksum length.

    Initialized from bytes value as BytesValue.
    """
    key = b'\x01'


@UASLocalMetadataSet.add_parser
class PrecisionTimeStamp(DateTimeElementParser):
    """Precision Timestamp represented in microseconds.

    Precision Timestamp represented in the number of microseconds elapsed
    since midnight (00:00:00), January 1, 1970 not including leap seconds.

    See MISB ST 0603 for additional details.
    """
    key = b'\x02'


@UASLocalMetadataSet.add_parser
class MissionID(StringElementParser):
    """Mission ID is the descriptive mission identifier.

    Mission ID value field free text with maximum of 127 characters
    describing the event.
    """
    key = b'\x03'


@UASLocalMetadataSet.add_parser
class PlatformTailNumber(StringElementParser):
    key = b'\x04'


@UASLocalMetadataSet.add_parser
class PlatformHeadingAngle(MappedElementParser):
    key = b'\x05'
    _domain = (0, 2**16-1)
    _range = (0, 360)


@UASLocalMetadataSet.add_parser
class PlatformPitchAngle(MappedElementParser):
    key = b'\x06'
    _domain = (-(2**15-1), 2**15-1)
    _range = (-20, 20)


@UASLocalMetadataSet.add_parser
class PlatformRollAngle(MappedElementParser):
    key = b'\x07'
    _domain = (-(2**15-1), 2**15-1)
    _range = (-50, 50)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformTrueAirspeed(MappedElementParser):
    key = b'\x08'
    _domain = (0, 2**8-1)
    _range = (0, 255)
    # units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformIndicatedAirspeed(MappedElementParser):
    key = b'\x09'
    _domain = (0, 2**8-1)
    _range = (0, 255)
    # units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformDesignation(StringElementParser):
    key = b'\x0A'
    # min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class ImageSourceSensor(StringElementParser):
    key = b'\x0B'
    # min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class ImageCoordinateSystem(StringElementParser):
    key = b'\x0C'
    # min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class SensorLatitude(MappedElementParser):
    key = b'\x0D'
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorLongitude(MappedElementParser):
    key = b'\x0E'
    _domain = (-(2**31-1), 2**31-1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorTrueAltitude(MappedElementParser):
    key = b'\x0F'
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class SensorHorizontalFieldOfView(MappedElementParser):
    key = b'\x10'
    _domain = (0, 2**16-1)
    _range = (0, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorVerticalFieldOfView(MappedElementParser):
    key = b'\x11'
    _domain = (0, 2**16-1)
    _range = (0, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorRelativeAzimuthAngle(MappedElementParser):
    key = b'\x12'
    _domain = (0, 2**32-1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorRelativeElevationAngle(MappedElementParser):
    key = b'\x13'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorRelativeRollAngle(MappedElementParser):
    key = b'\x14'
    _domain = (0, 2**32-1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SlantRange(MappedElementParser):
    key = b'\x15'
    _domain = (0, 2**32-1)
    _range = (0, +5e6)
    units = 'meters'


# @UASLocalMetadataSet.add_parser
# class TargetWidth(MappedElementParser):
#     key = b'\x16'
#     _domain = (0, 2**16-1)
#     _range = (0, +10e3)
#     units = 'meters'


@UASLocalMetadataSet.add_parser
class FrameCenterLatitude(MappedElementParser):
    key = b'\x17'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class FrameCenterLongitude(MappedElementParser):
    key = b'\x18'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class FrameCenterElevation(MappedElementParser):
    key = b'\x19'
    _domain = (0, 2**16-1)
    _range = (-900, +19e3)
    units = 'meters'

 
@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint1(MappedElementParser):
    key = b'\x1A'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, +0.075)
    units = 'degrees'
 
 
@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint1(MappedElementParser):
    key = b'\x1B'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint2(MappedElementParser):
    key = b'\x1C'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint2(MappedElementParser):
    key = b'\x1D'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint3(MappedElementParser):
    key = b'\x1E'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint3(MappedElementParser):
    key = b'\x1F'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint4(MappedElementParser):
    key = b'\x20'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint4(MappedElementParser):
    key = b'\x21'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


# # Tags 34-39 "Atmospheric Conditions"

@UASLocalMetadataSet.add_parser
class TargetLocationLatitude(MappedElementParser):
    key = b'\x28'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class TargetLocationLongitude(MappedElementParser):
    key = b'\x29'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class TargetLocationElevation(MappedElementParser):
    key = b'\x2A'
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'

# # # Tags 43 - 81


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint1Full(MappedElementParser):
    key = b'\x52'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint1Full(MappedElementParser):
    key = b'\x53'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint2Full(MappedElementParser):
    key = b'\x54'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint2Full(MappedElementParser):
    key = b'\x55'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint3Full(MappedElementParser):
    key = b'\x56'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint3Full(MappedElementParser):
    key = b'\x57'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint4Full(MappedElementParser):
    key = b'\x58'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint4Full(MappedElementParser):
    key = b'\x59'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'

# # # Tags 90 - 102
