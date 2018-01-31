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
    min_length, max_length = 0, 127

@UASLocalMetadataSet.add_parser
class PlatformTailNumber(StringElementParser):
    key = b'\x04'
    min_length, max_length = 0, 127


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
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformIndicatedAirspeed(MappedElementParser):
    key = b'\x09'
    _domain = (0, 2**8-1)
    _range = (0, 255)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformDesignation(StringElementParser):
    key = b'\x0A'
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class ImageSourceSensor(StringElementParser):
    key = b'\x0B'
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class ImageCoordinateSystem(StringElementParser):
    key = b'\x0C'
    min_length, max_length = 0, 127


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


@UASLocalMetadataSet.add_parser
class TargetWidth(MappedElementParser):
    key = b'\x16'
    _domain = (0, 2**16-1)
    _range = (0, +10e3)
    units = 'meters'


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


@UASLocalMetadataSet.add_parser
class IcingDetected(StringElementParser):
    key = b'\x22'
    units = 'flag'


@UASLocalMetadataSet.add_parser
class WindDirection(MappedElementParser):
    key = b'\x23'
    _domain = (0, 2**16 - 1)
    _range = (0, +360)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class WindSpeed(MappedElementParser):
    key = b'\x24'
    _domain = (0, 255)
    _range = (0, +100)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class StaticPressure(MappedElementParser):
    key = b'\x25'
    _domain = (0, 2**16 - 1)
    _range = (0, +5000)
    units = 'millibar'


@UASLocalMetadataSet.add_parser
class DensityAltitude(MappedElementParser):
    key = b'\x26'
    _domain = (0, 2**16 - 1)
    _range = (-900, +19e3)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class OutsideAirTemperature(MappedElementParser):
    key = b'\x27'


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


@UASLocalMetadataSet.add_parser
class TargetTrackGateWidth(MappedElementParser):
    key = b'\x2B'
    units = 'pixels'


@UASLocalMetadataSet.add_parser
class TargetTrackGateHeight(MappedElementParser):
    key = b'\x2C'
    units = 'pixels'


@UASLocalMetadataSet.add_parser
class TargetErrorEstimateCE90(MappedElementParser):
    key = b'\x2D'
    units = 'meters'


@UASLocalMetadataSet.add_parser
class TargetErrorEstimateLE90(MappedElementParser):
    key = b'\x2E'
    units = 'meters'


@UASLocalMetadataSet.add_parser
class GenericFlagData01(StringElementParser):
    key = b'\x2F'


# @UASLocalMetadataSet.add_parser
# class SecurityLocalMetadataSet(MappedElementParser):
#     key = b'\x30'


@UASLocalMetadataSet.add_parser
class DifferentialPressure(MappedElementParser):
    key = b'\x31'
    _domain = (0, 2**16-1)
    _range = (0, 5000)
    units = 'millibar'


@UASLocalMetadataSet.add_parser
class PlatformAngleOfAttack(MappedElementParser):
    key = b'\x32'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-20, 20)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformVerticalSpeed(MappedElementParser):
    key = b'\x33'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-180, 180)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformSideslipAngle(MappedElementParser):
    key = b'\x34'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-20, 20)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AirfieldBarometricPressure(MappedElementParser):
    key = b'\x35'
    _domain = (0, 2**16-1)
    _range = (0, 5000)
    units = 'millibar'


@UASLocalMetadataSet.add_parser
class AirfieldElevation(MappedElementParser):
    key = b'\x36'
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class RelativeHumidity(MappedElementParser):
    key = b'\x37'
    _domain = (0, 2**8-1)
    _range = (0, 100)
    units = '%'


@UASLocalMetadataSet.add_parser
class PlatformGroundSpeed(MappedElementParser):
    key = b'\x38'
    _domain = (0, 2**8-1)
    _range = (0, 255)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class GroundRange(MappedElementParser):
    key = b'\x39'
    _domain = (0, 2**32-1)
    _range = (0, 5000000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class PlatformFuelRemaining(MappedElementParser):
    key = b'\x3A'
    _domain = (0, 2**16-1)
    _range = (0, 10000)
    units = 'kilograms'


@UASLocalMetadataSet.add_parser
class PlatformCallSign(StringElementParser):
    key = b'\x3B'


@UASLocalMetadataSet.add_parser
class WeaponLoad(MappedElementParser):
    key = b'\x3C'


@UASLocalMetadataSet.add_parser
class WeaponFired(MappedElementParser):
    key = b'\x3D'


@UASLocalMetadataSet.add_parser
class LaserPRFCode(MappedElementParser):
    key = b'\x3E'


@UASLocalMetadataSet.add_parser
class SensorFieldOfViewName(MappedElementParser):
    key = b'\x3F'


@UASLocalMetadataSet.add_parser
class PlatformMagneticHeading(MappedElementParser):
    key = b'\x40'
    _domain = (0, 2**16-1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AlternatePlatformLatitude(MappedElementParser):
    key = b'\x43'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AlternatePlatformLongitude(MappedElementParser):
    key = b'\x44'
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AlternatePlatformAltitude(MappedElementParser):
    key = b'\x45'
    _domain = (0, 2**16 - 1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class AlternatePlatformName(StringElementParser):
    key = b'\x46'
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class AlternatePlatformHeading(MappedElementParser):
    key = b'\x47'
    _domain = (0, 2**16 - 1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class EventStartTime(DateTimeElementParser):
    key = b'\x48'


@UASLocalMetadataSet.add_parser
class RVTLocalSet(MappedElementParser):
    key = b'\x49'


@UASLocalMetadataSet.add_parser
class VMTILocalSet(MappedElementParser):
    key = b'\x4A'


@UASLocalMetadataSet.add_parser
class SensorEllipsoidHeightConversion(MappedElementParser):
    key = b'\x4B'
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class AlternatePlatformEllipsoidHeight(MappedElementParser):
    key = b'\x4C'
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class OperationalMode(StringElementParser):
    key = b'\x4D'


@UASLocalMetadataSet.add_parser
class FrameCenterHeightAboveEllipsoid(MappedElementParser):
    key = b'\x4E'
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class SensorNorthVelocity(MappedElementParser):
    key = b'\x4F'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-327, 327)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class SensorEastVelocity(MappedElementParser):
    key = b'\x50'
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-327, 327)
    units = 'meters/second'

# @UASLocalMetadataSet.add_parser
# class ImageHorizonPixelPack(MappedElementParser):
#     key = b'\x51'


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


@UASLocalMetadataSet.add_parser
class PlatformPitchAngleFull(MappedElementParser):
    key = b'\x5A'
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformRollAngleFull(MappedElementParser):
    key = b'\x5B'
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformAngleOfAttackFull(MappedElementParser):
    key = b'\x5C'
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformSideslipAngleFull(MappedElementParser):
    key = b'\x5D'
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


#@UASLocalMetadataSet.add_parser
# class MIISCoreIdentifier(MappedElementParser):
#     key = b'\x5E'


#@UASLocalMetadataSet.add_parser
# class SARMotionImageryLocalSet(MappedElementParser):
#     key = b'\x5F'


@UASLocalMetadataSet.add_parser
class TargetWidthExtended(MappedElementParser):
    key = b'\x60'
    _range = (0, +500000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class DensityAltitudeExtended(MappedElementParser):
    key = b'\x67'


@UASLocalMetadataSet.add_parser
class SensorEllipsoidHeightExtended(StringElementParser):
    key = b'\x68'


@UASLocalMetadataSet.add_parser
class AlternatePlatformEllipsoidHeightExtended(StringElementParser):
    key = b'\x69'
