import random

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
    def __init__(self, points):
        self.points = points

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
    
    def push_wall(self, start_index, distance):
        next_index = (start_index + 1) % len(self.points)
        is_horizontal = abs(self.points[next_index][0] - self.points[start_index][0]) > abs(self.points[next_index][1] - self.points[start_index][1])
        if is_horizontal:
            self.points[start_index][1] += distance
            self.points[next_index][1] += distance
        else:
            self.points[start_index][0] += distance
            self.points[next_index][0] += distance

    def split_wall(self, start_index, prog_along_wall):
        next_index = (start_index + 1) % len(self.points)
        new_point_x = self.points[start_index][0] + (self.points[next_index][0] - self.points[start_index][0]) * prog_along_wall
        new_point_y = self.points[start_index][1] + (self.points[next_index][1] - self.points[start_index][1]) * prog_along_wall
        self.points.insert(start_index + 1, [new_point_x, new_point_y])
        self.points.insert(start_index + 1, [new_point_x, new_point_y])
    
    def random_transform_wall(self, max_shift_distance, split_prob):
        wall_index = random.randrange(len(self.points))
        if random.uniform(0.0, 1.0) < split_prob:
            # Split the wall
            self.split_wall(wall_index, random.uniform(0.1, 0.9))
            if random.uniform(0.0, 1.0) < 0.5:
                wall_index = wall_index + 2
        self.push_wall(wall_index, random.uniform(-max_shift_distance, max_shift_distance))
    
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