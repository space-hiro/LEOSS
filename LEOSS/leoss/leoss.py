class LEOSS():

    def __init__(self):
        self.spacecraftObjects = []
        self.time = 0

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

class Spacecraft():

    def __init__(self, name):
        self.name = name
        self.state = State()

class Vector():

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z}'
    
    def __str__(self):
        return f'Vector({self.x}, {self.y}, {self.z}'
    
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
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
            )
    
    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
            )
    
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
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                self.x / other,
                self.y / other,
                self.z / other
                )
        else:
            raise TypeError("Operand must be int, or float")
        
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