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

Example-01: Basic GroundTrack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Python Code``
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

    simulateProgress(system, time, 8, orbitPropOnly=True)

    groundTrack(recorder['DIWATA'])

``Terminal Output``
.. code:: sh

    Run Simulation (from 0.0 to 14400, step=4)
    Simulating: 100%|█████████████████████████| 14400.0/14400.0 [00:00<00:00, 22944.82it/s]

    Elapsed Time:   0.6345400810241699 sec.

    Run Animation (from 0.0 to 14396.0, step=16.0)
    Animating Ground Track:  18%|████▍                    | 161/900 [00:22<01:42,  7.24it/s]

|Groundtrack Image|

This two-dimensional groundtrack shows the predicted track satellite track over a rotating Earth.

|Groundtrack|

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
.. |Groundtrack| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Groundtrack.gif
.. |Attitudetrack| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Attitudetrack.gif
.. |Sensortrack| image:: https://github.com/space-hiro/LEOSS/blob/main/examples/Sensortrack.gif