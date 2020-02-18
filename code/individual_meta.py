import numpy as np

class IndividualMeta:
    def __init__(self, room_types):
        self.room_types = room_types
    
    def permute_order(self, data, new_order=None):
        old_data = data.copy()

        if not new_order:
            new_order = list(np.random.permutation(list(range(len(self.room_types)))))

        for i in range(len(data)):
            for j in range(len(data[i])):
                # Skip lower left diagonal
                if i >= j:
                    continue

                old_i = new_order[i]
                old_j = new_order[j]
                old_coords = [old_i, old_j] if old_i < old_j else [old_j, old_i]
                data[i][j] = old_data[old_coords[0]][old_coords[1]] 
        
        # Update the room types order accordingly
        old_room_types = self.room_types.copy()
        self.room_types = [old_room_types[index] for index in new_order]


    def get_roomtype_multiplication(self, data, room_type_mat):
        total_sum = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                room_type_1 = self.room_types[i]
                room_type_2 = self.room_types[j]

                total_sum += data[i][j] * room_type_mat[min(room_type_1, room_type_2)][max(room_type_1, room_type_2)]
        return total_sum


    """
    def get_adj_value(self, permuted_data, room_id_1, room_id_2):
        # Note: might return a value from the lower-left zero diagonal area
        index_1 = self.order.index(room_id_1)
        index_2 = self.order.index(room_id_2)
        return permuted_data[min(index_1, index_2)][max(index_1, index_2)]
    """