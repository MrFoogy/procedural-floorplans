import numpy as np
import random
import graph_util

def number_of_node_mutation(individual, building_config, is_extend = None):
    individual.permute_order()
    if is_extend is None:
        is_extend = bool(random.getrandbits(1))
    if (not is_extend) and len(individual.adj_mat) > 1:
        # Reduce
        new_mat = individual.adj_mat[:-1,:-1].copy()
        individual.adj_mat = new_mat
        del individual.room_types[-1]
    else:
        # Extend
        new_mat = np.zeros((len(individual.adj_mat) + 1, len(individual.adj_mat) + 1))
        new_mat[:-1,:-1] = individual.adj_mat.copy()
        new_room_type = random.randint(0, len(building_config.rooms) - 1)
        individual.room_types.append(new_room_type) 
        num_new_connections = random.randint(building_config.rooms[new_room_type].max_valence[0], 
                                             building_config.rooms[new_room_type].max_valence[1])
        for i in range(num_new_connections):
            new_mat[i][-1] = 1

        individual.adj_mat = new_mat
            

def number_of_edge_mutation(individual, is_add = None):
    if is_add is None:
        is_add = bool(random.getrandbits(1))
    max_ones = (len(individual.adj_mat) * (len(individual.adj_mat) - 1)) // 2
    current_sum = individual.get_sum()

    if is_add and current_sum < max_ones:
        num_zeroes = max_ones - current_sum
        change_index = random.randint(0, num_zeroes - 1)
    else:
        num_ones = current_sum
        change_index = random.randint(0, num_ones - 1)
    count = 0
    for i in range(len(individual.adj_mat)):
        for j in range(len(individual.adj_mat)):
            if i >= j:
                continue
            if individual.adj_mat[i][j] != is_add:
                if count == change_index:
                    """
                    if individual.adj_mat[i][j] > 0.5:
                        individual.adj_mat[i][j] = 0
                    else:
                        individual.adj_mat[i][j] = 1
                        """
                    individual.adj_mat[i][j] = 1.0 - individual.adj_mat[i][j]
                    return
                count += 1


def node_label_mutation(individual, config):
    # blabla
    swap_position = random.randint(1, len(individual.room_types) - 1)


def swap_node_mutation(individual):


