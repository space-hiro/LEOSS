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
