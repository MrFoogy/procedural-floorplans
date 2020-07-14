import random
import geometry.util as util

class Building:
    def __init__(self, rooms, lot_shape, grid_size, walls_horizontal, walls_vertical):
        self.rooms = rooms
        self.lot_shape = lot_shape
        self.grid_size = grid_size
        self.walls_horizontal = walls_horizontal
        self.walls_vertical = walls_vertical
    
    def serialize(self):
        return {"rooms": [room.serialize() for room in self.rooms], "lot": self.lot_shape.serialize(), 
                "gridSize": self.grid_size}

    def print_wall_lists(self):
        print("Horizontal: ", self.walls_horizontal.walls, flush=True)
        print("Vertical: ", self.walls_vertical.walls, flush=True)
    
    def get_wall_set(self, is_horizontal):
        return self.walls_horizontal if is_horizontal else self.walls_vertical


class BuildingRoom:
    def __init__(self, room, shape, room_id):
        self.room = room
        self.shape = shape
        self.room_id = room_id
    
    def serialize(self):
        return {"name": self.room.name, "shape": self.shape.serialize()}


class BuildingShape:
    def __init__(self, points, room_id):
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
        if self.points[start_index][0] == self.points[next_index][0] and self.points[start_index][1] == self.points[next_index][1]:
            return not self.is_wall_horizontal(next_index)
        return (abs(self.points[start_index][0] - self.points[next_index][0]) > 
                abs(self.points[start_index][1] - self.points[next_index][1]))

    def get_walls_for_axis(self, get_horizontal):
        res = []
        for start_index in range(len(self.points)):
            next_index = (start_index + 1) % len(self.points)
            is_horizontal = self.is_wall_horizontal(start_index)
            if is_horizontal and get_horizontal:
                start_x = min(self.points[start_index][0], self.points[next_index][0])
                end_x = max(self.points[start_index][0], self.points[next_index][0])
                res.append([self.points[start_index][1], [start_x, end_x]])
            if (not is_horizontal) and (not get_horizontal):
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
        scanned_walls = wall_set.scan_walls(min(start_cross, start_cross + distance), 
                                            max(start_cross, start_cross + distance), 
                                            min(align_coord_1, align_coord_2), max(align_coord_1, align_coord_2))
                                        
        # If two walls from the same room overlap on the align axis, that room section would disappear
        # making such a push illegal
        for room_id in scanned_walls:
            if len(scanned_walls[room_id]) < 2:
                continue
            for i in range(len(scanned_walls[room_id])):
                for j in range(len(scanned_walls[room_id])):
                    if i == j:
                        continue
                    if util.is_wall_overlapping(scanned_walls[room_id][i][0], scanned_walls[room_id][i][1],
                                                scanned_walls[room_id][j][0], scanned_walls[room_id][j][1]):
                        return False
        return True
    
    def snap_wall(self, start_index, snap_index, building):
        is_horizontal = self.is_wall_horizontal(start_index)
        coord_index = 1 if is_horizontal else 0
        distance = self.points[snap_index][coord_index] - self.points[start_index][coord_index] 
        self.push_wall(start_index, distance, building)
    
    def snap_wall_random(self, start_index, building):
        snap_index = None
        if random.uniform(0, 1) < 0.5:
            snap_index = (start_index - 1) % len(self.points)
        else:
            snap_index = (start_index + 2) % len(self.points)
        self.snap_wall(start_index, snap_index, building)

    def push_wall(self, start_index, distance, building):
        if not self.can_push_wall(start_index, distance, building):
            return False
        
        # Remove from wall set, 3 walls are affected
        self.remove_from_wall_set(start_index - 1, building)
        self.remove_from_wall_set(start_index, building)
        self.remove_from_wall_set(start_index + 1, building)

        next_index = (start_index + 1) % len(self.points)
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
    
    def get_wall_info(self, start_index):
        next_index = (start_index + 1) % len(self.points)
        is_horizontal = self.is_wall_horizontal(start_index)
        if is_horizontal:
            y = self.points[start_index][1]
            start_x = min(self.points[start_index][0], self.points[next_index][0])
            end_x = max(self.points[start_index][0], self.points[next_index][0])
            return y, start_x, end_x, self.room_id
        else:
            x = self.points[start_index][0]
            start_y = min(self.points[start_index][1], self.points[next_index][1])
            end_y = max(self.points[start_index][1], self.points[next_index][1])
            return x, start_y, end_y, self.room_id
    
    def add_to_wall_set(self, index, building):
        index_mod = index % len(self.points)
        pos, start, end, room_id = self.get_wall_info(index_mod)
        building.get_wall_set(self.is_wall_horizontal(index_mod)).add_wall(pos, start, end, room_id)

    def remove_from_wall_set(self, index, building):
        index_mod = index % len(self.points)
        pos, start, end, room_id = self.get_wall_info(index_mod)
        building.get_wall_set(self.is_wall_horizontal(index_mod)).remove_wall(pos, start, end, room_id)

    def merge_walls(self, index_1, index_2, building):
        self.remove_from_wall_set(index_1, building)
        self.remove_from_wall_set(index_2, building)

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
        split_double = False
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
        if random.uniform(0.0, 1.0) < split_prob:
            # Split the wall
            split = self.split_wall_random(wall_index, grid_size, building)
            if split == 1 and random.uniform(0.0, 1.0) < 0.5:
                wall_index = wall_index + 2
            if split == 2:
                wall_index = wall_index + 2
        if random.uniform(0.0, 1.0) < push_prob:
            # Push the wall
            is_push = random.uniform(0, 1) < 0.5
            shift_distance = (util.get_random_grid(-max_shift_distance, -grid_size, grid_size) if is_push 
                            else util.get_random_grid(grid_size, max_shift_distance, grid_size))
            self.push_wall(wall_index, shift_distance, building)
        if random.uniform(0.0, 1.0) < snap_prob:
            # Snap the wall
            self.snap_wall_random(wall_index, building)
    
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
        return {"points": self.points, "center": self.get_center() }
