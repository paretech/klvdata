Motion Imagery Standards Board (MISB) Key Length Value (KLV) Common Metadata
System (CMS) Python Authoring and Parsing Library.

Built for Python 3.2.5 and later.

Output when run against the sample provided with MISB ST0902.5 Annex C, Table 5:
```
$ ./st0601.py DynamicConstantMISMMSPacketData.bin
```

```
02: Precision Time Stamp                8 bytes 2009-01-12 22:08:22
03: Mission ID                         10 bytes Mission 12
05: Platform Heading Angle              2 bytes 159.97436484321355
06: Platform Pitch Angle                2 bytes -0.4315317239905987
07: Platform Roll Angle                 2 bytes 3.4058656575212893
10: Platform Designation                8 bytes Predator
11: Image Source Sensor                 7 bytes EO Nose
12: Image Coordinate System            14 bytes Geodetic WGS84
13: Sensor Latitude                     4 bytes 60.176822966978335
14: Sensor Longitude                    4 bytes 128.42675904204452
15: Sensor True Altitude                2 bytes 14190.719462882427
16: Sensor Horizontal Field of View     2 bytes 144.5712977798123
17: Sensor Vertical Field of View       2 bytes 152.64362554360267
18: Sensor Relative Azimuth Angle       4 bytes 160.71921143697557
19: Sensor Relative Elevation Angle     4 bytes -168.79232483394085
20: Sensor Relative Roll Angle          4 bytes 176.86543764939194
21: Slant Range                         4 bytes 68590.98329874477
22: Target Width                        2 bytes 722.8198672465096
23: Frame Center Latitude               4 bytes -10.542388633146132
24: Frame Center Longitude              4 bytes 29.15789012292302
25: Frame Center Elevation              2 bytes 3216.0372320134275
48: Security Local Metadata Set        28 bytes b'\x01\x01\x01\x02\x01\x07\x03\x05//USA\x0c\x01\x07\r\x06\x00U\x00S\x00A\x16\x02\x00\n'
    01: Unsupported Tag                     1 bytes b'\x01'
    02: Unsupported Tag                     1 bytes b'\x07'
    03: Unsupported Tag                     5 bytes b'//USA'
    12: Unsupported Tag                     1 bytes b'\x07'
    13: Unsupported Tag                     6 bytes b'\x00U\x00S\x00A'
    22: Unsupported Tag                     2 bytes b'\x00\n'
65: UAS LS Version Number               1 bytes b'\x06'
94: Unsupported Tag                    34 bytes b'\x01p\xf5\x92\xf0#s6J\xf8\xaa\x91b\xc0\x0f.\xb2\xda\x16\xb7CA\x00\x08A\xa0\xbe6[Z\xb9j6E'
01: Checksum                            2 bytes b'\xaaC'
```
