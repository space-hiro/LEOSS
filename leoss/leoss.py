class LEOSS():

    def __init__(self):
        self.spacecraftObjects = []
        self.time = 0
        self.mu = 398600.4418e9

    def addSpacecraft(self, name):
        spacecraft = Spacecraft(name)
        self.spacecraftObjects.append(spacecraft)

    def listSpacecraft(self):
        names = []
        for spacecraft in self.spacecraftObjects:
            names.append(spacecraft.name)
        return names
    
    def numSpacecraft(self):
        return len(self.spacecraftObjects)
    
    def advance1timestep(self, deltaTime):
        for spacecraft in self.spacecraftObjects:
            spacecraft.netforce = spacecraft.netforce + planetGravity(self.mu, spacecraft.state.mass, spacecraft.state.position)
            newstate = runggeKutta4(spacecraft, spacecraft.state, self.time, deltaTime)
            spacecraft.state = newstate
        self.time = self.time + deltaTime
    
    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= 0 and item < self.numSpacecraft():
                return self.spacecraftObjects[item]
            else:
                raise IndexError(f"There are only {self.numSpacecraft()} spacecraft objects")
        else:
            raise TypeError("Operand should be a positive int")

class Spacecraft():

    def __init__(self, name):
        self.name = name
        self.state = State()
        self.netforce = Vector(0,0,0)

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
        
    def derivative(self, state, time):
        deltaState = State()
        deltaState.mass = 0
        deltaState.position = state.velocity
        deltaState.velocity = self.netforce/state.mass
        return deltaState
        
    def getvelocity(self):
        return self.state.velocity
    
    def setvelocity(self, other):
        if isinstance(other, Vector):
            self.state.velocity = other
        else:
            raise TypeError("Operand should be a Vector")

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

class State():

    def __init__(self, mass=0.0, pos=Vector(), vel=Vector()):
        self.mass = mass
        self.position = pos
        self.velocity = vel

    def __add__(self, other):
        if isinstance(other, State):
            return State(
                self.mass + other.mass,
                self.position + other.position,
                self.velocity + other.velocity
                )
        else:
            raise TypeError("Operand must be a State")
    
    def __sub__(self, other):
        if isinstance(other, State):
            return State(
                self.mass - other.mass,
                self.position - other.position,
                self.velocity - other.velocity
                )
        else:
            raise TypeError("Operand must be a State")
    
    def __mul__(self, other):
        if isinstance(other, State):
            return State(
            self.mass * other.mass,
            self.position * other.position,
            self.velocity * other.velocity
            )
        elif isinstance(other, (int, float)):
            return State(
            self.mass * other,
            self.position * other,
            self.velocity * other
            )
        else:
            raise TypeError("Operand must be a State, int or float")
        
    def __rmul__(self, other):
        return self * other
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return State(
            self.mass / other,
            self.position / other,
            self.velocity / other
            )
        else:
            raise TypeError("Operand must be int, or float")
        
    def __eq__(self, other):
        if isinstance(other, State):
            return (self.mass == other.mass and self.position == other.position and self.velocity == other.velocity)
        else:
            raise TypeError("Operand must be a State")
        
    def __str__(self):
        return f'State({self.mass}, {self.position}, {self.velocity})'
    
    def __repr__(self):
        return self.__str__()
    

def planetGravity(parameter, mass, position):
    rho = position.magnitude()
    return -(parameter*mass/(rho**3))*position

def runggeKutta4(object, state, time, deltaTime):
    k1 = object.derivative(state, time)
    k2 = object.derivative(state + k1*deltaTime/2, time + deltaTime/2)
    k3 = object.derivative(state + k2*deltaTime/2, time + deltaTime/2)
    k4 = object.derivative(state + k3*deltaTime, time + deltaTime)
    k  = (1/6)*(k1 + 2*k2 + 2*k3 + k4)*deltaTime
    return state+k