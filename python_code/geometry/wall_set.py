import geometry.util as util

class WallSet:
    def __init__(self):
        self.walls = []

    def add_wall(self, pos, start, end, room_id):
        place_index, exists = self.find_wall(pos)
        if not exists:
            self.walls.insert(place_index + 1, [pos, {}])
            place_index += 1
        if not room_id in self.walls[place_index][1]:
            self.walls[place_index][1][room_id] = []
        self.walls[place_index][1][room_id].append([start, end])
    
    def remove_wall(self, pos, start, end, room_id):
        place_index, exists = self.find_wall(pos)
        if not exists:
            print("Error: wall does not exist", flush=True)
        #print("Wall set before: ", self.walls, flush=True)
        for i in range(len(self.walls[place_index][1][room_id])):
            if self.walls[place_index][1][room_id][i][0] == start and self.walls[place_index][1][room_id][i][1] == end:
                del self.walls[place_index][1][room_id][i]
                break
        #print("Wall set after: ", self.walls, flush=True)

    def find_wall(self, pos):
        found_exact = False
        res_index = -1
        for i in range(len(self.walls)):
            if self.walls[i][0] > pos:
                break
            if self.walls[i][0] == pos:
                found_exact = True
                res_index = i
                break
            res_index = i
        return res_index, found_exact

    def scan_walls(self, cross_start, cross_end, align_start, align_end, filter_id=None):
        res = {}
        for i in range(len(self.walls)):
            if self.walls[i][0] >= cross_start and self.walls[i][0] <= cross_end:
                for room_id in self.walls[i][1]:
                    if filter_id != None and room_id != filter_id:
                        continue 
                    for wall_start, wall_end in self.walls[i][1][room_id]:
                        if util.is_wall_overlapping(wall_start, wall_end, align_start, align_end):
                            if room_id not in res:
                                res[room_id] = []
                            res[room_id].append([self.walls[i][0], [wall_start, wall_end]])
        return res