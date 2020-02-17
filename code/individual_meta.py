import numpy as np

class IndividualMeta:
    def __init__(self, rooms, order):
        self.rooms = rooms
        self.order = order
    
    def permute_order(self, data, new_order=None):
        old_data = data.copy()
        old_order = self.order.copy()

        if new_order:
            self.order = new_order
        else:
            self.order = list(np.random.permutation(self.order))

        # TODO: Optimize!!
        old_order_map = { room_id: index for index, room_id in enumerate(old_order) }
        for i in range(len(self.order)):
            for j in range(len(self.order)):
                # Skip lower left diagonal
                if i >= j:
                    continue

                old_i = old_order_map[self.order[i]]
                old_j = old_order_map[self.order[j]]
                old_coords = [old_i, old_j] if old_i < old_j else [old_j, old_i]
                data[i][j] = old_data[old_coords[0]][old_coords[1]] 

    def get_permuted_multiplication(self, permuted_data, mat):
        total_sum = 0
        for room_id_1 in self.order:
            for room_id_2 in self.order:
                total_sum += mat[room_id_1][room_id_2] * self.get_adj_value(permuted_data, room_id_1, room_id_2)
        return total_sum


    def get_adj_value(self, permuted_data, room_id_1, room_id_2):
        # Note: might return a value from the lower-left zero diagonal area
        index_1 = self.order.index(room_id_1)
        index_2 = self.order.index(room_id_2)
        return permuted_data[min(index_1, index_2)][max(index_1, index_2)]