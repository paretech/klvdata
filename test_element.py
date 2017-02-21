import unittest

from collections import namedtuple


class ElementTestCase(unittest.TestCase):
    pass


class ElementShort(ElementTestCase):
    def setUp(self):
        self.key = b'\x02'
        self.length = b'\x08'
        self.value = b'\x00\x04\x60\x50\x58\x4E\x01\x80'

        self.packet = self.key + self.length + self.value

        from element import Element
        self.element = Element(self.key, self.value)

    def test_key(self):
        self.assertEquals(self.element.key, self.key)

    def test_ber_length(self):
        from common import ber_decode
        from common import ber_encode
        self.assertEquals(ber_encode(ber_decode(self.length)), self.length)

    def test_length(self):
        self.assertEquals(self.element.length, self.length)

    def test_value(self):
        self.assertEquals(self.element.value, self.value)

    def test_bytes(self):
        self.assertEquals(bytes(self.element), self.packet)

    def test_modify_value(self):
        from datetime import datetime
        from struct import pack

        time = pack('>Q', int(datetime.utcnow().timestamp()*1e6))

        self.packet = self.key + self.length + time
        self.element.value = time

        self.assertEquals(bytes(self.element), self.packet)


class ElementLong(ElementTestCase):
    def setUp(self):
        self.key = bytes()
        self.length = bytes()
        self.value = bytes()

        with open('DynamicConstantMISMMSPacketData.bin', 'rb') as f:
            packet = f.read()

            self.key = packet[0:15]
            self.length = packet[16:18]
            self.value = packet[18:]

        self.packet = self.key + self.length + self.value

        from element import Element
        self.element = Element(self.key, self.value)

    def test_key(self):
        self.assertEquals(self.element.key, self.key)

    def test_ber_length(self):
        from common import ber_decode
        from common import ber_encode
        self.assertEquals(ber_encode(ber_decode(self.length)), self.length)

    def test_length(self):
        self.assertEquals(self.element.length, self.length)

    def test_value(self):
        self.assertEquals(self.element.value, self.value)

    def test_bytes(self):
        self.assertEquals(bytes(self.element), self.packet)


if __name__ == "__main__":
    unittest.main()
