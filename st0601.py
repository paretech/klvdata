#!/usr/bin/env python3

# Copyright 2016 Matthew Pare. All rights reserved.

import klvcms
from collections import OrderedDict
from datetime import datetime

# MISB ST0601 Tag #1
class LSChecksum(klvcms.BaseElement):
    """MISB ST0601 Checksum Parser"""
    def parser(self, item):
        self.name = 'Checksum'

        return item.value

    def __str__(self):
        return "{:2}: '{}' ({} bytes) \"{}\"".format(self.key, self.name, self.length, bytes2hexdump(self.value))

# MISB ST0601 Tag #2
class LSPrecisionTimeStamp(klvcms.BaseElement):
    """Form a MISB 0601.9 Tag=2 Precision Time Stamp Parser"""
    def parser(self, item):
        self.name = 'Precision Time Stamp'

        return datetime.utcfromtimestamp(self._bytes_to_int(item.value)*1e-6)

# MISB ST0601 Tag #3
class LSMissionID(klvcms.BaseElement):
    """Form a MISB 0601.9 Tag=3 Mission ID Parser"""
    def parser(self, item):
        self.name = 'Mission ID'

        return self._bytes_to_str(item.value)

# MISB ST0601 Tag #4
class LSPlatformTailNumber(klvcms.BaseElement):
    """Form a MISB 0601 Platform Tail Number Parser"""
    def parser(self, item):
        self.name = "Platform Tail Number"

        return self._bytes_to_str(item.value)

# MISB ST0601 Tag #5
class LSPlatformHeadingAngle(klvcms.BaseElement):
    """Form a MIST ST0601 Platform heading Angle Parser"""
    def parser(self, item):
        self.name = "Platform Heading Angle"

        min_value = 0 #degrees
        max_value = 360 #degrees

        return self._scale_value(min_value, max_value, item.value, signed=True)

# MIST ST0601 Tag #6
class LSPlatformPitchAngle(klvcms.BaseElement):
    """Form a MISB ST0601 Platform Pitch Angle Parser"""
    def parser(self, item):
        self.name = "Platform Pitch Angle"

        min_value = -20 #degrees
        max_value = +20 #degrees

        # TODO: Add "out of range" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

# MISB ST0601 Tag #7
class LSPlatformRollAngle(klvcms.BaseElement):
    """Form a MISB ST0601 Platform Roll Angle Parser"""
    def parser(self, item):
        self.name = "Platform Roll Angle"

        min_value = -50 #degrees
        max_value = +50 #degrees

        # TODO: Add "out of range" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

# MISB ST0601 Tag 8

# MISB ST0601 Tag 9

# MISB ST0601 Tag 10
class LSPlatformDesignation(klvcms.BaseElement):
    """Form a MISB ST0601 Platform Designation LS Tag Parser"""
    def parser(self, item):
        self.name = "Platform Designation"

        return self._bytes_to_str(item.value)

# MISB ST0601 Tag 11
class LSImageSourceSensor(klvcms.BaseElement):
    """Form a MISB ST0601 Image Source Sensor Parser"""
    def __init__(self, item):
        super().__init__(item)

        self.name = "Image Source Sensor"

    def parser(self, item):
        return self._bytes_to_str(item.value)

# MISB ST0601 Tag 12
class LSImageCoordinateSystem(klvcms.BaseElement):
    """Form a MISB ST0601 Image Coordinate System Parser"""
    def __init__(self, item):
        super().__init__(item)

        self.name = "Image Coordinate System"

    def parser(self, item):
        return self._bytes_to_str(item.value)

# MISB ST0601 Tag 13
class LSSensorLatitude(klvcms.BaseElement):
    """Form a MISB ST0601 Sensor Latitude Parser"""
    def __init__(self, item):
        super().__init__(item)

        self.name = "Sensor Latitude"

    def parser(self, item):
        min_value = -90
        max_value = +90

        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

# MISB ST0601 Tag 14
class LSSensorLongitude(klvcms.BaseElement):
    """Form a MISB ST0601 Sensor Longitude Parser"""
    def __init__(self, item):
        super().__init__(item)


    def parser(self, item):
        self.name = "Sensor Longitude"

        self.unites = 'degrees'

        min_value = -180
        max_value = +180

        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value, signed=True)

# MISB ST0601 Tag 15
class LSSensorTrueAltitude(klvcms.BaseElement):
    """Form a MISB ST0601 Sensor True Altitude Parser"""
    def parser(self, item):
        self.name = "Sensor True Altitude Parser"

        self.units = 'meters'
        min_value = -900
        max_value = +19000

        offset = 900

        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value) - offset

# MISB ST0601 Tag 16
class LSSensorHorizonalFieldOfView(klvcms.BaseElement):
    """Form a MISB ST0601 Sensor Horizontal Field of View Parser"""
    def parser(self, item):
        self.name = "Horizontal Field of View"

        self.units = 'degrees'
        min_value = 0
        max_value = 180


        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

# MISB ST0601 Tag 16
class LSSensorHorizontalFieldOfView(klvcms.BaseElement):
    """Form a MISB ST0601 Sensor Horizontal Field of View Parser"""
    def parser(self, item):
        self.name = "Horizontal Field of View"

        self.units = 'degrees'
        min_value = 0
        max_value = 180


        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)

# MISB ST0601 Tag 17
class LSSensorVerticalFieldOfView(klvcms.BaseElement):
    """Form a MISB ST0601 Sensor Vertical Field of View Parser"""
    def parser(self, item):
        self.name = "Vertical Field of View"

        self.units = 'degrees'
        min_value = 0
        max_value = 180


        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)


# MISB ST0601 Tag 18
class LSSensorRelativeAzimuthAngle(klvcms.BaseElement):
    """Sensor Relative Azimuth Angle Conversion"""
    def parser(self, item):
        self.name = "Sensor Relative Azimuth Angle"

        self.units = 'degrees'
        min_value = 0
        max_value = 360


        # @TODO: Implement "error" indicator
        return self._scale_value(min_value, max_value, item.value)


ST0601_tags = dict()
ST0601_tags[1] = LSChecksum
ST0601_tags[2] = LSPrecisionTimeStamp
ST0601_tags[3] = LSMissionID
ST0601_tags[4] = LSPlatformTailNumber
ST0601_tags[5] = LSPlatformHeadingAngle
ST0601_tags[6] = LSPlatformPitchAngle
ST0601_tags[7] = LSPlatformRollAngle


ST0601_tags[10] = LSPlatformDesignation
ST0601_tags[11] = LSImageSourceSensor
ST0601_tags[12] = LSImageCoordinateSystem
ST0601_tags[13] = LSSensorLatitude
ST0601_tags[14] = LSSensorLongitude
ST0601_tags[15] = LSSensorTrueAltitude
ST0601_tags[16] = LSSensorHorizontalFieldOfView
ST0601_tags[17] = LSSensorVerticalFieldOfView
ST0601_tags[18] = LSSensorRelativeAzimuthAngle

class TestParser(klvcms.BaseParser):
    def __next__(self):
        self.parse()

        return BasePacket(self)


class BasePacket(klvcms.BaseElement):
    element_parsers = dict()

    def __init__(self, item):
        klvcms.BaseElement.__init__(self, item)
        self.parse_elements()
        self.parse_nested_elements()

    def parse_elements(self):
        self.elements = OrderedDict()

        self.elements = OrderedDict((self._bytes_to_int(item.key), self._get_parser(item)(item)) for item in klvcms.BaseParser(self.value, 1))
#k        self.elements = (self._bytes_to_int(item.key), self._get_parser(item)(item)) for item in BaseParser(self.value, 1)

    def parse_nested_elements(self):
        # Add recognized element for security metadata
        # @TODO Move to MISB ST0601 parser. Does not belong in base
        # @TODO Clean up code...
        if 48 in self.elements:
            self.elements[48].elements = OrderedDict((item.key, klvcms.BaseElement(item)) for item in klvcms.BaseParser(self.elements[48].value, 1))

    def get_tags(self):
        return self.elements

    def get_tag(self, key):
        return self.get_tags()[key]

    def get_keys(self):
        return self.get_tags().keys()

    def get_items(self):
        return self.get_tags().items()

    def _get_parser(self, item):
        return ST0601_tags.get(self._bytes_to_int(item.key), klvcms.BaseElement)

# Previously named "pretty_print"
def bytes2hexdump(value):
    return " ".join(["{:02X}".format(byte) for byte in value])
