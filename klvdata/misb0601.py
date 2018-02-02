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
    TAG = 1
    LSName = "Checksum"
    USName = "Checksum"


@UASLocalMetadataSet.add_parser
class PrecisionTimeStamp(DateTimeElementParser):
    """Precision Timestamp represented in microseconds.

    Precision Timestamp represented in the number of microseconds elapsed
    since midnight (00:00:00), January 1, 1970 not including leap seconds.

    See MISB ST 0603 for additional details.
    """
    key = b'\x02'
    TAG = 2
    LSName = "UNIX Time Stamp"
    USName = "User Defined Time Stamp"


@UASLocalMetadataSet.add_parser
class MissionID(StringElementParser):
    """Mission ID is the descriptive mission identifier.

    Mission ID value field free text with maximum of 127 characters
    describing the event.
    """
    key = b'\x03'
    TAG = 3
    LSName = "Mission ID"
    USName = "Episode Number"
    min_length, max_length = 0, 127

@UASLocalMetadataSet.add_parser
class PlatformTailNumber(StringElementParser):
    key = b'\x04'
    TAG = 4
    LSName = "Platform Tail Number"
    USName = "Platform Tail Number"
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class PlatformHeadingAngle(MappedElementParser):
    key = b'\x05'
    TAG = 5
    LSName = "Platform Heading Angle"
    USName = "Platform Heading Angle"
    _domain = (0, 2**16-1)
    _range = (0, 360)


@UASLocalMetadataSet.add_parser
class PlatformPitchAngle(MappedElementParser):
    key = b'\x06'
    TAG = 6
    LSName = "Platform Pitch Angle"
    USName = "Platform Pitch Angle"
    _domain = (-(2**15-1), 2**15-1)
    _range = (-20, 20)


@UASLocalMetadataSet.add_parser
class PlatformRollAngle(MappedElementParser):
    key = b'\x07'
    TAG = 7
    LSName = "Platform Roll Angle"
    USName = "Platform Roll Angle"
    _domain = (-(2**15-1), 2**15-1)
    _range = (-50, 50)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformTrueAirspeed(MappedElementParser):
    key = b'\x08'
    TAG = 8
    LSName = "Platform True Airspeed"
    USName = "Platform True Airspeed"
    _domain = (0, 2**8-1)
    _range = (0, 255)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformIndicatedAirspeed(MappedElementParser):
    key = b'\x09'
    TAG = 9
    LSName = "Platform Indicated Airspeed"
    USName = "Platform Indicated Airspeed"
    _domain = (0, 2**8-1)
    _range = (0, 255)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformDesignation(StringElementParser):
    key = b'\x0A'
    TAG = 10
    LSName = "Platform Designation"
    USName = "Device Designation"
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class ImageSourceSensor(StringElementParser):
    key = b'\x0B'
    TAG = 11
    LSName = "Image Source Sensor"
    USName = "Image Source Device"
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class ImageCoordinateSystem(StringElementParser):
    key = b'\x0C'
    TAG = 12
    LSName = "Image Coordinate System"
    USName = "Image Coordinate System"
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class SensorLatitude(MappedElementParser):
    key = b'\x0D'
    TAG = 13
    LSName = "Sensor Latitude"
    USName = "Device Latitude"
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorLongitude(MappedElementParser):
    key = b'\x0E'
    TAG = 14
    LSName = "Sensor Longitude"
    USName = "Device Longitude"
    _domain = (-(2**31-1), 2**31-1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorTrueAltitude(MappedElementParser):
    key = b'\x0F'
    TAG = 15
    LSName = "Sensor True Altitude"
    USName = "Device Altitude"
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class SensorHorizontalFieldOfView(MappedElementParser):
    key = b'\x10'
    TAG = 16
    LSName = "Sensor Horizontal Field of View"
    USName = "Field of View (FOVHorizontal)"
    _domain = (0, 2**16-1)
    _range = (0, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorVerticalFieldOfView(MappedElementParser):
    key = b'\x11'
    TAG = 17
    LSName = "Sensor Vertical Field of View"
    USName = "Field of View (FOVVertical)"
    _domain = (0, 2**16-1)
    _range = (0, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorRelativeAzimuthAngle(MappedElementParser):
    key = b'\x12'
    TAG = 18
    LSName = "Sensor Relative Azimuth Angle"
    USName = "Sensor Relative Azimuth Angle"
    _domain = (0, 2**32-1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorRelativeElevationAngle(MappedElementParser):
    key = b'\x13'
    TAG = 19
    LSName = "Sensor Relative Elevation Angle"
    USName = "Sensor Relative Elevation Angle"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SensorRelativeRollAngle(MappedElementParser):
    key = b'\x14'
    TAG = 20
    LSName = "Sensor Relative Roll Angle"
    USName = "Sensor Relative Roll Angle"
    _domain = (0, 2**32-1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class SlantRange(MappedElementParser):
    key = b'\x15'
    TAG = 21
    LSName = "Slant Range"
    USName = "Slant Range"
    _domain = (0, 2**32-1)
    _range = (0, +5e6)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class TargetWidth(MappedElementParser):
    key = b'\x16'
    TAG = 22
    LSName = "Target Width"
    USName = "Target Width"
    _domain = (0, 2**16-1)
    _range = (0, +10e3)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class FrameCenterLatitude(MappedElementParser):
    key = b'\x17'
    TAG = 23
    LSName = "Frame Center Latitude"
    USName = "Frame Center Latitude"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class FrameCenterLongitude(MappedElementParser):
    key = b'\x18'
    TAG = 24
    LSName = "Frame Center Longitude"
    USName = "Frame Center Longitude"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class FrameCenterElevation(MappedElementParser):
    key = b'\x19'
    TAG = 25
    LSName = "Frame Center Elevation"
    USName = "Frame Center Elevation"
    _domain = (0, 2**16-1)
    _range = (-900, +19e3)
    units = 'meters'

 
@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint1(MappedElementParser):
    key = b'\x1A'
    TAG = 26
    LSName = "Offset Corner Latitude Point 1"
    USName = "Corner Latitude Point 1"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, +0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint1(MappedElementParser):
    key = b'\x1B'
    TAG = 27
    LSName = "Offset Corner Longitude Point 1"
    USName = "Corner Longitude Point 1"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint2(MappedElementParser):
    key = b'\x1C'
    TAG = 28
    LSName = "Offset Corner Latitude Point 2"
    USName = "Corner Latitude Point 2"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint2(MappedElementParser):
    key = b'\x1D'
    TAG = 29
    LSName = "Offset Corner Longitude Point 2"
    USName = "Corner Longitude Point 2"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint3(MappedElementParser):
    key = b'\x1E'
    TAG = 30
    LSName = "Offset Corner Latitude Point 3"
    USName = "Corner Latitude Point 3"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint3(MappedElementParser):
    key = b'\x1F'
    TAG = 31
    LSName = "Offset Corner Longitude Point 3"
    USName = "Corner Longitude Point 3"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLatitudePoint4(MappedElementParser):
    key = b'\x20'
    TAG = 32
    LSName = "Offset Corner Latitude Point 4"
    USName = "Corner Latitude Point 4"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class OffsetCornerLongitudePoint4(MappedElementParser):
    key = b'\x21'
    TAG = 33
    LSName = "Offset Corner Longitude Point 4"
    USName = "Corner Longitude Point 4"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-0.075, 0.075)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class IcingDetected(StringElementParser):
    key = b'\x22'
    TAG = 34
    LSName = "Icing Detected"
    USName = "Icing Detected"
    units = 'flag'


@UASLocalMetadataSet.add_parser
class WindDirection(MappedElementParser):
    key = b'\x23'
    TAG = 35
    LSName = "Wind Direction"
    USName = "Wind Direction"
    _domain = (0, 2**16 - 1)
    _range = (0, +360)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class WindSpeed(MappedElementParser):
    key = b'\x24'
    TAG = 36
    LSName = "Wind Speed"
    USName = "Wind Speed"
    _domain = (0, 255)
    _range = (0, +100)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class StaticPressure(MappedElementParser):
    key = b'\x25'
    TAG = 37
    LSName = "Static Pressure"
    USName = "Static Pressure"
    _domain = (0, 2**16 - 1)
    _range = (0, +5000)
    units = 'millibar'


@UASLocalMetadataSet.add_parser
class DensityAltitude(MappedElementParser):
    key = b'\x26'
    TAG = 38
    LSName = "Density Altitude"
    USName = "Density Altitude"
    _domain = (0, 2**16 - 1)
    _range = (-900, +19e3)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class OutsideAirTemperature(MappedElementParser):
    key = b'\x27'
    TAG = 39
    LSName = "Outside Air Temperature"
    USName = "Outside Air Temperature"


@UASLocalMetadataSet.add_parser
class TargetLocationLatitude(MappedElementParser):
    key = b'\x28'
    TAG = 40
    LSName = "Target Location Latitude"
    USName = "Target Location Latitude"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class TargetLocationLongitude(MappedElementParser):
    key = b'\x29'
    TAG = 41
    LSName = "Target Location Longitude"
    USName = "Target Location Longitude"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class TargetLocationElevation(MappedElementParser):
    key = b'\x2A'
    TAG = 42
    LSName = "Target Location Elevation"
    USName = "Target Location Elevation"
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class TargetTrackGateWidth(MappedElementParser):
    key = b'\x2B'
    TAG = 43
    LSName = "Target Track Gate Width"
    USName = "Target Track Gate Width"
    units = 'pixels'


@UASLocalMetadataSet.add_parser
class TargetTrackGateHeight(MappedElementParser):
    key = b'\x2C'
    TAG = 44
    LSName = "Target Track Gate Height"
    USName = "Target Track Gate Height"
    units = 'pixels'


@UASLocalMetadataSet.add_parser
class TargetErrorEstimateCE90(MappedElementParser):
    key = b'\x2D'
    TAG = 45
    LSName = "Target Error Estimate - CE90"
    USName = "Target Error Estimate - CE90"
    units = 'meters'


@UASLocalMetadataSet.add_parser
class TargetErrorEstimateLE90(MappedElementParser):
    key = b'\x2E'
    TAG = 46
    LSName = "Target Error Estimate - LE90"
    USName = "Target Error Estimate - LE90"
    units = 'meters'


@UASLocalMetadataSet.add_parser
class GenericFlagData01(StringElementParser):
    key = b'\x2F'
    TAG = 47
    LSName = "Generic Flag Data 01"
    USName = "Generic Flag Data 01"


# @UASLocalMetadataSet.add_parser
# class SecurityLocalMetadataSet(MappedElementParser):
#     key = b'\x30'
#     TAG = 48
#     LSName = "Security Local Metadata Set"
#     USName = "Security Local Metadata Set"


@UASLocalMetadataSet.add_parser
class DifferentialPressure(MappedElementParser):
    key = b'\x31'
    TAG = 49
    LSName = "Differential Pressure"
    USName = "Differential Pressure"
    _domain = (0, 2**16-1)
    _range = (0, 5000)
    units = 'millibar'


@UASLocalMetadataSet.add_parser
class PlatformAngleOfAttack(MappedElementParser):
    key = b'\x32'
    TAG = 50
    LSName = "Platform Angle of Attack"
    USName = "Platform Angle of Attack"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-20, 20)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformVerticalSpeed(MappedElementParser):
    key = b'\x33'
    TAG = 51
    LSName = "Platform Vertical Speed"
    USName = "Platform Vertical Speed"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-180, 180)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class PlatformSideslipAngle(MappedElementParser):
    key = b'\x34'
    TAG = 52
    LSName = "Platform Sideslip Angle"
    USName = "Platform Sideslip Angle"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-20, 20)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AirfieldBarometricPressure(MappedElementParser):
    key = b'\x35'
    TAG = 53
    LSName = "Airfield Barometric Pressure"
    USName = "Airfield Barometric Pressure"
    _domain = (0, 2**16-1)
    _range = (0, 5000)
    units = 'millibar'


@UASLocalMetadataSet.add_parser
class AirfieldElevation(MappedElementParser):
    key = b'\x36'
    TAG = 54
    LSName = "Airfield Elevation"
    USName = "Airfield Elevation"
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class RelativeHumidity(MappedElementParser):
    key = b'\x37'
    TAG = 55
    LSName = "Relative Humidity"
    USName = "Relative Humidity"
    _domain = (0, 2**8-1)
    _range = (0, 100)
    units = '%'


@UASLocalMetadataSet.add_parser
class PlatformGroundSpeed(MappedElementParser):
    key = b'\x38'
    TAG = 56
    LSName = "Platform Ground Speed"
    USName = "Platform Ground Speed"
    _domain = (0, 2**8-1)
    _range = (0, 255)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class GroundRange(MappedElementParser):
    key = b'\x39'
    TAG = 57
    LSName = "Ground Range"
    USName = "Ground Range"
    _domain = (0, 2**32-1)
    _range = (0, 5000000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class PlatformFuelRemaining(MappedElementParser):
    key = b'\x3A'
    TAG = 58
    LSName = "Platform Fuel Remaining"
    USName = "Platform Fuel Remaining"
    _domain = (0, 2**16-1)
    _range = (0, 10000)
    units = 'kilograms'


@UASLocalMetadataSet.add_parser
class PlatformCallSign(StringElementParser):
    key = b'\x3B'
    TAG = 59
    LSName = "Platform Call Sign"
    USName = "Platform Call Sign"


@UASLocalMetadataSet.add_parser
class WeaponLoad(MappedElementParser):
    key = b'\x3C'
    TAG = 60
    LSName = "Weapon Load"
    USName = "Weapon Load"


@UASLocalMetadataSet.add_parser
class WeaponFired(MappedElementParser):
    key = b'\x3D'
    TAG = 61
    LSName = "Weapon Fired"
    USName = "Weapon Fired"

@UASLocalMetadataSet.add_parser
class LaserPRFCode(MappedElementParser):
    key = b'\x3E'
    TAG = 62
    LSName = "Laser PRF Code"
    USName = "Laser PRF Code"


@UASLocalMetadataSet.add_parser
class SensorFieldOfViewName(MappedElementParser):
    key = b'\x3F'
    TAG = 63
    LSName = "Sensor Field of View Name"
    USName = "Sensor Field of View Name"


@UASLocalMetadataSet.add_parser
class PlatformMagneticHeading(MappedElementParser):
    key = b'\x40'
    TAG = 64
    LSName = "Platform Magnetic Heading"
    USName = "Platform Magnetic Heading"
    _domain = (0, 2**16-1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AlternatePlatformLatitude(MappedElementParser):
    key = b'\x43'
    TAG = 67
    LSName = "Alternate Platform Latitude"
    USName = "Alternate Platform Latitude"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AlternatePlatformLongitude(MappedElementParser):
    key = b'\x44'
    TAG = 68
    LSName = "Alternate Platform Longitude"
    USName = "Alternate Platform Longitude"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class AlternatePlatformAltitude(MappedElementParser):
    key = b'\x45'
    TAG = 69
    LSName = "Alternate Platform Altitude"
    USName = "Alternate Platform Altitude"
    _domain = (0, 2**16 - 1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class AlternatePlatformName(StringElementParser):
    key = b'\x46'
    TAG = 70
    LSName = "Alternate Platform Name"
    USName = "Alternate Platform Name"
    min_length, max_length = 0, 127


@UASLocalMetadataSet.add_parser
class AlternatePlatformHeading(MappedElementParser):
    key = b'\x47'
    TAG = 71
    LSName = "Alternate Platform Heading"
    USName = "Alternate Platform Heading"
    _domain = (0, 2**16 - 1)
    _range = (0, 360)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class EventStartTime(DateTimeElementParser):
    key = b'\x48'
    TAG = 72
    LSName = "Event Start Time - UTC"
    USName = "Event Start Time - UTC"


@UASLocalMetadataSet.add_parser
class RVTLocalSet(MappedElementParser):
    key = b'\x49'
    TAG = 73
    LSName = "RVT Local Data Set"
    USName = "Remote Video Terminal Local Data Set"


@UASLocalMetadataSet.add_parser
class VMTILocalSet(MappedElementParser):
    key = b'\x4A'
    TAG = 74
    LSName = ""
    USName = ""



@UASLocalMetadataSet.add_parser
class SensorEllipsoidHeightConversion(MappedElementParser):
    key = b'\x4B'
    TAG = 75
    LSName = "Sensor Ellipsoid Height"
    USName = "Sensor Ellipsoid Height"
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class AlternatePlatformEllipsoidHeight(MappedElementParser):
    key = b'\x4C'
    TAG = 76
    LSName = "Alternate Platform Ellipsoid Height"
    USName = "Alternate Platform Ellipsoid Height"
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class OperationalMode(StringElementParser):
    key = b'\x4D'
    TAG = 77
    LSName = "Operational Mode"
    USName = "Operational Mode"



@UASLocalMetadataSet.add_parser
class FrameCenterHeightAboveEllipsoid(MappedElementParser):
    key = b'\x4E'
    TAG = 78
    LSName = "Frame Center Height Above Ellipsoid"
    USName = "Frame Center Height Above Ellipsoid"
    _domain = (0, 2**16-1)
    _range = (-900, 19000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class SensorNorthVelocity(MappedElementParser):
    key = b'\x4F'
    TAG = 79
    LSName = "Sensor North Velocity"
    USName = "Sensor North Velocity"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-327, 327)
    units = 'meters/second'


@UASLocalMetadataSet.add_parser
class SensorEastVelocity(MappedElementParser):
    key = b'\x50'
    TAG = 80
    LSName = "Sensor East Velocity"
    USName = "Sensor East Velocity"
    _domain = (-(2**15 - 1), 2**15 - 1)
    _range = (-327, 327)
    units = 'meters/second'

# @UASLocalMetadataSet.add_parser
# class ImageHorizonPixelPack(MappedElementParser):
#     key = b'\x51'
#     TAG = 81
#     LSName = "Image Horizon Pixel Pack"
#     USName = "Image Horizon Pixel Pack"



@UASLocalMetadataSet.add_parser
class CornerLatitudePoint1Full(MappedElementParser):
    key = b'\x52'
    TAG = 82
    LSName = "Corner Latitude Point 1 (Full)"
    USName = "Corner Latitude Point 1 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint1Full(MappedElementParser):
    key = b'\x53'
    TAG = 83
    LSName = "Corner Longitude Point 1 (Full)"
    USName = "Corner Longitude Point 1 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint2Full(MappedElementParser):
    key = b'\x54'
    TAG = 84
    LSName = "Corner Latitude Point 2 (Full)"
    USName = "Corner Latitude Point 2 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint2Full(MappedElementParser):
    key = b'\x55'
    TAG = 85
    LSName = "Corner Longitude Point 2 (Full)"
    USName = "Corner Longitude Point 2 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint3Full(MappedElementParser):
    key = b'\x56'
    TAG = 86
    LSName = "Corner Latitude Point 3 (Full)"
    USName = "Corner Latitude Point 3 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint3Full(MappedElementParser):
    key = b'\x57'
    TAG = 87
    LSName = "Corner Longitude Point 3 (Full)"
    USName = "Corner Longitude Point 3 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLatitudePoint4Full(MappedElementParser):
    key = b'\x58'
    TAG = 88
    LSName = "Corner Latitude Point 4 (Full)"
    USName = "Corner Latitude Point 4 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class CornerLongitudePoint4Full(MappedElementParser):
    key = b'\x59'
    TAG = 89
    LSName = "Corner Longitude Point 4 (Full)"
    USName = "Corner Longitude Point 4 (Decimal Degrees)"
    _domain = (-(2**31 - 1), 2**31 - 1)
    _range = (-180, 180)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformPitchAngleFull(MappedElementParser):
    key = b'\x5A'
    TAG = 90
    LSName = "Platform Pitch Angle (Full)"
    USName = "Platform Pitch Angle"
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformRollAngleFull(MappedElementParser):
    key = b'\x5B'
    TAG = 91
    LSName = "Platform Roll Angle (Full)"
    USName = "Platform Roll Angle"
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformAngleOfAttackFull(MappedElementParser):
    key = b'\x5C'
    TAG = 92
    LSName = "Platform Angle of Attack (Full)"
    USName = "Platform Angle of Attack"
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


@UASLocalMetadataSet.add_parser
class PlatformSideslipAngleFull(MappedElementParser):
    key = b'\x5D'
    TAG = 93
    LSName = "Platform Sideslip Angle (Full)"
    USName = "Platform Sideslip Angle"
    _domain = (-(2**31-1), 2**31-1)
    _range = (-90, 90)
    units = 'degrees'


#@UASLocalMetadataSet.add_parser
# class MIISCoreIdentifier(MappedElementParser):
#     key = b'\x5E'
#     TAG = 94
#     LSName = "MIIS Core Identifier"
#     USName = "Motion Imagery Identification System Core"


#@UASLocalMetadataSet.add_parser
# class SARMotionImageryLocalSet(MappedElementParser):
#     key = b'\x5F'
#     TAG = 95
#     LSName = "SAR Motion Imagery Local Set"
#     USName = "SAR Motion Imagery Local Set"



@UASLocalMetadataSet.add_parser
class TargetWidthExtended(MappedElementParser):
    key = b'\x60'
    TAG = 96
    LSName = "Target Width Extended"
    USName = "Target Width"
    _range = (0, +500000)
    units = 'meters'


@UASLocalMetadataSet.add_parser
class DensityAltitudeExtended(MappedElementParser):
    key = b'\x67'
    TAG = 103
    LSName = "Density Altitude Extended"
    USName = ""


@UASLocalMetadataSet.add_parser
class SensorEllipsoidHeightExtended(StringElementParser):
    key = b'\x68'
    TAG = 104
    LSName = "Sensor Ellipsoid Height Extended"
    USName = ""


@UASLocalMetadataSet.add_parser
class AlternatePlatformEllipsoidHeightExtended(StringElementParser):
    key = b'\x69'
    TAG = 105
    LSName = " Alternate Platform Ellipsoid Height Extended"
    USName = ""
