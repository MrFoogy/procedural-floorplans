import numpy as np
from topology import graph_util
import heapq

class Individual:
    def __init__(self, adj_mat, room_types):
        self.adj_mat = adj_mat
        self.room_types = room_types
    
    def permute_order(self, new_order=None):
        old_adj_mat = self.adj_mat.copy()

        # First row/col is exterior, and should not be permuted
        if not new_order:
            new_order = [0] + list(np.random.permutation(list(range(len(self.room_types)))[1:]))

        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat[i])):
                # Skip lower left diagonal
                if i >= j:
                    continue

                old_i = new_order[i]
                old_j = new_order[j]
                old_coords = [old_i, old_j] if old_i < old_j else [old_j, old_i]
                self.adj_mat[i][j] = old_adj_mat[old_coords[0]][old_coords[1]] 
        
        # Update the room types order accordingly
        old_room_types = self.room_types.copy()
        self.room_types = [old_room_types[index] for index in new_order]


    def get_building_size(self):
        return len(self.room_types)

    def get_adjacency_score(self, config):
        return self.get_roomtype_mult(self.adj_mat, config.adj_pref)
    
    def get_distance_score(self, config):
        sum = 0
        distances_mat = self.get_all_pairs_distances()
        for i in range(len(distances_mat)):
            for j in range(len(distances_mat)):
                room_type_1 = self.room_types[i]
                room_type_2 = self.room_types[j]
                dist_pref_val = config.dist_pref[min(room_type_1, room_type_2)][max(room_type_1, room_type_2)]
                if dist_pref_val > 0:
                    # Max dist
                    sum += min(0, dist_pref_val - distances_mat[i][j])
                if dist_pref_val < 0:
                    # Min dist
                    sum += min(0, distances_mat[i][j] + dist_pref_val)

        return sum
    
    def get_roomtype_mult(self, base_mat, room_type_mat):
        total_sum = 0
        for i in range(len(self.room_types)):
            for j in range(len(self.room_types)):
                if i >= j:
                    continue
                room_type_1 = self.room_types[i]
                room_type_2 = self.room_types[j]
                total_sum += base_mat[i][j] * room_type_mat[min(room_type_1, room_type_2)][max(room_type_1, room_type_2)]
        return total_sum

    def get_utility_score(self, config):
        target_utilities = config.target_utilities
        rooms_def = config.rooms
        current_utilities = { type : 0.0 for type in target_utilities }
        for room_type in self.room_types:
            for utility_type in rooms_def[room_type].utilities:
                current_utilities[utility_type] += rooms_def[room_type].utilities[utility_type]
        score = 0.0
        for utility_type in current_utilities:
            score += min(target_utilities[utility_type], current_utilities[utility_type])
        return score

    def get_num_rooms_penalty(self, config):
        return abs(len(self.room_types) - 1 - config.pref_rooms)       

    def get_valence_violation(self, config):
        valence_lims = config.get_max_valences()
        valences = [0 for i in range(len(self.room_types))]
        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat[i])):
                if self.adj_mat[i][j]:
                    valences[i] += 1
                    valences[j] += 1
        
        return sum(max(valences[i] - valence_lims[self.room_types[i]][1], valence_lims[self.room_types[i]][0] - valences[i], 0) for i in range(len(self.room_types)))

    def get_num_room_types_violation(self, config):
        max_num_room_types = config.get_max_rooms()
        rooms = config.rooms
        num_room_types = {i: 0 for i in range(len(rooms))}
        for room_type in self.room_types:
            num_room_types[room_type] += 1
        return sum(max(num_room_types[i] - max_num_room_types[i], 0) for i in range(len(rooms)))


    def get_disconnect_violation(self):
        subtrees = graph_util.get_spanning_subtrees(self.adj_mat)
        return len(subtrees)


    def get_all_pairs_distances(self):
        # All pairs shortest distances
        res = np.full((len(self.adj_mat), len(self.adj_mat)), np.inf) 

        # First find adjacency lists
        connections_dict = {}
        for i in range(len(self.adj_mat)):
            connections_dict[i] = []
        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat)):
                if self.adj_mat[i][j] > 0:
                    connections_dict[i].append(j)
                    connections_dict[j].append(i)

        # Dijkstra's algorithm for evey node
        for i in range(len(self.adj_mat)):
            pq = [(0, i)]
            res[i][i] = 0
            while len(pq) > 0:
                current_distance, current_vertex = heapq.heappop(pq)
                if current_distance > res[i][current_vertex]:
                    continue

                for neighbor in connections_dict[current_vertex]:
                    distance = current_distance + 1

                    if distance < res[i][neighbor]:
                        res[i][neighbor] = distance
                        heapq.heappush(pq, (distance, neighbor))
            
            for j in range(len(self.adj_mat)):
                if res[i][j] == np.inf:
                    res[i][j] = 0.0
        
        return res


    """
    def get_adj_value(self, permuted_self.adj_mat, room_id_1, room_id_2):
        # Note: might return a value from the lower-left zero diagonal area
        index_1 = self.order.index(room_id_1)
        index_2 = self.order.index(room_id_2)
        return permuted_self.adj_mat[min(index_1, index_2)][max(index_1, index_2)]
    """

    def get_sum(self):
        return int(round(sum(sum(self.adj_mat))))