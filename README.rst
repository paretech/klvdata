What?
-----
KLV-Data is a Python library that can parse Key Length Value (KLV) formatted binary streams. Common uses of the library would be parsing and displaying MISB 0601 UAS metadata from STANAG 4609 compliant MPEG-2 Transport Streams (TS) (MPEG-TS). Note that this library cannot parse MPEG-TS directly a dependencies like FFmpeg_ or GStreamer_ are still requried.

.. _FFMpeg: https://www.ffmpeg.org/
.. _GStreamer: https://gstreamer.freedesktop.org/


Why?
----
Not many opensource options available.

Features
--------
- Parses KLV metadata streams
- Supports MISB ST 0601 UAV field definitions.
- Supports MISB ST 0102 Security Metadata field definitions.
- Built for Python 3.6

Quick Start
-----------

Contributing
------------
Contributions are welcome!