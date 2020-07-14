from geometry.building import Building
from geometry.building import BuildingRoom
from geometry.building import BuildingShape
from geometry.room_pref import RoomPref
from geometry.wall_set import WallSet
import geometry.util as util
import random

def get_test_building():
    building = generate_building()
    return building.serialize()

def initialize_room(min_pos, max_pos, grid_size, index, building):
    xdisplace = util.get_random_grid(min_pos[0], max_pos[0], grid_size)
    ydisplace = util.get_random_grid(min_pos[1], max_pos[1], grid_size)
    points = [[0.0, 0.0], [3.0, 0.0], [3.0, 1.0], [2.0, 1.0], [2.0, 2.0], [1.0, 2.0], [1.0, 1.0], [0.0, 1.0]]
    points = [[point[0] + xdisplace, point[1] + ydisplace] for point in points]
    room = BuildingRoom(RoomPref("Room" + str(index), index, 0, 0), BuildingShape(points, index), index)
    walls_h = room.shape.get_walls_for_axis(True)
    walls_v = room.shape.get_walls_for_axis(False)
    for wall in walls_h: 
        building.walls_horizontal.add_wall(wall[0], wall[1][0], wall[1][1], index)
    for wall in walls_v: 
        building.walls_vertical.add_wall(wall[0], wall[1][0], wall[1][1], index)
    return room

def generate_building():
    min_pos = (-10.0, -10.0)
    max_pos = (10.0, 10.0)
    grid_size = 0.25
    lot_shape = BuildingShape([(-10.0, -10.0), (10.0, -10.0), (10.0, 10.0), (-10.0, 10.0)], -1)
    building = Building([], lot_shape, grid_size, WallSet(), WallSet())
    for i in range(1):
        new_room = initialize_room(min_pos, max_pos, grid_size, i, building)
        building.rooms.append(new_room)
    building.print_wall_lists()
    for room in building.rooms:
        room.shape.random_transform_wall(grid_size, 0.0, 0.0, 1.0, building)
    building.print_wall_lists()
    return building

