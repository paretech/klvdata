What?
-----
KLV Data is a Python library for parsing Key Length Value (KLV_) formatted binary streams. Common uses of the library would be parsing and displaying `MISB ST`_ 0601 UAS metadata from `STANAG 4609`_ compliant `MPEG-2 Transport Streams (TS) (MPEG-TS)`_. Note that this library alone cannot de-mux an MPEG-TS, a dependency like FFmpeg_ or GStreamer_ is still requried.

.. _KLV: https://en.wikipedia.org/wiki/KLV
.. _STANAG 4609: http://www.gwg.nga.mil/misb/docs/nato_docs/STANAG_4609_Ed3.pdf
.. _MPEG-2 Transport Streams (TS) (MPEG-TS): https://en.wikipedia.org/wiki/MPEG_transport_stream
.. _MISB ST: http://www.gwg.nga.mil/misb/st_pubs.html
.. _FFMpeg: https://www.ffmpeg.org/
.. _GStreamer: https://gstreamer.freedesktop.org/


Why?
----
Not many opensource options available.

Features
--------
- Parses KLV metadata streams.
- Supports `MISB ST`_ 0601 UAV Datalink Local Set.
- Supports `MISB ST`_ 0102 Security Metadata field definitions.
- Built for Python 3.5, 3.6.
- Requires no external Python dependencies.

.. _MISB ST: http://www.gwg.nga.mil/misb/st_pubs.html

Contributing
------------
Contributions are welcome!