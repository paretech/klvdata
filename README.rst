.. image:: https://travis-ci.org/paretech/klv_data.svg?branch=master
    :target: https://travis-ci.org/paretech/klv_data

.. image:: https://coveralls.io/repos/github/paretech/klv_data/badge.svg?branch=master
    :target: https://coveralls.io/github/paretech/klv_data?branch=master

What?
-----
KLV_Data is a Python library for parsing and constructing Key Length Value (KLV_) formatted binary streams. Common uses of the library would be parsing and displaying `MISB ST`_ 0601 Unmanned Air System (UAS) metadata from `STANAG 4609`_ compliant `MPEG-2 Transport Streams (TS) (MPEG-TS)`_. Note that KLV_Data alone cannot de-mux KLV data from an MPEG-2 TS, but programs like FFmpeg_ and GStreamer_ can be used with KLV_Data in the workflow to perform the function.

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
- Supports `MISB ST`_ 0601 UAS Datalink Local Set.
- Supports `MISB ST`_ 0102 Security Metadata Local Set.
- Built for Python 3.5, 3.6.
- Requires no external Python dependencies.

.. _MISB ST: http://www.gwg.nga.mil/misb/st_pubs.html

Contributing
------------
Contributions are welcome!