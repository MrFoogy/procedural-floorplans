from geometry.building import Building
from geometry.building import BuildingRoom
from geometry.building import BuildingShape
from geometry.room_pref import RoomPref
import random

def get_test_building():
    rooms = []
    for i in range(8):
        xdisplace = random.uniform(-10.0, 10.0)
        ydisplace = random.uniform(-10.0, 10.0)
        points = [[0.0, 0.0], [3.0, 0.0], [3.0, 1.0], [2.0, 1.0], [2.0, 2.0], [1.0, 2.0], [1.0, 1.0], [0.0, 1.0]]
        points = [[point[0] + xdisplace, point[1] + ydisplace] for point in points]
        room = BuildingRoom(RoomPref("Room" + str(i), i, 0, 0), BuildingShape(points))
        room.shape.random_transform_wall(0.5, 0.5)
        rooms.append(room)
    lot_shape = BuildingShape([(-10.0, -10.0), (10.0, -10.0), (10.0, 10.0), (-10.0, 10.0)])
    building = Building(rooms, lot_shape)
    return building.serialize()
