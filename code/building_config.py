class BuildingConfig:
    def __init__(self, rooms, adj_pref, rel_ratios, pref_rooms, target_utilities):
        self.rooms = rooms
        self.adj_pref = adj_pref
        self.rel_ratios = rel_ratios
        self.pref_rooms = pref_rooms
        self.target_utilities = target_utilities

    def get_max_valences(self):
        return [room.max_valence for room in self.rooms]
         
    def get_max_rooms(self):
        return [room.max_num for room in self.rooms]