import datetime
import math
from tqdm import tqdm
import time as clock

R2D = 180/math.pi
D2R = math.pi/180

class Vector():

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'
    
    def __str__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'
    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError("There are only three elements in the vector")
        
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
                )
        else:
            raise TypeError("Operance must a Vector")
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z
                )
        else:
            raise TypeError("Operance must a Vector")
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z
                )
        elif isinstance(other, (int, float)):
            return Vector(
                self.x * other,
                self.y * other,
                self.z * other
                )
        else:
            raise TypeError("Operand must be Vector, int, or float")
        
    def __rmul__(self, other):
        return self * other
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                self.x / other,
                self.y / other,
                self.z / other
                )
        else:
            raise TypeError("Operand must be int, or float")
        
    def __eq__(self, other):
        if isinstance(other, Vector):
            return (self.x == other.x and self.y == other.y and self.z == other.z)
        else:
            raise TypeError("Operand must be Vector")
        
    def cross(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
                )
        else:
            raise TypeError("Operand must be Vector")

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self):
        magnitude = self.magnitude()
        return Vector(
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude
        )

class Quaternion():

    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        if self.magnitude() != 1 and self.magnitude() > 0:
            Q = self.normalize()
            self.w = Q.w
            self.x = Q.x
            self.y = Q.y
            self.z = Q.z 
        elif self.magnitude == 0:
            raise ValueError("Invalid quaternion, zero values")

    def __repr__(self):
        return f'Quaternion({self.w}, {self.x}, {self.y}, {self.z})'
    
    def __str__(self):
        return f'Quaternion({self.w}, {self.x}, {self.y}, {self.z})'
    
    def __getitem__(self, item):
        if item == 0:
            return self.w
        elif item == 1:
            return self.x
        elif item == 2:
            return self.y
        elif item == 3:
            return self.z
        else:
            raise IndexError("There are only four elements in the quaternion")
        
    def __add__(self, other):
        if isinstance(other, Quaternion):
            q = Quaternion(
                other.w * self.w - other.x * self.x - other.y * self.y - other.z * self.z,
                other.x * self.w + other.w * self.x + other.z * self.y - other.y * self.z,
                other.y * self.w - other.z * self.x + other.w * self.y + other.x * self.z,
                other.z * self.w + other.y * self.x - other.x * self.y + other.w * self.z
                )
            return q.normalize()
        else:
            raise TypeError("Operand must a Quaternion")
    
    def __sub__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(
                 other.w * self.w + other.x * self.x + other.y * self.y + other.z * self.z,
                -other.x * self.w + other.w * self.x + other.z * self.y - other.y * self.z,
                -other.y * self.w - other.z * self.x + other.w * self.y + other.x * self.z,
                -other.z * self.w + other.y * self.x - other.x * self.y + other.w * self.z
                )
        else:
            raise TypeError("Operand must a Quaternion")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other,
                self.z * other
                )
        else:
            raise TypeError("Operand must be Quaternion, int, or float")
        
    def __rmul__(self, other):
        return self * other
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(
                self.w / other,
                self.x / other,
                self.y / other,
                self.z / other
                )
        else:
            raise TypeError("Operand must be int, or float")
        
    def __eq__(self, other):
        if isinstance(other, Quaternion):
            if (self.w == other.w and self.x == other.x and self.y == other.y and self.z == other.z):
                return True
            elif (self-other).angle()*R2D < 1e-8:
                return True
            else:
                return False
        else:
            raise TypeError("Operand must be Quaternion")

    def magnitude(self):
        return (self.w**2 + self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self):
        magnitude = self.magnitude()
        return Quaternion(
            self.w / magnitude,
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude
        )
    
    def vector(self):
        return Vector(self.x, self.y, self.z)
    
    def angle(self):
        return 2*math.acos(self.w)
    
    def toMRP(self):
        return Vector(self.x, self.y, self.z) / (1 + self.magnitude())

class State():

    def __init__(self, mass=0.0, pos=Vector(), vel=Vector()):
        self.mass = mass
        self.position = pos
        self.velocity = vel

    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= 0 and item < len(self.__dict__):
                return list(self.__dict__.values())[item]
            else:
                raise IndexError(f"There are only {len(self.__dict__)} state variables")
        else:
            raise TypeError("Operand should be a positive int")
        
    def __setitem__(self, item, value):
        if isinstance(item, int):
            if item >= 0 and item < len(self.__dict__):
                key = list(self.__dict__.keys())[item]
                self.__dict__[key] = value
            else:
                raise IndexError(f"There are only {len(self.__dict__)} state variables")
        else:
            raise TypeError("Operand should be a positive int")

    def __add__(self, other):
        if isinstance(other, State):
            newstate = State()
            for i in range(0,len(self.__dict__),1):
                newstate[i] = self[i] + other[i]
            return newstate
        else:
            raise TypeError("Operand must be a State")
    
    def __sub__(self, other):
        if isinstance(other, State):
            newstate = State()
            for i in range(0,len(self.__dict__),1):
                newstate[i] = self[i] - other[i]
            return newstate
        else:
            raise TypeError("Operand must be a State")
    
    def __mul__(self, other):
        if isinstance(other, State):
            newstate = State()
            for i in range(0,len(self.__dict__),1):
                newstate[i] = self[i] * other[i]
            return newstate
        elif isinstance(other, (int, float)):
            newstate = State()
            for i in range(0,len(self.__dict__),1):
                newstate[i] = self[i] * other
            return newstate
        else:
            raise TypeError("Operand must be a State, int or float")
        
    def __rmul__(self, other):
        return self * other
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            newstate = State()
            for i in range(0,len(self.__dict__),1):
                newstate[i] = self[i] / other
            return newstate
        else:
            raise TypeError("Operand must be int, or float")
        
    def __eq__(self, other):
        if isinstance(other, State):
            for i in range(0,len(self.__dict__),1):
                if self[i] != other[i]:
                    return False
            return True
        else:
            raise TypeError("Operand must be a State")
        
    def __str__(self):
        out = str(self[0])
        for i in range(1,len(self.__dict__),1):
            out = out + ", " + str(self[i])
        return f'State({out})'
    
    def __repr__(self):
        return self.__str__()

class Spacecraft():

    def __init__(self, name):
        self.name = name
        self.state = State()
        self.netforce = Vector(0,0,0)
        self.location = Vector(0,0,0)
        self.system = None

    def getmass(self):
        return self.state.mass

    def setmass(self, other):
        if isinstance(other, (int, float)):
            self.state.mass = other
        else:
            raise TypeError("Operand should be int or float")

    def getposition(self):
        return self.state.position
    
    def setposition(self, other):
        if isinstance(other, Vector):
            self.state.position = other
        else:
            raise TypeError("Operand should be a Vector")
        
    def getvelocity(self):
        return self.state.velocity
    
    def setvelocity(self, other):
        if isinstance(other, Vector):
            self.state.velocity = other
        else:
            raise TypeError("Operand should be a Vector")
        
    def derivative(self, state: State, time):
        self.clearForces()
        deltaState = State()
        deltaState.mass = 0
        deltaState.position = state.velocity
        self.netforce = self.netforce + systemGravity(self.system, state.mass, state.position)
        deltaState.velocity = self.netforce/state.mass
        return deltaState
    
    def clearForces(self):
        self.netforce = Vector(0,0,0)

    def __getitem__(self, item):
        if isinstance(item, str):
            if item == "State": 
                return self.state
            elif item == "Netforce": 
                return self.netforce
            elif item == "Location": 
                return self.location
            else:
                raise TypeError("Operand should be a recorder item")
        else:
            raise TypeError("Operand should be a recorder item in str")

class Recorder():

    def __init__(self, datetime: datetime.datetime,  spacecraft: Spacecraft, datalist: list):
        self.attachedTo   = spacecraft
        self.attachedWhen = datetime
        self.dataDict = { "Datetime" : [] }

        for item in datalist:
            self.dataDict[item] = []
        self.update(datetime)
    
    def update(self, datetime: datetime.datetime):
        Datetime = datetime
        self.dataDict["Datetime"].append(Datetime)

        for item in list(self.dataDict.keys())[1:]:
            self.dataDict[item].append(self.attachedTo[item])

    def __getitem__(self, item):
        if isinstance(item, str) and item in self.dataDict.keys():
            return self.dataDict[item]
        else:
            raise TypeError("Operand should be recorder item")

class LEOSS():

    def __init__(self):
        self.spacecraftObjects = []
        self.recorderObjects = {}
        self.time = 0.0
        self.mu = 398600.4418e9
        self.radi = 6378.137e3
        self.epochDT(datetime.datetime.today())

    def epochDT(self, dt: datetime.datetime):
            self.epoch(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)

    def epoch(self, year=0, month=0, day=0, hour=0, minute=0, second=0, microsecond=0):
            
            self.datetime0 = datetime.datetime(year, month, day, hour, minute, second, microsecond)
            self.jdate0 = 367*year - int((7*(year + int((month+9)/12)))/4) + int(275*month/9) + day + 1721013.5
            
            hours  = hour + minute/60 + second/3600 + microsecond/3600000000
            j2000  = 2451545
            T0     = (self.jdate0 - j2000)/36525
            
            gmst0_ =  100.4606184 + 36000.77004*T0 + 0.000387933*(T0**2) - (2.583e-8)*(T0**3)

            self.gmst0 = gmst0_%360
            self.gmst  = self.gmst0 + 360.98564724*hours/24

    def datenow(self):
        return self.datetime0 + datetime.timedelta(seconds=self.time)

    def addSpacecraft(self, name, recordList: list = ["State"]):
        spacecraft = Spacecraft(name)
        spacecraft.system = self
        self.spacecraftObjects.append(spacecraft)
        recorder = Recorder(self.datenow(), spacecraft, recordList)
        self.recorderObjects[name] = recorder

    def listSpacecraft(self):
        names = []
        for spacecraft in self.spacecraftObjects:
            names.append(spacecraft.name)
        return names
    
    def getSpacecrafts(self):
        spacecraftDict = {}
        for spacecraft in self.spacecraftObjects:
            spacecraftDict[spacecraft.name] = spacecraft
        return spacecraftDict
    
    def getRecorders(self):
        return self.recorderObjects
    
    def numSpacecraft(self):
        return len(self.spacecraftObjects)
    
    def advance1timestep(self, deltaTime):
        for spacecraft in self.spacecraftObjects:
            spacecraft.location = self.locate(spacecraft)
            newstate = runggeKutta4(spacecraft.derivative, spacecraft.state, self.time, deltaTime)
            spacecraft.state = newstate
            self.recorderObjects[spacecraft.name].update(self.datenow()+datetime.timedelta(seconds=deltaTime))
        self.time = self.time + deltaTime

    def initRecorders(self):
        for spacecraft in self.spacecraftObjects:
            self.recorderObjects[spacecraft.name].update(self.datenow())
    
    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= 0 and item < self.numSpacecraft():
                return self.spacecraftObjects[item]
            else:
                raise IndexError(f"There are only {self.numSpacecraft()} spacecraft objects")
        else:
            raise TypeError("Operand should be a positive int")
        
    def locate(self, spacecraft: Spacecraft):
        
        position = spacecraft.getposition()

        mag = position.magnitude()

        theta = math.acos(position.z/mag)
        psi   = math.atan2(position.y,position.x)

        latitude  = 90 - (theta*R2D)
        longitude = psi*R2D
        altitude  = (mag-self.radi)/1000

        xy = math.sqrt(position.x**2+position.y**2)

        gd_theta = latitude*D2R
        C = 0
        gd = 0
        e2 = 0.006694385000

        while True:
            C = self.radi/math.sqrt(1-e2*math.sin(gd_theta)*math.sin(gd_theta))
            gd = math.atan2(position.z+C*e2*math.sin(gd_theta),xy)
            if abs(gd-gd_theta) < 1e-6:
                gd_theta = gd
                break
            gd_theta = gd
        
        h_ellp = ( xy/math.cos(gd_theta) ) - C  
        
        altitude = h_ellp/1e3
        latitude = gd_theta*R2D

        gmst_ = self.gmst + self.time*(360.98564724)/(24*3600) 
        longitude = longitude - gmst_
        if longitude < 0:
            longitude = (((longitude/360) - int(longitude/360)) * 360) + 360    
        if longitude > 180:
            longitude = -360 + longitude
        
        location = Vector(latitude, longitude, altitude)
        return location


def systemGravity(system: LEOSS, mass, position):
    rho = position.magnitude()
    return -(system.mu*mass/(rho**3))*position

def runggeKutta4(derivative, state, time, deltaTime):
    k1 = derivative(state, time)
    k2 = derivative(state + k1*deltaTime/2, time + deltaTime/2)
    k3 = derivative(state + k2*deltaTime/2, time + deltaTime/2)
    k4 = derivative(state + k3*deltaTime, time + deltaTime)
    k  = (1/6)*(k1 + 2*k2 + 2*k3 + k4)*deltaTime
    return state + k

def simulate(system: LEOSS, timeEnd, timeStep=1/32):
    
    for spacecraft in system.spacecraftObjects:
        spacecraft.location = system.locate(spacecraft)
        spacecraft.derivative(spacecraft.state, system.time)

    system.initRecorders()

    while system.time < timeEnd:
        system.advance1timestep(timeStep)

def simulateProgress0(system: LEOSS, timeEnd, timeStep=1/32):
    
    for spacecraft in system.spacecraftObjects:
        spacecraft.location = system.locate(spacecraft)
        spacecraft.derivative(spacecraft.state, system.time)

    system.initRecorders()
    
    with tqdm(total = timeEnd) as pbar:
        while system.time < timeEnd:
            system.advance1timestep(timeStep)
            pbar.update(timeStep)

def simulateProgress(system: LEOSS, timeEnd, timeStep=1/32):
    
    for spacecraft in system.spacecraftObjects:
        spacecraft.location = system.locate(spacecraft)
        spacecraft.derivative(spacecraft.state, system.time)

    system.initRecorders()

    print("\nRun Simulation (from "+str(system.time)+" to "+str(timeEnd)+", step="+str(timeStep)+")")
    t0 = clock.time()

    pbar = tqdm(total=timeEnd-system.time, position=0, desc='Simulating', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}')
    
    while(system.time < timeEnd):
        prev_time = system.time
        system.advance1timestep(timeStep)        
        pbar.update(system.time - prev_time)
    pbar.close()

    t1 = clock.time()
    print("\nElapsed Time:\t"+str(t1-t0)+" sec.")