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
    min_length, max_length, signed = 2, 2, True


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
    min_length, max_length, signed = 1, 1, True


@register
class PlatformIndicatedAirspeed(MappedConverterElement):
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
    min_length, max_length, signed = 2, 2, True


@register
class SensorHorizontalFieldOfView(MappedConverterElement):
    tag, name = 16, "Sensor Horizontal Field of View"
    min_value, max_value, units = 0, +180, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class SensorVerticalFieldOfView(MappedConverterElement):
    tag, name = 17, "Sensor Vertical Field of View"
    min_value, max_value, units = 0, +180, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class SensorRelativeAzimuthAngle(MappedConverterElement):
    tag, name = 18, "Sensor Relative Azimuth Angle"
    min_value, max_value, units = 0, +360, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class SensorRelativeElevationAngle(MappedConverterElement):
    tag, name = 19, "Sensor Relative Elevation Angle"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class SensorRelativeRollAngle(MappedConverterElement):
    tag, name = 20, "Sensor Relative Roll Angle"
    min_value, max_value, units = 0, +360, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class SlantRange(MappedConverterElement):
    tag, name = 21, "Slant Range"
    min_value, max_value, units = 0, +5e6, 'meters'
    min_length, max_length, signed = 4, 4, True


@register
class TargetWidth(MappedConverterElement):
    tag, name = 22, "Target Width"
    min_value, max_value, units = 0, +10e3, 'meters'
    min_length, max_length, signed = 2, 2, True


@register
class FrameCenterLatitude(MappedConverterElement):
    tag, name = 23, "Frame Center Latitude"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class FrameCenterLongitude(MappedConverterElement):
    tag, name = 24, "Frame Center Longitude"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class FrameCenterElevation(MappedConverterElement):
    tag, name = 25, "Frame Center Elevation"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLatitudePoint1(MappedConverterElement):
    tag, name = 26, "Offset Corner Latitude Point 1"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLongitudePoint1(MappedConverterElement):
    tag, name = 27, "Offset Corner Longitude Point 1"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLatitudePoint2(MappedConverterElement):
    tag, name = 28, "Offset Corner Latitude Point 2"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLongitudePoint2(MappedConverterElement):
    tag, name = 29, "Offset Corner Longitude Point 2"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLatitudePoint3(MappedConverterElement):
    tag, name = 30, "Offset Corner Latitude Point 3"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLongitudePoint3(MappedConverterElement):
    tag, name = 31, "Offset Corner Longitude Point 3"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLatitudePoint4(MappedConverterElement):
    tag, name = 32, "Offset Corner Latitude Point 4"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class OffsetCornerLongitudePoint4(MappedConverterElement):
    tag, name = 33, "Offset Corner Longitude Point 4"
    min_value, max_value, units = -0.075, +0.075, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class IcingDetected(MappedConverterElement):
    tag, name = 34, "Icing Detected"
#     min_value, max_value, units = 0, 2, 'flag'
#     min_length, max_length, signed = 1, 1, False


@register
class WindDirection(MappedConverterElement):
    tag, name = 35, "Wind Direction"
    min_value, max_value, units = 0, +360, 'meters/second'
    min_length, max_length, signed = 2, 2, False


@register
class WindSpeed(MappedConverterElement):
    tag, name = 36, "Wind Speed"
    min_value, max_value, units = 0, +100, 'meters/second'
    min_length, max_length, signed = 2, 2, False


@register
class StaticPressure(MappedConverterElement):
    tag, name = 37, "Static Pressure"
    min_value, max_value, units = 0, +5000, 'millibar'
    min_length, max_length, signed = 2, 2, False


@register
class DensityAltitude(MappedConverterElement):
    tag, name = 38, "Density Altitude"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class OutsideAirTemperature(MappedConverterElement):
    tag, name = 39, "Outside Air Temperature"
    min_value, max_value, units = -128, +127, "degrees"
    min_length, max_length, signed = 1, 1, False


@register
class TargetLocationLatitude(MappedConverterElement):
    tag, name = 40, "Target Location latitude"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class TargetLocationLongitude(MappedConverterElement):
    tag, name = 41, "Target Location Longitude"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class TargetLocationElevation(MappedConverterElement):
    tag, name = 42, "Target Location Elevation"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class TargetTrackGateWidth(MappedConverterElement):
    tag, name = 43, "Target Track Gate Width"
    min_length, max_length, signed = 1, 1, False


@register
class TargetTrackGateHeight(MappedConverterElement):
    tag, name = 44, "Target Track Gate Height"
    min_length, max_length, signed = 1, 1, False


@register
class TargetErrorEstimateCE90(MappedConverterElement):
    tag, name = 45, "Target Error Estimate - CE90"
    min_length, max_length, signed = 2, 2, False


@register
class TargetErrorEstimateLE90(MappedConverterElement):
    tag, name = 46, "Target Error Estimate - LE90"
    min_length, max_length, signed = 1, 1, False


@register
class GenericFlagData01(StringConverterElement):
    tag, name = 47, "Generic Flag Data 01"
    min_length, max_length, signed = 2, 2, False


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


@register
class DifferentialPressure(MappedConverterElement):
    tag, name = 49, "Differential Pressure"
    min_value, max_value, units = 0, +5000, 'millibar'
    min_length, max_length, signed = 2, 2, False


@register
class PlatformAngleOfAttack(MappedConverterElement):
    tag, name = 50, "Platform Angle of Attack"
    min_value, max_value, units = -20, +20, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class PlatformVerticalSpeed(MappedConverterElement):
    tag, name = 51, "Platform Vertical Speed"
    min_value, max_value, units = -180, +180, 'meters/second'
    min_length, max_length, signed = 2, 2, True


@register
class PlatformSideslipAngle(MappedConverterElement):
    tag, name = 52, "Platform Sideslip Angle"
    min_value, max_value, units = -20, +20, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class AirfieldBarometricPressure(MappedConverterElement):
    tag, name = 53, "Airfield Barometric Pressure"
    min_value, max_value, units = 0, +5000, "millibar"
    min_length, max_length, signed = 2, 2, False


@register
class AirfieldElevation(MappedConverterElement):
    tag, name = 54, "Airfield Elevation"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class RelativeHumidity(MappedConverterElement):
    tag, name = 55, "Relative Humidity"
    min_value, max_value, units = 0, +19e3, "%"
    min_length, max_length, signed = 1, 1, False


@register
class PlatformGroundSpeed(MappedConverterElement):
    tag, name = 56, "Platform Ground Speed"
    min_value, max_value, units = 0, +255, 'meters/second'
    min_length, max_length, signed = 1, 1, False


@register
class GroundRange(MappedConverterElement):
    tag, name = 57, "Ground Range"
    min_value, max_value, units = 0, +5000000, 'meters'
    min_length, max_length, signed = 4, 4, False


@register
class PlatformFuelRemaining(MappedConverterElement):
    tag, name = 58, "Platform Fuel Remaining"
    min_value, max_value, units = 0, +10000, 'kilograms'
    min_length, max_length, signed = 2, 2, False


@register
class PlatformCallSign(MappedConverterElement):
    tag, name = 59, "Platform Call Sign"


@register
class WeaponLoad(MappedConverterElement):
    tag, name = 60, "Weapon Load"
    min_length, max_length, signed = 2, 2, False


@register
class WeaponFired(MappedConverterElement):
    tag, name = 61, "Weapon Fired"
    min_length, max_length, signed = 1, 1, False


@register
class LaserPRFCode(MappedConverterElement):
    tag, name = 62, "Laser PRF Code"
    min_length, max_length, signed = 2, 2, False


@register
class SensorFieldOfViewName(MappedConverterElement):
    tag, name = 63, "Sensor Field of View Name"
    min_length, max_length, signed = 1, 1, False


@register
class PlatformMagneticHeading(MappedConverterElement):
    tag, name = 64, "Platform Magnetic Heading"
    min_value, max_value, units = 0, +360, 'degrees'
    min_length, max_length, signed = 2, 2, True


@register
class UASLSVersionNumber(ConverterElement):
    tag, name = 65, "UAS Datalink LS Version Number"

    # TODO: Associate max version with the version of the MISB implemented?
    min_length, max_length, signed = 1, 1, False


@register
class AlternatePlatformLatitude(MappedConverterElement):
    tag, name = 67, "Alternate Platform Latitude"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class AlternatePlatformLongitude(MappedConverterElement):
    tag, name = 68, "Alternate Platform Longitude"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class AlternatePlatformAltitude(MappedConverterElement):
    tag, name = 69, "Alternate Platform Altitude"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class AlternatePlatformName(MappedConverterElement):
    tag, name = 70, "Alternate Platform Name"
    min_length, max_length = 0, 127


@register
class AlternatePlatformHeading(MappedConverterElement):
    tag, name = 71, "Alternate Platform Heading"
    min_value, max_value, units = 0, +360, 'degrees'
    min_length, max_length, signed = 2, 2, False


@register
class EventStartTime(DateConverterElement):
    tag, name = 72, "Event Start Time - UTC"
    min_value, max_value, units = datetime.utcfromtimestamp(0), \
                                  datetime.max, 'microseconds'
    min_length, max_length, signed = 8, 8, False


@register
class RVTLocalSet(StringConverterElement):
    tag, name = 73, "RVT Local Set"


@register
class VMTILocalSet(StringConverterElement):
    tag, name = 74, "VMTI Local Set"


@register
class SensorEllipsoidHeightConversion(MappedConverterElement):
    tag, name = 75, "Sensor Ellipsoid Height"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, True


@register
class AlternatePlatformEllipsoidHeight(MappedConverterElement):
    tag, name = 76, "Alternate Platform Ellipsoid Height"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class OperationalMode(StringConverterElement):
    tag, name = 77, "Operational Mode"
    min_length, max_length, signed = 1, 1, False


@register
class FrameCenterHeightAboveEllipsoid(MappedConverterElement):
    tag, name = 78, "Frame Center Height Above Ellipsoid"
    min_value, max_value, units = -900, +19e3, "meters"
    min_length, max_length, signed = 2, 2, False


@register
class SensorNorthVelocity(MappedConverterElement):
    tag, name = 79, "Sensor North Velocity"
    min_value, max_value, units = -327, +327, "meters/second"
    min_length, max_length, signed = 2, 2, True


@register
class SensorEastVelocity(MappedConverterElement):
    tag, name = 80, "Sensor East Velocity"
    min_value, max_value, units = -327, +327, "meters/second"
    min_length, max_length, signed = 2, 2, True

# Tag 81 (0x51) Image Horizon Pixel Pack
# @register
# class ImageHorizonPixelPack(MappedConverterElement):
#     tag, name = 81, "Image Horizon Pixel Pack"


@register
class CornerLatitudePoint1Full(MappedConverterElement):
    tag, name = 82, "Corner Latitude Point 1 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class CornerLongitudePoint1Full(MappedConverterElement):
    tag, name = 83, "Corner Longitude Point 1 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False

@register
class CornerLatitudePoint2Full(MappedConverterElement):
    tag, name = 84, "Corner Latitude Point 2 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class CornerLongitudePoint2Full(MappedConverterElement):
    tag, name = 85, "Corner Longitude Point 2 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class CornerLatitudePoint3Full(MappedConverterElement):
    tag, name = 86, "Corner Latitude Point 3 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class CornerLongitudePoint3Full(MappedConverterElement):
    tag, name = 87, "Corner Longitude Point 3 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False

@register
class CornerLatitudePoint4Full(MappedConverterElement):
    tag, name = 88, "Corner Latitude Point 4 (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class CornerLongitudePoint4Full(MappedConverterElement):
    tag, name = 89, "Corner Longitude Point 4 (Full)"
    min_value, max_value, units = -180, +180, 'degrees'
    min_length, max_length, signed = 4, 4, False


@register
class PlatformPitchAngleFull(MappedConverterElement):
    tag, name = 90, "Platform Pitch Angle (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class PlatformRollAngleFull(MappedConverterElement):
    tag, name = 91, "Platform Roll Angle (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class PlatformAngleOfAttackFull(MappedConverterElement):
    tag, name = 92, "Platform Angle of Attack (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True


@register
class PlatformSideslipAngleFull(MappedConverterElement):
    tag, name = 93, "Platform Sideslip Angle (Full)"
    min_value, max_value, units = -90, +90, 'degrees'
    min_length, max_length, signed = 4, 4, True

@register
class MIISCoreIdentifier(object):
    tag, name = 94, "MIIS Core Identifier"

    def converter(self, item):
        return self._bytes_to_hex_dump(item.value)


# # Tag 95 (0x5F) SAR Motion Imagery (MISB ST 1206) Local Set
# @register
# class SARMotionImageryLocalSet(MappedConverterElement):


@register
class TargetWidthExtended(MappedConverterElement):
    tag, name = 96, "Target Width Extended"
    min_value, max_value, units = 0, +500000, 'meters'


# # Tag 97 (0x61) Range Image (MISB ST 1002) Local Set
# @register
# class RangeImageLocalSet(MappedConverterElement):
# # Tag 98 (0x62) Geo-Registration (MISB ST 1601) Local Set
# @register
# class GeoRegistrationLocalSet(MappedConverterElement):
# # Tag 100 (0x64) Segment (MISB ST 1607) Local Set
# @register
# class SegmentLocalSet(MappedConverterElement):
# # Tag 101 (0x65) Amend (MISB ST 1607) Local Set
# @register
# class AmendLocalSet(MappedConverterElement):
# # Tag 102 (0x66) SDCC-FLP (MISB ST 1010)
# @register
# class SDCCFLP(MappedConverterElement):


@register
class DensityAltitudeExtended(StringConverterElement):
    tag, name = 103, "Density Altitude Extended"


@register
class SensorEllipsoidHeightExtended(StringConverterElement):
    tag, name = 104, "Sensor Ellipsoid Height Extended"


@register
class AlternatePlatformEllipsoidHeightExtended(StringConverterElement):
    tag, name = 105, "Alternate Platform Ellipsoid Height Extended"
