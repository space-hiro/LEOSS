from leoss import __version__
from leoss import *


def test_version():
    assert __version__ == "0.1.8"

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

    system.addSpacecraft("DIWATA")

    system[0].setmass(4.5)
    system[0].setposition(Vector(100,60,80))
    system[0].setvelocity(Vector(5,3,4))

    system.advance1timestep(1.0)

    assert system[0].getmass() == 4.5
    assert system[0].getposition() == Vector(105,63,84)
    assert system[0].getvelocity() == Vector(5,3,4)

    system.advance1timestep(1.0)

    assert system[0].getmass() == 4.5
    assert system[0].getposition() == Vector(110,66,88)
    assert system[0].getvelocity() == Vector(5,3,4)

