import numpy as np

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


    def get_roomtype_multiplication(self, room_type_mat):
        total_sum = 0
        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat[i])):
                room_type_1 = self.room_types[i]
                room_type_2 = self.room_types[j]

                total_sum += self.adj_mat[i][j] * room_type_mat[min(room_type_1, room_type_2)][max(room_type_1, room_type_2)]
        return total_sum

    def get_valence_violation(self, valence_lims):
        valences = {i: 0 for i in range(len(valence_lims))}
        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat[i])):
                if self.adj_mat[i][j]:
                    valences[self.room_types[i]] += 1
                    valences[self.room_types[j]] += 1
        
        return sum(max(valences[i] - valence_lims[i][1], valence_lims[i][0] - valences[i], 0) for i in range(len(valence_lims)))

    def get_num_room_types_violation(self, max_num_room_types, rooms):
        num_room_types = {i: 0 for i in range(len(rooms))}
        for room_type in self.room_types:
            num_room_types[room_type] += 1
        return sum(max(num_room_types[i] - max_num_room_types[i], 0) for i in range(len(rooms)))

    """
    def get_adj_value(self, permuted_self.adj_mat, room_id_1, room_id_2):
        # Note: might return a value from the lower-left zero diagonal area
        index_1 = self.order.index(room_id_1)
        index_2 = self.order.index(room_id_2)
        return permuted_self.adj_mat[min(index_1, index_2)][max(index_1, index_2)]
    """

    def get_sum(self):
        return int(round(sum(sum(self.adj_mat))))