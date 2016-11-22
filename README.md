# STANAG 4609 KLV Metadata Analyzer and Composer
## Summary
[North Atlantic Treaty Organization (NATO) Standardization Agreement (STANAG) 4609 Ed. 3](http://www.gwg.nga.mil/misb/docs/nato_docs/STANAG_4609_Ed3.pdf) specifies standards for exchanging and producing Motion Imagery (MI). In short, STANAG 4609 defines MI as a sequential stream of images ("video") and __metadata__ at a rate fast enough to characterize a phenomenon within a common Field of Regard (FOR). It is the intent that the following documentation and Python software will be beneficial in decoding, interpretation and authoring of the metadata used in the exploitation of MI.

Video, audio and metadata streams are combined into an MPEG Transport Stream (MPEG-TS, MTS or TS) (ISO/IEC 13818-1). Where videos are typically compressed using MPEG-2 (ISO/IEC 13818-2) or H.264 (ISO/IEC 14496-10) and metadata as byte streams in accordance with a [Society of Motion Picture and Television Engineers (SMPTE)](https://www.smpte.org/)) 336M and a variety of [Motion Imagery Standards Board (MISB)](http://www.gwg.nga.mil/misb/) recommended practices and standards.

The MISB standards and recommended practices are freely and openly available at <http://www.gwg.nga.mil/misb/index.html>. These documents are generally easy to understand and detail all the information that is necessary to implement a Key Length Value (KLV) metadata analyzer and composer based on MISB [RP 0701](http://www.gwg.nga.mil/misb/docs/rp/RP0701.pdf) "Common Metadata System Structure" and supporting the MISB [ST 0601.9](http://www.gwg.nga.mil/misb/docs/standards/ST0601.9.pdf) "Unamanned Air System (UAS) Datalink Local Set" including MISB [ST 0102.11](http://www.gwg.nga.mil/misb/docs/standards/ST0102.11.pdf) "Security Metadata Local Set" for MI as specified by STANAG 4609.

_**NOTE**: Since the publication of NATO STANAG 4609 Ed. 3, some of the standards referenced as MISB recommeded practices (RP) have been superceeded by MISB standards (ST). For example, MISB RP 0102.4 has been superseded by MISB ST 0102.11. In some cases the title and other language has also changed._

_**NOTE**: The MISB standards do a seemingly good job of being self contained and not necessarily requiring the aquisition of external standards like SMPTE 336M. Considering the ease of access to MISB documents, this project's documentation will cite MISB documentation over origin documentation when available._

## Licensing
This project is released under the MIT license.

## References

## Examples
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

## Software Requirements

### Python Support
- Python 3.2.5 and later

_**NOTE:** [Portable Python 3.2.5.1](http://portablepython.com/wiki/PortablePython3.2.5.1/) is easily available for Windows systems for which there are no administrative rights._

### Platform Support
- Contemporary versions of Linux, Windows and Mac OS X.

### User Interface
- Command Line Interface (CLI)

### Input
- Standard Input
- Local File
- UDP Socket (multicast and unicast)
- TCP Socket

### Output
- Standard Output
- Local File
- Standard Output AND Local File

### Source Parsing

### Composition and Authoring

### Extensibility

