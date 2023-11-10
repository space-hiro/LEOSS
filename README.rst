LEOSS
=====

``LEOSS`` is shorthand for Low Earth Orbit Spacecraft Simulator. 

This project README is still in construction...

Installation
============

.. code:: sh

    pip install leoss

Usage
=====

.. code:: python

    from leoss import *

Groundtracks
---------------------

``Groundtracks``, by definition, are the locus of points formed by the points on the Earth directly below a satellite
as it travels through its orbit. The practical use case of this feature is for determining satellite orbit position and
location relative to a specific point on the Earth or a ground site in particular. 

****

Example-01: Basic GroundTrack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code:

.. code:: python

    system = LEOSS()
    system.epoch(2023,1,1,12,0,0)

    system.addSpacecraft("DIWATA")

    spacecraft = system.getSpacecrafts()
    recorder   = system.getRecorders()

    spacecraft["DIWATA"].setmass(4.00)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.3405))
    spacecraft["DIWATA"].setposition(Vector(-3398.36655479e3, 2536.91064491e3,  5312.67851581e3))
    spacecraft["DIWATA"].setvelocity(Vector(-5.05043202e3, -5.73213209e3, -0.49795572e3))

    time = 60*60*4

    simulateProgress(system, time, 4, orbitPropOnly=True)

    groundTrack(recorder['DIWATA'])


Terminal Output:

.. code:: sh

    Run Simulation (from 0.0 to 14400, step=4)
    Simulating: 100%|█████████████████████████| 14400.0/14400.0 [00:00<00:00, 22944.82it/s]

    Elapsed Time:   0.6345400810241699 sec.

|Groundtrack Image|

The figure above shows the output plot from the line  ``groundTrack(recorder['DIWATA'])``. The horizontal 
axis is the longitude ranging from 180°W to 180°E (or -180° to 180°). The vertical axis is the geodetic
latitude ranging from 90°S to 90°N (or -90° to 90°). This two-dimensional groundtrack shows the predicted
track satellite track over a rotating Earth. The sub-satellite point (the point on Earth where the satellite
is directly above), is presented as a white circle, likewise the sun is the yellow circle. The instantaneous
position (latitude, longitude and altitude) is annotated with the satellite. The name of the satellite is
shown as the title: ``DIWATA``, the instantaneous datetime is also shown after the satellite name.

****

Example-02: Animated GroundTrack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code:

.. code:: python

    system = LEOSS()
    system.epoch(2023,1,1,12,0,0)

    system.addSpacecraft("DIWATA")

    spacecraft = system.getSpacecrafts()
    recorder   = system.getRecorders()

    spacecraft["DIWATA"].setmass(4.00)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.3405))
    spacecraft["DIWATA"].setposition(Vector(-3398.36655479e3, 2536.91064491e3,  5312.67851581e3))
    spacecraft["DIWATA"].setvelocity(Vector(-5.05043202e3, -5.73213209e3, -0.49795572e3))

    time = 60*60*4

    simulateProgress(system, time, 4, orbitPropOnly=True)

    animatedGroundTrack(recorder["DIWATA"], sample=4, saveas = 'gif')


Terminal Output:

.. code:: sh

    Run Simulation (from 0.0 to 14400, step=4)
    Simulating: 100%|█████████████████████████| 14400.0/14400.0 [00:00<00:00, 22535.73it/s]

    Elapsed Time:   0.64249587059021 sec.

    Run Animation (from 0.0 to 14396.0, step=16.0)
    Animating Ground Track:  10%|██▍                      | 88/900 [00:12<01:56,  6.98it/s]

|Groundtrack GIF|

The figure above shows the output GIF from the line ``animatedGroundTrack(recorder['DIWATA']), sample=4, saveas='gif')``. 
This is the animated version of the previous example, sampled at every ``4th`` frames.

****

Example-03: Counting Passes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Code:

.. code:: python

    system = LEOSS()
    system.epoch(2023,1,1,12,0,0)

    system.addSpacecraft("DIWATA")

    spacecraft = system.getSpacecrafts()
    recorder   = system.getRecorders()

    spacecraft["DIWATA"].setmass(4.00)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.3405))
    spacecraft["DIWATA"].setposition(Vector(-3398.36655479e3, 2536.91064491e3,  5312.67851581e3))
    spacecraft["DIWATA"].setvelocity(Vector(-5.05043202e3, -5.73213209e3, -0.49795572e3))

    time = 60*60*24*3

    simulateProgress(system, time, 4, orbitPropOnly=True)

    groundTrack(recorder['DIWATA'])

    test_station = GroundStation('TEST_GRS', 12, 122, 5)
    passTrack(recorder['DIWATA'], test_station)

Terminal Output:

.. code:: sh

    Run Simulation (from 0.0 to 259200, step=4)
    Simulating: 100%|█████████████████████████| 259200.0/259200.0 [00:11<00:00, 22198.93it/s]

    Elapsed Time:   11.676238536834717 sec.
    #1:     Pass(AOS:2023-01-01 13:08:00, TCA:2023-01-01 13:13:20, MaxElev:37.25320526774923, LOS:2023-01-01 13:18:40, Duration:640.0)
    #2:     Pass(AOS:2023-01-01 23:02:12, TCA:2023-01-01 23:07:28, MaxElev:37.66819774201771, LOS:2023-01-01 23:12:48, Duration:636.0)
    #3:     Pass(AOS:2023-01-02 00:40:08, TCA:2023-01-02 00:43:56, MaxElev:7.022392466935841, LOS:2023-01-02 00:47:48, Duration:460.0)
    #4:     Pass(AOS:2023-01-02 12:19:52, TCA:2023-01-02 12:25:12, MaxElev:40.89032470174465, LOS:2023-01-02 12:30:32, Duration:640.0)
    #5:     Pass(AOS:2023-01-02 13:57:56, TCA:2023-01-02 14:01:56, MaxElev:7.704157631282513, LOS:2023-01-02 14:06:00, Duration:484.0)
    #6:     Pass(AOS:2023-01-02 22:14:56, TCA:2023-01-02 22:19:12, MaxElev:10.038695486057108, LOS:2023-01-02 22:23:32, Duration:516.0)
    #7:     Pass(AOS:2023-01-02 23:50:44, TCA:2023-01-02 23:55:52, MaxElev:29.833762372275316, LOS:2023-01-03 00:01:08, Duration:624.0)
    #8:     Pass(AOS:2023-01-03 11:32:52, TCA:2023-01-03 11:37:08, MaxElev:9.948364280656776, LOS:2023-01-03 11:41:28, Duration:516.0)
    #9:     Pass(AOS:2023-01-03 13:08:28, TCA:2023-01-03 13:13:36, MaxElev:28.566104657418002, LOS:2023-01-03 13:18:52, Duration:624.0)
    #10:    Pass(AOS:2023-01-03 21:29:52, TCA:2023-01-03 21:30:44, MaxElev:0.23096525156636005, LOS:2023-01-03 21:31:36, Duration:104.0)
    #11:    Pass(AOS:2023-01-03 23:02:28, TCA:2023-01-03 23:07:48, MaxElev:50.79955505964675, LOS:2023-01-03 23:13:12, Duration:644.0)
    #12:    Pass(AOS:2023-01-04 00:40:56, TCA:2023-01-04 00:44:16, MaxElev:4.822331693934615, LOS:2023-01-04 00:47:40, Duration:404.0)
    Number of Passes: 12, Ground Radius: 2241175.1615987364 m.

|Groundtrack|
|Passtrack Image1|  
|Passtrack Image2| |Passtrack Image3| |Passtrack Image4|

The figure above shows the output GIF from the line ``animatedGroundTrack(recorder['DIWATA']), sample=4, saveas='gif')``. 
This is the animated version of the previous example, sampled at every ``4th`` frames.

****

Animated Attitude Tracking
--------------------------

|Attitudetrack|

Animated Sensor Tracking
------------------------

|Sensortrack|

Support
=======

Roadmap
=======

Contributing
============

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropiate.

Authors and Acknowledgement
===========================

Main Author: ``kennethjohnibarra@gmail.com``

License
=======

`MIT <https://choosealicense.com/licenses/mit/>`__

.. |Groundtrack Image| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Figure_1.png
.. |Groundtrack GIF| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Groundtrack.gif
.. |Groundtrack| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Figure_6.png
.. |Passtrack Image1| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Figure_2.png
.. |Passtrack Image2| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Figure_3.png
    :width: 32%
.. |Passtrack Image3| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Figure_4.png
    :width: 32%
.. |Passtrack Image4| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Figure_5.png
    :width: 32%
.. |Attitudetrack| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Attitudetrack.gif
.. |Sensortrack| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Sensortrack.gif