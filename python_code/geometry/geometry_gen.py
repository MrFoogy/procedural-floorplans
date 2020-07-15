from geometry.building import Building
from geometry.building import BuildingRoom
from geometry.building import BuildingShape
from geometry.room_pref import RoomPref
from geometry.wall_set import WallSet
import geometry.util as util
import random

def get_test_building():
    adjacency_dict = {}
    """
    for i in range(500,600):
        random.seed(i)
        building = generate_building(adjacency_dict)
        if len(building) < 80:
            print("Seed: ", i, flush=True)
            return building
            """
    random.seed(502)
    #adjacency_dict = { 0: [1,2], 1: [0, 2], 2: [0, 1]}
    return generate_building(adjacency_dict)

def initialize_room(min_pos, max_pos, grid_size, index, building, pref_area, pref_aspect):
    width = 0.25
    height = 0.25
    points = [[-width, -height], [width, -height], [width, height], [-width, height]]
    xdisplace = points[index][0]
    ydisplace = points[index][1]
    points = [[point[0] + xdisplace, point[1] + ydisplace] for point in points]
    room = BuildingRoom(RoomPref("Room" + str(index), index, pref_area, pref_aspect), 
                        BuildingShape(points, index), index)
    walls_h = room.shape.get_walls_for_axis(True)
    walls_v = room.shape.get_walls_for_axis(False)
    for wall in walls_h: 
        building.walls_horizontal.add_wall(wall[0], wall[1][0], wall[1][1], index)
    for wall in walls_v: 
        building.walls_vertical.add_wall(wall[0], wall[1][0], wall[1][1], index)
    return room

def initalize_lot(corners, building):
    lot_shape = BuildingShape(corners, -1)
    walls_h = lot_shape.get_walls_for_axis(True)
    walls_v = lot_shape.get_walls_for_axis(False)
    for wall in walls_h: 
        building.walls_horizontal.add_wall(wall[0], wall[1][0], wall[1][1], -1)
    for wall in walls_v: 
        building.walls_vertical.add_wall(wall[0], wall[1][0], wall[1][1], -1)
    return lot_shape

def generate_building(adjacency_dict):
    results = []
    min_pos = (-10.0, -10.0)
    max_pos = (10.0, 10.0)
    grid_size = 0.5
    building = Building([], grid_size, WallSet(), WallSet(), adjacency_dict)
    building.lot_shape = initalize_lot([(-10.0, -10.0), (10.0, -10.0), (10.0, 10.0), (-10.0, 10.0)], building)
    for i in range(4):
        new_room = initialize_room(min_pos, max_pos, grid_size, i, building, 2.0, 2.0)
        building.rooms.append(new_room)
    #building.print_wall_lists()
    num_iterations = 20
    results.append(building.serialize())
    iter = 1
    for i in range(num_iterations):
        try:
            for room in building.rooms:
                iter += 1
                if iter == 31:
                    for i in range(20):
                        print("DONALD TRUMP", flush=True)
                room.shape.random_transform_wall(grid_size, 0.2, 1.0, 0.0, building)
                results.append(building.serialize())
                for wall_vertical in building.walls_vertical.walls:
                    if wall_vertical[0] == 1.0:
                        if 1 in wall_vertical[1]:
                            if wall_vertical[1][1].count([-0.5, 0.5]) > 1:
                                print("Double at ", iter, flush=True)
                #print("Now it was: ", room.room_id, flush=True)
                #building.print_wall_lists()
        except:
            break
    #building.print_wall_lists()
    print("Cost function: ", building.get_cost_function(), flush=True)
    return results

