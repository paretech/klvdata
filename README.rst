.. image:: https://travis-ci.org/paretech/klvdata.svg?branch=master
    :target: https://travis-ci.org/paretech/klvdata

.. image:: https://coveralls.io/repos/github/paretech/klvdata/badge.svg?branch=master
    :target: https://coveralls.io/github/paretech/klvdata?branch=master

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

.. _MISB ST: http://www.gwg.nga.mil/misb/st_pubs.htmlrm

Quick Start
-----------
First:

.. code-block:: console

    $ pip install klvdata
    $ wget https://raw.githubusercontent.com/paretech/klvdata/master/data/DynamicConstantMISMMSPacketData.bin

	$ cat << EOF > klvdata_test.py
	#!/usr/bin/env python
	import sys, klvdata;
	for packet in klvdata.StreamParser(sys.stdin.buffer.read()): packet.structure()
	EOF

And then:

.. code-block:: console

	$ ./klvdata_test.py < DynamicConstantMISMMSPacketData.bin

	<class 'klvdata.misb0601.UASLocalMetadataSet'>
	    <class 'klvdata.misb0601.PrecisionTimeStamp'>
	    <class 'klvdata.misb0601.MissionID'>
	    <class 'klvdata.misb0601.PlatformHeadingAngle'>
	    <class 'klvdata.misb0601.PlatformPitchAngle'>
	    <class 'klvdata.misb0601.PlatformRollAngle'>
	    <class 'klvdata.misb0601.PlatformDesignation'>
	    <class 'klvdata.misb0601.ImageSourceSensor'>
	    <class 'klvdata.misb0601.ImageCoordinateSystem'>
	    <class 'klvdata.misb0601.SensorLatitude'>
	    <class 'klvdata.misb0601.SensorLongitude'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0102.SecurityLocalMetadataSet'>
	            <class 'klvdata.misb0102.SecurityClassification'>
	            <class 'klvdata.misb0102.UnknownElement'>
	            <class 'klvdata.misb0102.UnknownElement'>
	            <class 'klvdata.misb0102.UnknownElement'>
	            <class 'klvdata.misb0102.UnknownElement'>
	            <class 'klvdata.misb0102.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.UnknownElement'>
	    <class 'klvdata.misb0601.Checksum'>

If you have FFmpeg installed, want to try it on real video, and have some bandwidth to spare (~97 MB):

.. code-block:: console

    $ wget http://samples.ffmpeg.org/MPEG2/mpegts-klv/Day%20Flight.mpg
    $ ffmpeg -i data/Day\ Flight.mpg -map data-re -codec copy -f data - | ./klvdata_test.py

    <class 'klvdata.misb0601.UASLocalMetadataSet'>
        <class 'klvdata.misb0601.PrecisionTimeStamp'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.PlatformHeadingAngle'>
        <class 'klvdata.misb0601.PlatformPitchAngle'>
        <class 'klvdata.misb0601.PlatformRollAngle'>
        <class 'klvdata.misb0601.ImageSourceSensor'>
        <class 'klvdata.misb0601.ImageCoordinateSystem'>
        <class 'klvdata.misb0601.SensorLatitude'>
        <class 'klvdata.misb0601.SensorLongitude'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.UnknownElement'>
        <class 'klvdata.misb0601.Checksum'>

       [...]
	
Contributing
------------
Contributions are welcome!