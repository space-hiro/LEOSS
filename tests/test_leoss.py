from leoss import __version__
from leoss import *


def test_version():
    assert __version__ == "0.2.20"

def test_01():
    '''
    Test LEOSS Class Implementation.
    LEOSS object creation
    addSpacecraft method -- add new "DIWATA-1" and "DIWATA-2" Spacecraft Class object to system (LEOSS Class)
    listSpacecraft method -- list the names of Spacecraft Class objects in system
    numSpacecraft method -- count number of Spacecraft Class objects in system
    '''
    system = LEOSS()
    system.addSpacecraft("DIWATA-1")
    system.addSpacecraft("DIWATA-2")

    assert system.listSpacecraft() == ['DIWATA-1', 'DIWATA-2']
    assert system.numSpacecraft() == 2

def test_02():
    '''
    Test Vector Class Implementation.
    Vector Addition
    Vector Subtraction
    Vector Element Wise Multiplication
    Vector Scalar Multiplication
    Vector Cross Product
    Vector Normalization
    __getitem__ method
    __str__ method
    __repr__ method
    '''
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
    '''
    __getitem__ method for LEOSS class
    setmass method for Spacecraft class
    getmass method fpr Spacecraft class
    setposition method for Spacecraft class
    getposition method for Spacecraft class
    setvelocity method for Spacecraft class
    getvelocity method for Spacecraft class
    '''
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
    '''
    Test State Class Implementation.
    State Addition __add__ (element wise)
    State Subtraction __sub__ (element wise)
    State Multiplication __mul__ (element wise)
    State Reverse Multiplication __rmul__ (element wise)
    State Floor Division __truediv__ (element wise)
    '''
    system = LEOSS()

    system.addSpacecraft("DIWATA")

    system[0].setmass(4.5)
    system[0].setposition(Vector(100,60,80))
    system[0].setvelocity(Vector(5,3,4))

    assert system[0].state + system[0].state == 2 * system[0].state
    assert system[0].state - system[0].state == system[0].state * 0
    assert system[0].state / 2 == system[0].state * 0.5
    # assert str(system[0].state) == "State(4.5, Vector(100, 60, 80), Vector(5, 3, 4))" 

def test_05():
    '''
    Test LEOSS class methods.
    advance1timestep method -- move forward the system with one time step
    verify that the position updates with the velocity as derivatives
    '''
    system = LEOSS()
    system.mu = 0

    system.addSpacecraft("DIWATA-1")
    system.addSpacecraft("DIWATA-2")

    system[0].setmass(4.5)
    system[0].setsize(Vector(0.1,0.1,0.1))
    system[0].setposition(Vector(100,60,80))
    system[0].setvelocity(Vector(5,3,4))

    system[1].setmass(3.5)
    system[1].setsize(Vector(0.1,0.1,0.1))
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
    '''
    Test State methods.
    __getitem__ method
    '''

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
    '''
    Test LEOSS methods.
    simulate method -- move forward multiple time steps given the timeEnd and timeStep in seconds
    verify that the specific mechanical energy and orbit specific angular momentum is conserved <= 1e-3 
    '''
    system = LEOSS()

    system.addSpacecraft("DIWATA-1")
    system[0].setmass(4.00)
    system[0].setsize(Vector(0.1,0.1,0.1))
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
    '''
    verify that a function is a class like LEOSS.
    '''
    assert type(visual_check()) == LEOSS

def test_09():
    '''
    Test LEOSS method and variables.
    epoch method -- specify the date and time epoch or instant in time as initial value of the system
    '''

    system = LEOSS()

    assert system.datetime0 == datetime.datetime.today()
    
    system.epoch(2023,1,1)

    assert system.datetime0 == datetime.datetime(2023,1,1,0,0,0,0)

def test_10():
    '''
    Test LEOSS methods.
    verify that simulate runs the correct amount of time by using epoch to check the date time after simulation
    '''

    system = LEOSS()

    system.addSpacecraft("DIWATA-1")

    assert system.datenow() == datetime.datetime.today()

    system[0].setmass(4.00)
    system[0].setsize(Vector(0.1,0.1,0.1))
    system[0].setposition(Vector(-3398.36655479e3, 2536.91064491e3,  5312.67851581e3 ))
    system[0].setvelocity(Vector(-5.05043202e3, -5.73213209e3, -0.49795572e3))

    system.epoch(2023,1,1)
    simulate(system, timeEnd=1000, timeStep=1/8)

    assert system.datenow() == datetime.datetime(2023,1,1,0,16,40,0)

def test_11():
    '''
    Test LEOSS methods.
    verify that epoch calcualtes the correct Julian Date, Greenwich Mean Sidereal Time at UT and Greenwich Mean Sidereal Time
    '''

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
    '''
    Test LEOSS simulation.
    Using data from ISS orbit and with the python sgp4 library.
    Verify that the simulation acquires minimal error compared with the later orbit propagation.
    Test the locate method of LEOSS -- gives the latitude, longitude and altitude or a Spacecraft object
    '''
    system = LEOSS()

    system.addSpacecraft("DIWATA")

    spacecraft = system.getSpacecrafts()

    # ISS data from https://live.ariss.org/tle/
    # 26/09/2023 03:11:18 UTC
    # -33.2464deg, -12.9220deg
    # 431.8 km

    # r v state vectors given here are calculated from sgp4 (analytical) python library
    spacecraft["DIWATA"].setmass(50)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.1))
    spacecraft["DIWATA"].setposition(1e3*Vector(4395.079058029986, 3631.5889348004957, -3712.575674067216))
    spacecraft["DIWATA"].setvelocity(1e3*Vector(-5.76886641743168, 2.5823185921356733, -4.310210403510053))

    system.epoch(2023,9,26,3,11,18)

    location = system.locate(spacecraft["DIWATA"], system.time)

    assert str(system.datenow()) == '2023-09-26 03:11:18'
    assert abs(location[0]- -33.2464) <= 1
    assert abs(location[1]- -12.9220) <= 1
    assert abs(location[2]- 431.8) <= 1 

    time = 41*60 + 59

    simulate(system, time)
    location = system.locate(spacecraft["DIWATA"], system.time)

    # ISS data from https://live.ariss.org/tle/
    # 26/09/2023 03:53:17 UTC
    # 20.7225deg, 142.6722deg
    # 414.6km

    assert str(system.datenow()) == '2023-09-26 03:53:17'
    assert abs(location[0]- 20.7225) <= 1
    assert abs(location[1]- 142.6722) <= 1
    assert abs(location[2]- 414.6) <= 1 

def test_13():
    '''
    Test Recorder Class Implementation.
    Recorder class - used as a recorder or observer for a Spacecraft class object
    verify that the recorder class records every state of the spacecraft during simulation.
    '''

    system = LEOSS()
    system.epoch(2023,9,26,3,11,18,0)

    system.addSpacecraft("DIWATA")

    spacecraft = system.getSpacecrafts()
    recorder   = system.getRecorders()

    spacecraft["DIWATA"].setmass(50)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.1))
    spacecraft["DIWATA"].setposition(1e3*Vector(4395.079058029986, 3631.5889348004957, -3712.575674067216))
    spacecraft["DIWATA"].setvelocity(1e3*Vector(-5.76886641743168, 2.5823185921356733, -4.310210403510053))

    time = 41*60 + 59

    simulate(system, time)

    datetime0  = recorder["DIWATA"]["Datetime"][1]
    statedata0 = recorder["DIWATA"]["State"][1]
    datetimef  = recorder["DIWATA"]["Datetime"][-1]
    statedataf = recorder["DIWATA"]["State"][-1]
    
    assert str(datetime0) == '2023-09-26 03:11:18.031250'
    assert statedata0.position == Vector(4394898.778238248, 3631669.6300121024, -3712710.365847866)
    assert statedata0.velocity ==  Vector(-5769.040252603422, 2582.1749501580102, -4310.063557192801)
    assert str(datetimef) == '2023-09-26 03:53:16.968750'
    assert statedataf.position == Vector(-5725429.518467132, -2767128.121674426, 2382521.4362371108)
    assert statedataf.velocity == Vector(4028.4864460075523, -3694.449056195037, 5373.066456593324)

def test_14():
    '''
    Test Recorder class methods.
    addSpacecraft method now can be used to set what the recorder class will record.
    verify that the recorder records the selected parameters during simulation.
    '''

    system = LEOSS()
    system.epoch(2023,9,26,3,11,18,0)

    system.addSpacecraft("DIWATA", ["State", "Location", "Netforce"])

    spacecraft = system.getSpacecrafts()
    recorder   = system.getRecorders()

    spacecraft["DIWATA"].setmass(50)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.1))
    spacecraft["DIWATA"].setposition(1e3*Vector(4395.079058029986, 3631.5889348004957, -3712.575674067216))
    spacecraft["DIWATA"].setvelocity(1e3*Vector(-5.76886641743168, 2.5823185921356733, -4.310210403510053))

    time = 41*60 + 59

    simulate(system, time)

    datetime0  = recorder["DIWATA"]["Datetime"][1]
    statedata0 = recorder["DIWATA"]["State"][1]
    location0  = recorder["DIWATA"]["Location"][1]
    netforce0  = recorder["DIWATA"]["Netforce"][1]
    datetimef  = recorder["DIWATA"]["Datetime"][-1]
    statedataf = recorder["DIWATA"]["State"][-1]
    locationf = recorder["DIWATA"]["Location"][-1]
    netforcef  = recorder["DIWATA"]["Netforce"][-1]
    
    assert str(datetime0) == '2023-09-26 03:11:18.031250'
    assert statedata0.position == Vector(4394898.778238248, 3631669.6300121024, -3712710.365847866)
    assert statedata0.velocity == Vector(-5769.040252603422, 2582.1749501580102, -4310.063557192801)
    assert location0 == Vector(-33.23762159989866, -12.932703716557796, 431.80805538907555)
    assert netforce0 == Vector(-278.11913958517897, -229.83480648340282, 234.9668751720585)
    assert str(datetimef) == '2023-09-26 03:53:16.968750'
    assert statedataf.position == Vector(-5725429.518467132, -2767128.121674426, 2382521.4362371108)
    assert statedataf.velocity == Vector(4028.4864460075523, -3694.449056195037, 5373.066456593324)
    assert locationf == Vector(20.658246279489802, 142.76949414474478, 415.2313183538606)
    assert netforcef == Vector(364.382790906085, 176.1192072581338, -151.64453269308962) 

def test_15():
    '''
    Test Quaternion Class Implementation.
    Quaternion Addition 
    __str__ method
    __repr__ method
    Quaternion get methods (w, x, y, z)
    Quaternion Scalar Multiplcation
    '''

    q1 = Quaternion()
    q2 = Quaternion()

    assert q1 + q2 == Quaternion()
    assert str(q1) == 'Quaternion(1.0, 0.0, 0.0, 0.0)'

    q3 = Quaternion(1,1,1,1)
    
    assert q3 == Quaternion(0.5, 0.5, 0.5, 0.5)
    assert q1 + q3 == q3
    assert q3 + q3 == Quaternion(-0.5, 0.5, 0.5, 0.5)

    q4 = Quaternion(1,0,3,2)

    assert q4 == Quaternion(0.2672612419124244, 0.0, 0.8017837257372732, 0.5345224838248488)
    assert q3 + q4 == Quaternion(-0.5345224838248488, 0.0, 0.2672612419124244, 0.8017837257372731)
    assert q4 + q3 == Quaternion(-0.5345224838248488, 0.2672612419124244, 0.8017837257372732, 0.0)
    assert q4[0] == 1.0 == q4.w
    assert q4[1] == 0.0 == q4.x
    assert q4[2] == 3.0 == q4.y
    assert q4[3] == 2.0 == q4.z
    assert q4 * 2 == 2 * Quaternion(0.2672612419124244, 0.0, 0.8017837257372732, 0.5345224838248488)
    assert str( 2 * q4 ) == 'Quaternion(2, 0, 6, 4)'

    q3q4 = q3 + q4
    q4q3 = q4 + q3

    assert (q3q4 - q3) == q4
    assert (q4q3 - q4) == q3

def test_16():
    '''
    Test Matrix and Quaternion Implementations.
    __str__ and __repr__ methods
    trace method -- gets the trace of a Matrix
    PRVtoQuaternion global function -- given a rotation vector and angle give the equivalent Quaternion
    toMatrix method -- convert a Quaternion to its equivalent Matrix frame rotation
    toQuaternion method -- convert a Matrix (frame rotation) to its equivalent Quaternion
    isOrthogonal method -- checks if a Matrix is orthogonal or orthonormal
    tranpose method -- gets the tranpose of a Matrix
    Matrix-Vector Multiplication
    Matrix-Matrix Multiplcation
    conjugate method -- gets the opposite Quaternion of a Quaternion
    rotate method -- given a point or a Vector, rotate it using a point rotation matrix equivalent of the Quaternion used
    RPY_toYPR_quaternion -- given a Vector representing the Roll, Pitch, Yaw orientation, get the equivalent Quaternion for 3-2-1 sequence rotation 
    '''
    M = Matrix()
    V = Vector(5,3,4)

    assert str(M) == 'Matrix(1, 0, 0; 0, 1, 0; 0, 0, 1)'
    assert str(V) == 'Vector(5, 3, 4)'
    assert str(M*V) == 'Vector(5, 3, 4)'
    assert str(2*M) == 'Matrix(2, 0, 0; 0, 2, 0; 0, 0, 2)'
    assert str(2*M*V) == 'Vector(10, 6, 8)'
    assert str(M.trace()) == '3'

    PRV = Vector(1,0,0)
    Arg = 45
    Q  = PRVtoQuaternion(PRV,Arg)
    M  = Q.toMatrix()
    assert Q == Quaternion(0.9238795325112867, 0.3826834323650898, 0.0, 0.0)
    assert str(Q.toMatrix()) == 'Matrix(1.0, 0.0, 0.0; 0.0, 0.7071067811865475, 0.7071067811865476; 0.0, -0.7071067811865476, 0.7071067811865475)'
    assert M.toQuaternion() == Quaternion(0.9238795325112867, 0.3826834323650898, 0.0, 0.0)
    assert Q == M.toQuaternion()
    assert M.isOrthogonal() 

    PRV = Vector(0,1,0)
    Arg = 45
    Q = PRVtoQuaternion(PRV,Arg)
    M  = Q.toMatrix()
    assert Q == Quaternion(0.9238795325112867, 0.0, 0.3826834323650898, 0.0)
    assert str(Q.toMatrix()) == 'Matrix(0.7071067811865475, 0.0, -0.7071067811865476; 0.0, 1.0, 0.0; 0.7071067811865476, 0.0, 0.7071067811865475)'
    assert M.toQuaternion() == Quaternion(0.9238795325112867, 0.0, 0.3826834323650898, 0.0)
    assert Q == M.toQuaternion() 
    assert M.isOrthogonal()

    PRV = Vector(0,0,1)
    Arg = 45
    Q = PRVtoQuaternion(PRV,Arg)
    M  = Q.toMatrix()
    assert Q == Quaternion(0.9238795325112867, 0.0, 0.0, 0.3826834323650898)
    assert str(Q.toMatrix()) == 'Matrix(0.7071067811865475, 0.7071067811865476, 0.0; -0.7071067811865476, 0.7071067811865475, 0.0; 0.0, 0.0, 1.0)'
    assert M.toQuaternion() == Quaternion(0.9238795325112867, 0.0, 0.0, 0.3826834323650898)
    assert Q == M.toQuaternion()
    assert M.isOrthogonal()

    Vx = Vector(1,0,0)
    Vy = Vector(0,1,0)
    Vz = Vector(0,0,1)

    M = Matrix(x=Vector(0.892539, -0.275451, 0.357073), y=Vector(0.157379, 0.932257, 0.325773), z=Vector(-0.422618, -0.234570, 0.875426))
    assert M.toQuaternion() == Quaternion(0.9617980557268766, -0.14564985774912026, 0.20266494493242407, 0.11250542601505098)
    assert M.isOrthogonal()

    I = M * M.transpose()
    assert I.isOrthogonal()

    Mt = M.transpose()
    assert (M * Mt * Vx).sum() - 1 <= 1e-3
    assert (M * Mt * Vy).sum() - 1 <= 1e-3
    assert (M * Mt * Vz).sum() - 1 <= 1e-3

    M = Matrix(x=Vector(5,1,1), y=Vector(1,3,1), z=Vector(1,1,4))
    Mt = M.transpose()
    assert M*Vx == Vector(5,1,1)
    assert Mt*Vx == Vector(5,1,1)
    assert M*Vy == Vector(1,3,1)
    assert Mt*Vy == Vector(1,3,1)
    assert M*Vz == Vector(1,1,4)
    assert Mt*Vz == Vector(1,1,4)

    M = Matrix(x=Vector(5,1,2), y=Vector(1,3,2), z=Vector(1,2,4))
    Mt = M.transpose()
    assert M*Vx == Vector(5,1,2)
    assert Mt*Vx == Vector(5,1,1)
    assert M*Vy == Vector(1,3,2)
    assert Mt*Vy == Vector(1,3,2)
    assert M*Vz == Vector(1,2,4)
    assert Mt*Vz == Vector(2,2,4)

    Q_zrot = PRVtoQuaternion(Vz,30)
    M_zrot = Q_zrot.toMatrix()
    Q_yrot = PRVtoQuaternion(Vy,-60)
    M_yrot = Q_yrot.toMatrix()
    Q_xrot = PRVtoQuaternion(Vx,135)
    M_xrot = Q_xrot.toMatrix()

    Q_zyxrot = (Q_zrot + Q_yrot) + Q_xrot
    M_zyxrot = M_xrot * (M_yrot * M_zrot)

    assert Q_zyxrot == M_zyxrot.toQuaternion()

    Euler = Vector(135,-60,30)
    assert Euler.RPY_toYPR_quaternion() == Q_zyxrot

    assert (Q_zyxrot.rotate(Vx) - M_zyxrot.transpose() * Vx).magnitude() <= 1e-8

    Q_z = PRVtoQuaternion(Vz, 90)
    M_z = Q_z.toMatrix()

    assert (M_z.x - Vector(0,-1,0)).magnitude() <= 1e-8
    assert (M_z.y - Vector(1,0,0)).magnitude() <= 1e-8
    assert (M_z.z - Vector(0,0,1)).magnitude() <= 1e-8
    assert (Vector(0,1,0) - M_z.transpose() * Vx).magnitude() <= 1e-8
    assert (Vector(0,-1,0) - Q_z.conjugate().rotate(Vx)).magnitude() <= 1e-8
    assert (Vector(0,1,0) - Q_z.rotate(Vx)).magnitude() <= 1e-8

def test_17():
    '''
    Testing the sensor class functions.
    Using custom functions to define gyroscope and gps sensors.
    nameofsensor = Sensor('NAMEOFSENSOR') - create an empty sensor class
    nameofsensor.setMethod(customfunction) - sets the custom function to the sensor class
    spacecraft["NAMEOFCRAFT"].addSensor(nameofsensor) - adds the sensor class to a spacecraft 
    sensorlist = spacecraft["NAMEOFCRAFT"].getSensors() - gets the list of all sensors (pointers to the sensors class)
    sensorlist["NAMEOFSENSOR"] - gets the specific sensor from the list
    '''
    system = LEOSS()
    system.epoch(2023,9,26,3,11,18,0)

    system.addSpacecraft("DIWATA", ["State", "Location", "Netforce"])

    spacecraft = system.getSpacecrafts()
    recorder   = system.getRecorders()

    spacecraft["DIWATA"].setmass(50)
    spacecraft["DIWATA"].setsize(Vector(0.1,0.1,0.1))
    spacecraft["DIWATA"].setposition(1e3*Vector(4395.079058029986, 3631.5889348004957, -3712.575674067216))
    spacecraft["DIWATA"].setvelocity(1e3*Vector(-5.76886641743168, 2.5823185921356733, -4.310210403510053))
    spacecraft["DIWATA"].setbodyrate(Vector(5,-4,3))
    spacecraft["DIWATA"].setorientation(Vector(0,0,0))

    gyroscope = Sensor("gyro")
    gps       = Sensor("gps")

    def gyrofunction(spacecraft, args):
        return spacecraft.state.bodyrate
    
    def gpsfunction(spacecraft, args):
        return spacecraft['Location']
    
    gyroscope.setMethod(gyrofunction)
    gps.setMethod(gpsfunction)

    spacecraft["DIWATA"].addSensor(gyroscope)
    spacecraft["DIWATA"].addSensor(gps)

    sensors = spacecraft["DIWATA"].getSensors()

    assert sensors['gyro'] == gyroscope
    assert sensors['gps'] == gps
    assert sensors['gyro'].attachedTo == spacecraft["DIWATA"]
    assert sensors['gyro'].system == system
    assert spacecraft["DIWATA"]['gyro'] == gyroscope.data
    assert spacecraft["DIWATA"]['gps'] == gps.data

    time = 60

    simulate(system, time)

    assert recorder["DIWATA"]['State'][-1].bodyrate == sensors['gyro'].data
    assert recorder["DIWATA"]['Location'][-1] == sensors['gps'].data
    assert recorder['DIWATA']['gps'][-1] == sensors['gps'].data
    assert recorder['DIWATA']['gps'][-1] == sensors['gps'].data
    assert recorder['DIWATA']['State'][1].bodyrate == recorder['DIWATA']['gyro'][1]
