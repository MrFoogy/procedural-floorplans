class Building:
    def __init__(self, rooms, lot_shape):
        self.rooms = rooms
        self.lot_shape = lot_shape
    
    def serialize(self):
        return {"rooms": [room.serialize() for room in self.rooms], "lot": self.lot_shape.serialize()}


class BuildingRoom:
    def __init__(self, room, shape):
        self.room = room
        self.shape = shape
    
    def serialize(self):
        return {"name": self.room.name, "shape": self.shape.serialize()}


class BuildingShape:
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        self.position = position
    
    def get_area(self):
        return self.width * self.height

    def get_aspect(self):
        return self.width / self.height

    def serialize(self):
        return {"width": self.width, "height": self.height, "position": self.position}