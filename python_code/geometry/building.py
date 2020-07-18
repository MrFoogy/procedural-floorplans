import random
import geometry.util as util
import copy

class Building:
    def __init__(self, rooms, grid_size, walls_horizontal, walls_vertical, adjacency_dict):
        self.rooms = rooms
        self.grid_size = grid_size
        self.walls_horizontal = walls_horizontal
        self.walls_vertical = walls_vertical
        self.adjacency_dict = adjacency_dict
    
    def serialize(self):
        return {"rooms": [room.serialize() for room in self.rooms], "lot": self.lot_shape.serialize(), 
                "gridSize": self.grid_size}

    def print_wall_lists(self):
        print("Horizontal: ", self.walls_horizontal.walls, flush=True)
        print("Vertical: ", self.walls_vertical.walls, flush=True)
    
    def get_wall_set(self, is_horizontal):
        return self.walls_horizontal if is_horizontal else self.walls_vertical
    
    def push_hit_walls(self, pushing_shape, start_index, distance):
        next_index = (start_index + 1) % len(pushing_shape.points)
        is_horizontal = pushing_shape.is_wall_horizontal(start_index)
        cross_coord_index = 1 if is_horizontal else 0
        align_coord_index = 0 if is_horizontal else 1
        wall_set = self.walls_horizontal if is_horizontal else self.walls_vertical
        start_cross = pushing_shape.points[start_index][cross_coord_index]
        end_cross = start_cross + distance
        scan_end_cross = end_cross
        # Make sure not to scan the walls at the end point of the push
        if distance < 0:
            scan_end_cross += self.grid_size
        else:
            scan_end_cross -= self.grid_size
        align_coord_1 = pushing_shape.points[start_index][align_coord_index]
        align_coord_2 = pushing_shape.points[next_index][align_coord_index]
        align_start = min(align_coord_1, align_coord_2)
        align_end = max(align_coord_1, align_coord_2)
        scanned_walls = wall_set.scan_walls(min(start_cross, scan_end_cross), 
                                            max(start_cross, scan_end_cross), 
                                            align_start, align_end, False)

        for room_id in scanned_walls:
            if room_id == pushing_shape.room_id:
                continue
            hit_shape = self.rooms[room_id].shape
            for scanned_wall_info in scanned_walls[room_id]:
                wall_start, wall_end, start_index, end_index = scanned_wall_info[1]
                cross_coord = scanned_wall_info[0]
                hit_shape.push_wall_at(is_horizontal, wall_start, wall_end, cross_coord, 
                                       align_start, align_end, end_cross, self, pushing_shape)
    
    def get_connected_rooms(self):
        res = { room_id : set() for room_id in range(len(self.rooms)) }
        door_width = 0.75
        wall_sets = [self.walls_horizontal.walls, self.walls_vertical.walls]
        for wall_set in wall_sets:
            for aligned_walls in wall_set:
                for room_id_1 in aligned_walls[1]:
                    for room_id_2 in aligned_walls[1]:
                        if room_id_1 == -1 or room_id_2 == -1:
                            continue
                        if room_id_1 == room_id_2:
                            continue
                        for wall_coords_1 in aligned_walls[1][room_id_1]:
                            for wall_coords_2 in aligned_walls[1][room_id_2]:
                                if util.is_wall_overlapping_length(wall_coords_1[0], wall_coords_1[1],
                                                                   wall_coords_2[0], wall_coords_2[1], door_width):
                                    res[room_id_1].add(room_id_2)
                                    res[room_id_2].add(room_id_1)
        return res

    def get_cost_function(self):
        sum = 0
        adjacency_cost = self.get_adjacency_cost()
        dimension_cost = self.get_dimension_cost()
        shape_cost = self.get_shape_cost()
        print("Adjacency: ", adjacency_cost, flush=True)
        print("Dimension: ", dimension_cost, flush=True)
        print("Shape: ", shape_cost, flush=True)
        sum += 10.0 * adjacency_cost
        sum += 0.1 * dimension_cost
        sum += 0.1 * shape_cost
        return sum

    def get_adjacency_cost(self):
        current_adjacencies = self.get_connected_rooms()
        print(current_adjacencies, flush=True)
        print(self.adjacency_dict, flush=True)
        unmet_conditions = 0
        for room_id in self.adjacency_dict:
            for connected_id in self.adjacency_dict[room_id]:
                if connected_id not in current_adjacencies[room_id]:
                    unmet_conditions += 1
        # Since every connection is counted twice, divide by 2
        return unmet_conditions / 2
    
    def get_dimension_cost(self):
        sum = 0
        for room in self.rooms:
            actual_area = room.shape.get_area()
            actual_aspect = room.shape.get_aspect()
            sum += abs(actual_area - room.room_pref.pref_size) + \
                abs(actual_aspect - room.room_pref.pref_aspect)
        return sum

    def get_shape_cost(self):
        sum = 0
        for room in self.rooms:
            area = room.shape.get_area()
            sum += len(room.shape.points) + (room.shape.get_aabb_area() - area) / area
        return sum


class BuildingRoom:
    def __init__(self, room_pref, shape, room_id):
        self.room_pref = room_pref
        self.shape = shape
        self.room_id = room_id
    
    def serialize(self):
        return {"name": self.room_pref.name, "shape": self.shape.serialize()}


class BuildingShape:
    def __init__(self, points, room_id):
        """
        The points are the vertices of the shape
        Two subsequent points are considered connected (wraps around at the end)
        """
        self.points = points
        self.room_id = room_id

    def get_aspect(self):
        aabb = self.get_aabb()
        width = aabb[1][0] - aabb[0][0]
        height = aabb[1][1] - aabb[0][1]
        return max(width, height) / min(width, height)

    def get_aabb(self):
        min_x = float('inf')
        max_x = -float('inf')
        min_y = float('inf')
        max_y = -float('inf')
        for point in self.points:
            min_x = min(point[0], min_x)
            max_x = max(point[0], max_x)
            min_y = min(point[1], min_y)
            max_y = max(point[1], max_y)
        return [(min_x, min_y), (max_x, max_y)]
    
    def get_aabb_area(self):
        aabb = self.get_aabb()
        return (aabb[1][0] - aabb[0][0]) * (aabb[1][1] - aabb[0][1])

    def get_area(self):
        sum = 0.0
        for i in range(0, len(self.points)):
            j = (i + 1) % len(self.points)
            sum += self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1]
        return sum / 2
    
    def is_wall_horizontal(self, start_index):
        next_index = (start_index + 1) % len(self.points)
        return (abs(self.points[start_index][0] - self.points[next_index][0]) > 
                abs(self.points[start_index][1] - self.points[next_index][1]))

    def get_walls_for_axis(self, get_horizontal):
        res = []
        for start_index in range(len(self.points)):
            next_index = (start_index + 1) % len(self.points)
            is_horizontal = self.is_wall_horizontal(start_index)
            if is_horizontal and get_horizontal:
                res.append(self.get_wall_info(start_index))
                start_x = min(self.points[start_index][0], self.points[next_index][0])
                end_x = max(self.points[start_index][0], self.points[next_index][0])
                res.append([self.points[start_index][1], [start_x, end_x]])
            if (not is_horizontal) and (not get_horizontal):
                res.append(self.get_wall_info(start_index))
                start_y = min(self.points[start_index][1], self.points[next_index][1])
                end_y = max(self.points[start_index][1], self.points[next_index][1])
                res.append([self.points[start_index][0], [start_y, end_y]])
        return res
    
    def can_push_wall(self, start_index, distance, building):
        # Scan walls
        next_index = (start_index + 1) % len(self.points)
        is_horizontal = self.is_wall_horizontal(start_index)
        cross_coord_index = 1 if is_horizontal else 0
        align_coord_index = 0 if is_horizontal else 1
        wall_set = building.walls_horizontal if is_horizontal else building.walls_vertical
        start_cross = self.points[start_index][cross_coord_index]
        align_coord_1 = self.points[start_index][align_coord_index]
        align_coord_2 = self.points[next_index][align_coord_index]
        align_start = min(align_coord_1, align_coord_2)
        align_end = max(align_coord_1, align_coord_2)
        scanned_walls = wall_set.scan_walls(min(start_cross, start_cross + distance), 
                                                  max(start_cross, start_cross + distance),
                                                  align_start, align_end, True)
                                        
        # If two walls from the same room overlap on the align axis, that room section would disappear
        # making such a push illegal
        for room_id in scanned_walls:
            # This is the boundary
            if room_id == -1:
                return False
            if len(scanned_walls[room_id]) < 2:
                continue
            for i in range(len(scanned_walls[room_id])):
                for j in range(len(scanned_walls[room_id])):
                    if i == j:
                        continue
                    wall_1 = scanned_walls[room_id][i][1]
                    wall_2 = scanned_walls[room_id][j][1]
                    room = building.rooms[room_id]
                    if util.is_wall_overlapping(wall_1[0], wall_1[1], wall_2[0], wall_2[1]):
                        return False
                    if wall_1[1] == wall_2[0]:
                        if not room.shape.are_points_connected(wall_1[3], wall_2[2]):
                            return False
                    if wall_1[0] == wall_2[1]:
                        if not room.shape.are_points_connected(wall_1[2], wall_2[3]):
                            return False

        return True
    
    def are_points_connected(self, index_1, index_2):
        return min((index_1 - index_2) % len(self.points), (index_2 - index_1) % len(self.points)) == 1
    
    def snap_wall(self, start_index, snap_index, building):
        is_horizontal = self.is_wall_horizontal(start_index)
        if self.is_wall_horizontal(start_index) != self.is_wall_horizontal(snap_index):
            print("Snap is pranked!!!", flush=True)
        coord_index = 1 if is_horizontal else 0
        distance = self.points[snap_index][coord_index] - self.points[start_index][coord_index] 
        return self.push_wall(start_index, distance, building)
    
    def snap_wall_random(self, start_index, building):
        snap_index = None
        if random.uniform(0, 1) < 0.5:
            snap_index = (start_index - 2) % len(self.points)
        else:
            snap_index = (start_index + 2) % len(self.points)
        return self.snap_wall(start_index, snap_index, building)

    def push_wall(self, start_index, distance, building, is_original=True):
        if is_original and not self.can_push_wall(start_index, distance, building):
            return False

        if is_original:
            building.push_hit_walls(self, start_index, distance)
        
        next_index = (start_index + 1) % len(self.points)

        # Remove from wall set, 3 walls are affected
        self.remove_from_wall_set(start_index - 1, building)
        self.remove_from_wall_set(start_index, building)
        self.remove_from_wall_set(start_index + 1, building)

        is_horizontal = self.is_wall_horizontal(start_index)
        if is_horizontal:
            self.points[start_index][1] += distance
            self.points[next_index][1] += distance
        else:
            self.points[start_index][0] += distance
            self.points[next_index][0] += distance

        # Add back to wall set, 3 walls are affected
        self.add_to_wall_set(start_index - 1, building)
        self.add_to_wall_set(start_index, building)
        self.add_to_wall_set(start_index + 1, building)

        self.merge_unnecessary_walls(building)

        #print("Points after: ", self.points, flush=True)

    def push_wall_at(self, is_horizontal, wall_start, wall_end, wall_cross, align_start, align_end, end_cross, building, pushing_shape):
        # wall_start and wall_end are the current coordinates of the wall to be pushed
        # align_start and align_end is the section which is pushing this wall
        # end_cross is the end destination of the wall along the cross-axis

        # First, find which wall it is
        start_index = None
        is_reverse_order = False
        for i in range(len(self.points)):
            wall_is_horizontal = self.is_wall_horizontal(i)
            if wall_is_horizontal != is_horizontal:
                continue 
            j = (i + 1) % len(self.points)
            align_coord_index = 0 if is_horizontal else 1
            cross_coord_index = 1 - align_coord_index
            wall_coord_1 = self.points[i][align_coord_index]
            wall_coord_2 = self.points[j][align_coord_index]
            cross_coord = self.points[i][cross_coord_index]
            is_reverse_order = wall_start != self.points[i][align_coord_index]
            if (min(wall_coord_1, wall_coord_2) == wall_start and 
                max(wall_coord_1, wall_coord_2) == wall_end and cross_coord == wall_cross):
                start_index = i
                break
        if start_index is None:
            print("Couldn't find wall!", flush=True)
            """
            print("I am: ", self.room_id, self.points, flush=True)
            print("Pushed by: ", pushing_shape.room_id, pushing_shape.points, flush=True)
            print("Sought wall: ", is_horizontal, wall_start, wall_end, wall_cross, align_start, align_end, end_cross, flush=True)
            print("Whole building: ", building.serialize(), flush=True)
            """

        # Perform split if necessary
        split_points = []
        push_index = start_index
        if wall_start < align_start:
            split_points.append(align_start)
        if wall_end > align_end:
            split_points.append(align_end)
        if len(split_points) == 1:
            self.split_wall(start_index, split_points[0], building)
            # xor operation to determine push index
            if is_reverse_order != (wall_start < align_start):
                push_index = (start_index + 2) % len(self.points)
        if len(split_points) == 2:
            self.split_wall_double(start_index, split_points[0], split_points[1], building)
            push_index = (start_index + 2) % len(self.points)
        
        # Push the wall
        self.push_wall(push_index, end_cross - wall_cross, building, False)

    
    def get_wall_info(self, start_index):
        next_index = (start_index + 1) % len(self.points)
        is_horizontal = self.is_wall_horizontal(start_index)
        if is_horizontal:
            y = self.points[start_index][1]
            if self.points[start_index][0] < self.points[next_index][0]:
                return y, self.points[start_index][0], self.points[next_index][0], start_index, next_index, self.room_id
            else:
                return y, self.points[next_index][0], self.points[start_index][0], next_index, start_index, self.room_id
        else:
            x = self.points[start_index][0]
            if self.points[start_index][1] < self.points[next_index][1]:
                return x, self.points[start_index][1], self.points[next_index][1], start_index, next_index, self.room_id
            else:
                return x, self.points[next_index][1], self.points[start_index][1], next_index, start_index, self.room_id
    
    def is_wall_zero_length(self, start_index):
        next_index = (start_index + 1) % len(self.points)
        return self.points[start_index][0] == self.points[next_index][0] and \
            self.points[start_index][1] == self.points[next_index][1]
    
    def add_all_walls_to_wall_set(self, building):
        for i in range(len(self.points)):
            self.add_to_wall_set(i, building)
    
    def add_to_wall_set(self, index, building):
        index_mod = index % len(self.points)
        if self.is_wall_zero_length(index_mod):
            return
        pos, start, end, start_index, end_index, room_id = self.get_wall_info(index_mod)
        building.get_wall_set(self.is_wall_horizontal(index_mod)).add_wall(pos, start, end, start_index, end_index, room_id)

    def remove_from_wall_set(self, index, building):
        index_mod = index % len(self.points)
        if self.is_wall_zero_length(index_mod):
            return
        pos, start, end, start_index, end_index, room_id = self.get_wall_info(index_mod)
        building.get_wall_set(self.is_wall_horizontal(index_mod)).remove_wall(pos, start, end, room_id)

    def merge_walls(self, index_1, index_2, building):
        self.remove_from_wall_set(index_1, building)
        self.remove_from_wall_set(index_2, building)

        # Correct the index in case index_2 is the first point,
        # making the value of index_1 wrong
        if index_2 == 0:
            index_1 -= 1

        # Simply remove the second point
        del self.points[index_2]

        self.add_to_wall_set(index_1, building)
    
    def should_merge_walls(self, index_1, index_2):
        end_index = (index_2 + 1) % len(self.points)
        return self.points[index_1][0] == self.points[end_index][0] or self.points[index_1][1] == self.points[end_index][1]

    def merge_unnecessary_walls(self, building):
        num_points = len(self.points)
        for i in range(num_points):
            while (i < len(self.points) and self.should_merge_walls(i, (i + 1) % len(self.points))):
                self.merge_walls(i, (i + 1) % len(self.points), building)
            if i >= len(self.points):
                break
    
    def split_wall(self, start_index, coord, building):
        is_horizontal = self.is_wall_horizontal(start_index)

        # Remove from wall set
        self.remove_from_wall_set(start_index, building)

        pos = None
        if is_horizontal:
            pos = (coord, self.points[start_index][1])
        else:
            pos = (self.points[start_index][0], coord)
        self.points.insert(start_index + 1, [pos[0], pos[1]])
        self.points.insert(start_index + 1, [pos[0], pos[1]])

        # Remove from wall set
        self.add_to_wall_set(start_index, building)
        self.add_to_wall_set(start_index + 1, building)
        self.add_to_wall_set(start_index + 2, building)
    
    def split_wall_double(self, start_index, coord_1, coord_2, building):
        next_index = (start_index + 1) % len(self.points)
        is_horizontal = self.is_wall_horizontal(start_index)

        # Remove from wall set
        self.remove_from_wall_set(start_index, building)

        pos_1 = None
        pos_2 = None
        if is_horizontal:
            is_decreasing = self.points[next_index][0] < self.points[start_index][0]
            pos_1 = (max(coord_1, coord_2) if is_decreasing else min(coord_1, coord_2), self.points[start_index][1])
            pos_2 = (min(coord_1, coord_2) if is_decreasing else max(coord_1, coord_2), self.points[start_index][1])
        else:
            is_decreasing = self.points[next_index][1] < self.points[start_index][1]
            pos_1 = (self.points[start_index][0], max(coord_1, coord_2) if is_decreasing else min(coord_1, coord_2))
            pos_2 = (self.points[start_index][0], min(coord_1, coord_2) if is_decreasing else max(coord_1, coord_2))

        # Insert pos_2 first so that it gets pushed back
        self.points.insert(start_index + 1, [pos_2[0], pos_2[1]])
        self.points.insert(start_index + 1, [pos_2[0], pos_2[1]])
        self.points.insert(start_index + 1, [pos_1[0], pos_1[1]])
        self.points.insert(start_index + 1, [pos_1[0], pos_1[1]])

        # Add to wall set
        self.add_to_wall_set(start_index, building)
        self.add_to_wall_set(start_index + 1, building)
        self.add_to_wall_set(start_index + 2, building)
        self.add_to_wall_set(start_index + 3, building)
        self.add_to_wall_set(start_index + 4, building)

    def split_wall_random(self, start_index, grid_size, building):
        next_index = (start_index + 1) % len(self.points)
        is_horizontal = self.is_wall_horizontal(start_index)
        coord_index = 0 if is_horizontal else 1
        min_coord = min(self.points[start_index][coord_index], self.points[next_index][coord_index])
        max_coord = max(self.points[start_index][coord_index], self.points[next_index][coord_index])
        min_pos = min_coord + grid_size
        max_pos = max_coord - grid_size
        if min_pos > max_pos:
            return False
        can_split_double = min_pos < max_pos
        if not can_split_double:
            return False
        split_double = True
        if split_double:
            split_coord_1 = util.get_random_grid(min_pos, max_pos, grid_size)
            split_coord_2 = split_coord_1
            while split_coord_2 == split_coord_1:
                split_coord_2 = util.get_random_grid(min_pos, max_pos, grid_size)
            self.split_wall_double(start_index, split_coord_1, split_coord_2, building)
            return 2
        else:
            split_coord = util.get_random_grid(min_pos, max_pos, grid_size)
            self.split_wall(start_index, split_coord, building)
            return 1
    
    def random_transform_wall(self, max_shift_distance, split_prob, push_prob, snap_prob, building):
        wall_index = random.randrange(len(self.points))
        grid_size = building.grid_size
        split_wall = False
        pushed = False
        if random.uniform(0.0, 1.0) < snap_prob:
            snap_index = random.randrange(len(self.points))
            # Snap the wall
            pushed = pushed or self.snap_wall_random(snap_index, building)
        else:
            if random.uniform(0.0, 1.0) < split_prob:
                # Split the wall
                split = self.split_wall_random(wall_index, grid_size, building)
                if split == 1 and random.uniform(0.0, 1.0) < 0.5:
                    wall_index = wall_index + 2
                if split == 2:
                    wall_index = wall_index + 2
                split_wall = True
            if random.uniform(0.0, 1.0) < push_prob:
                # Push the wall
                is_push = random.uniform(0, 1) < 0.5
                shift_distance = (util.get_random_grid(-max_shift_distance, -grid_size, grid_size) if is_push 
                                else util.get_random_grid(grid_size, max_shift_distance, grid_size))
                pushed = pushed or self.push_wall(wall_index, shift_distance, building)
        if split_wall and not pushed:
            self.merge_unnecessary_walls(building)
    
    def get_center(self):
        area = self.get_area()
        sum_x = 0.0
        sum_y = 0.0
        for i in range(0, len(self.points)):
            j = (i + 1) % len(self.points)
            sum_x += (self.points[i][0] + self.points[j][0]) * (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1])
            sum_y += (self.points[i][1] + self.points[j][1]) * (self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1])
        return (sum_x / (6 * area), sum_y / (6 * area))

    def serialize(self):
        return {"points": copy.deepcopy(self.points), "center": self.get_center() }
