from leoss import __version__
from leoss import *


def test_version():
    assert __version__ == "0.1.18"

def test_01():
    system = LEOSS()
    system.addSpacecraft("DIWATA-1")
    system.addSpacecraft("DIWATA-2")

    assert system.listSpacecraft() == ['DIWATA-1', 'DIWATA-2']
    assert system.numSpacecraft() == 2

def test_02():
    a = Vector(1,1,1)
    b = Vector(2,2,2)
    c = 3
    d = Vector(1,2,3)

    assert a + b == Vector(3,3,3)
    assert a - b == Vector(-1,-1,-1)
    assert a * b == Vector(2,2,2)
    assert a * c == Vector(3,3,3)
    assert c * a == Vector(3,3,3)
    assert a / c == Vector(1/3,1/3,1/3)
    assert a.cross(b) == Vector(0,0,0)
    assert a.cross(d) == Vector(1,-2,1)
    assert b.cross(a) == Vector(0,0,0)
    assert d.cross(a) == Vector(-1,2,-1)
    assert b.normalize() == a.normalize()
    assert d.normalize() == Vector(1/(14**0.5),2/(14**0.5),3/(14**0.5))
    assert d[0] == 1
    assert d[1] == 2
    assert d[2] == 3
    assert str(a) == "Vector(1, 1, 1)"
    assert str(d) == "Vector(1, 2, 3)"

def test_03():
    system = LEOSS()

    system.addSpacecraft("DIWATA-1")
    system.addSpacecraft("DIWATA-2")
    
    assert system[0].name == "DIWATA-1"
    assert system[1].name == "DIWATA-2"

    assert system[0].getmass() == 0
    system[0].setmass(10)
    assert system[0].getmass() == 10
    system[1].setmass(99)
    assert system[1].getmass() == 99

    system[0].setposition(Vector(50,30,40))
    assert system[0].getposition() == Vector(50,30,40)
    assert system[1].getposition() == Vector(0,0,0)
    system[1].setvelocity(Vector(50,30,40)*5)
    assert system[1].getvelocity() == Vector(250,150,200)
    system[1].setvelocity(2*Vector(50,30,40))
    assert system[1].getvelocity() == Vector(100, 60, 80)

def test_04():

    system = LEOSS()

    system.addSpacecraft("DIWATA")

    system[0].setmass(4.5)
    system[0].setposition(Vector(100,60,80))
    system[0].setvelocity(Vector(5,3,4))

    assert system[0].state + system[0].state == 2 * system[0].state
    assert system[0].state - system[0].state == system[0].state * 0
    assert system[0].state / 2 == system[0].state * 0.5
    assert str(system[0].state) == "State(4.5, Vector(100, 60, 80), Vector(5, 3, 4))" 

def test_05():

    system = LEOSS()
    system.mu = 0

    system.addSpacecraft("DIWATA-1")
    system.addSpacecraft("DIWATA-2")

    system[0].setmass(4.5)
    system[0].setposition(Vector(100,60,80))
    system[0].setvelocity(Vector(5,3,4))

    system[1].setmass(3.5)
    system[1].setposition(Vector(60,100,50))
    system[1].setvelocity(Vector(5,4,3))

    system.advance1timestep(1.0)

    assert system[0].getmass() == 4.5
    assert system[0].getposition() == Vector(105,63,84)
    assert system[0].getvelocity() == Vector(5,3,4)
    assert system.time == 1.0

    system.advance1timestep(1.0)

    assert system[0].getmass() == 4.5
    assert system[0].getposition() == Vector(110,66,88)
    assert system[0].getvelocity() == Vector(5,3,4)
    assert system.time == 2.0

    assert system[1].getmass() == 3.5
    assert system[1].getposition() == Vector(70,108,56)
    assert system[1].getvelocity() == Vector(5,4,3)

    system.advance1timestep(0.50)

    assert system[0].getmass() == 4.5
    assert system[0].getposition() == Vector(112.5,67.5,90)
    assert system[0].getvelocity() == Vector(5,3,4)
    assert system.time == 2.50

    assert system[1].getmass() == 3.5
    assert system[1].getposition() == Vector(72.5,110,57.5)
    assert system[1].getvelocity() == Vector(5,4,3)

def test_06():

    system = LEOSS()
    
    system.addSpacecraft("DIWATA")

    assert system[0].state[0] == system[0].state.mass
    assert system[0].state[1] == system[0].state.position
    assert system[0].state[2] == system[0].state.velocity

    system[0].state[0] = 10
    assert system[0].state.mass == 10

    system[0].setmass(20)
    assert system[0].state[0] == 20

    system[0].state[1] = Vector(1.0,2.0,3.0)
    assert system[0].state.position == Vector(1,2,3)

def test_07():

    system = LEOSS()

    system.addSpacecraft("DIWATA-1")
    system[0].setmass(4.00)
    system[0].setposition(Vector(-3398.36655479e3, 2536.91064491e3,  5312.67851581e3 ))
    system[0].setvelocity(Vector(-5.05043202e3, -5.73213209e3, -0.49795572e3))

    pos0 = system[0].state.position
    vel0 = system[0].state.velocity
    h0   = pos0.cross(vel0).magnitude()
    xi0  = (vel0.magnitude()**2)/2 - ( system.mu/pos0.magnitude() )

    simulate(system, timeEnd=1000, timeStep=1/8)

    pos1 = system[0].state.position
    vel1 = system[0].state.velocity
    h1   = pos1.cross(vel1).magnitude()
    xi1  = (vel1.magnitude()**2)/2 - ( system.mu/pos1.magnitude() )
    
    assert abs(h1-h0) < 1e-3
    assert abs(xi1-xi0) < 1e-3

def test_08():

    assert type(visual_check()) == LEOSS

def test_09():

    system = LEOSS()

    assert system.datetime0 == datetime.datetime.today()
    
    system.epoch(2023,1,1)

    assert system.datetime0 == datetime.datetime(2023,1,1,0,0,0,0)

def test_10():

    system = LEOSS()

    system.addSpacecraft("DIWATA-1")

    assert system.datenow() == datetime.datetime.today()

    system[0].setmass(4.00)
    system[0].setposition(Vector(-3398.36655479e3, 2536.91064491e3,  5312.67851581e3 ))
    system[0].setvelocity(Vector(-5.05043202e3, -5.73213209e3, -0.49795572e3))

    system.epoch(2023,1,1)
    simulate(system, timeEnd=1000, timeStep=1/8)

    assert system.datenow() == datetime.datetime(2023,1,1,0,16,40,0)

def test_11():

    system = LEOSS()

    system.epoch(2004,3,3,4,30,0)

    assert system.jdate0 == 2453067.5
    assert system.gmst0  == 161.10873367774252
    assert system.gmst   == 228.79354253524252

    system.epoch(1992,8,20,12,14,0)

    assert system.jdate0 == 2448854.5
    assert system.gmst0  == 328.5763825139975
    assert system.gmst%360 == 152.57878881549743

def test_12():

    system = LEOSS()

    system.addSpacecraft("DIWATA")

    spacecraft = system.getSpacecrafts()

    spacecraft["DIWATA"].setmass(50)
    spacecraft["DIWATA"].setposition(1e3*Vector(4395.079058029986, 3631.5889348004957, -3712.575674067216))
    spacecraft["DIWATA"].setvelocity(1e3*Vector(-5.76886641743168, 2.5823185921356733, -4.310210403510053))

    system.epoch(2023,9,26,3,11,18)

    location = system.locate(spacecraft["DIWATA"])

    assert abs(location[0]- -33.2464) <= 1
    assert abs(location[1]- -12.9220) <= 1
    assert abs(location[2]- 431.8) <= 1 

    time = 41*60 + 59

    simulate(system, time)
    location = system.locate(spacecraft["DIWATA"])

    assert str(system.datenow()) == '2023-09-26 03:53:17'
    assert abs(location[0]- 20.7225) <= 1
    assert abs(location[1]- 142.6722) <= 1
    assert abs(location[2]- 414.6) <= 1 