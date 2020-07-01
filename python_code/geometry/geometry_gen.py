from building import Building
from building import BuildingRoom
from building import BuildingShape
from room_pref import RoomPref
import random

def get_test_building():
    rooms = []
    for i in range(8):
        rooms.append(BuildingRoom(RoomPref("Room" + str(i), i, 0, 0), BuildingShape(random.uniform(0.5, 3.0), random.uniform(0.5, 3.0), 
                                                                                    (random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)))))
    lot_shape = BuildingShape(20.0, 20.0, (0.0, 0.0))
    building = Building(rooms, lot_shape)
    return building.serialize()
