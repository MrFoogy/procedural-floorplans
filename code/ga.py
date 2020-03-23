import random
import graph_util
import numpy
import mutation

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def init_individual(icls, config):
    room_types=list(range(len(config.rooms)))
    shape = (len(room_types), len(room_types))
    ind = icls(numpy.random.randint(0, 1, shape), room_types)
    ind.permute_order()
    return ind


def get_fitness(individual, max_valences, max_rooms, config, pref_rooms):
    num_rooms_penalty = abs(len(individual.room_types) - pref_rooms)
    valence_penalty = individual.get_valence_violation(max_valences)
    num_room_types_penalty = individual.get_num_room_types_violation(max_rooms, config.rooms)
    score = individual.get_roomtype_multiplication(config.adj_pref) / 2 ** (num_rooms_penalty + valence_penalty + num_room_types_penalty)
    return score, 
    """
    mult = numpy.multiply(individual, adj_pref)
    return sum(sum(mult)), 
    """
    #return sum(sum(individual)), 


def simple_flip_bit_mutation(individual, indpb):
    # Since individual is a 2D matrix, iterate through rows and apply the mutFlipBit function
    for i in range(len(individual.adj_mat)):
        for j in range(len(individual.adj_mat[i])):
            # Use XOR operator to flip the bit if the conditions are met
            individual.adj_mat[i][j] = int(individual.adj_mat[i][j]) ^ (i < j and numpy.random.uniform() < indpb)


def get_mutation(individual, config, indpb):
    """
    simple_flip_bit_mutation(individual, indpb)
    """
    mutation_type = random.randint(0,3)
    if mutation_type == 0:
        mutation.number_of_node_mutation(individual, config)
    if mutation_type == 1:
        mutation.number_of_edge_mutation(individual)
    if mutation_type == 2:
        mutation.node_label_mutation(individual, config)
    if mutation_type == 3:
        mutation.swap_node_mutation(individual)
    return individual, 


def get_crossover(ind_1, ind_2):
    """Execute a two points crossover with copy on the input individuals. The
    copy is required because the slicing in numpy returns a view of the data,
    which leads to a self overwritting in the swap operation. It prevents
    ::
    
        >>> import numpy
        >>> a = numpy.array((1,2,3,4))
        >>> b = numpy.array((5,6,7,8))
        >>> a[1:3], b[1:3] = b[1:3], a[1:3]
        >>> print(a)
        [1 6 7 4]
        >>> print(b)
        [5 6 7 8]
    """

    # Permute order of matrices
    ind_1.permute_order()
    ind_2.permute_order()

    # Select cutoff points for both matrices
    cutoff_1 = random.randint(1, len(ind_1.adj_mat) - 1)
    cutoff_2 = random.randint(1, len(ind_2.adj_mat) - 1)

    # Swap the room types
    swap_room_types_1 = ind_1.room_types[cutoff_1:]
    swap_room_types_2 = ind_2.room_types[cutoff_2:]
    ind_1.room_types = ind_1.room_types[:cutoff_1] + swap_room_types_2
    ind_2.room_types = ind_2.room_types[:cutoff_2] + swap_room_types_1

    # Swap lower rights 
    ind_1.adj_mat, ind_2.adj_mat = graph_util.swap_lower_right(ind_1.adj_mat, ind_2.adj_mat, cutoff_1, cutoff_2)

    # Find spanning trees
    spanning_tree_1 = graph_util.get_spanning_tree(ind_1.adj_mat)

    length = sum(len(spanning_tree_1[node_1]) for node_1 in spanning_tree_1)
    assert length == len(ind_1.adj_mat) - 2

    min_length_1 = len(ind_1.adj_mat) - 1
    max_length_1 = (len(ind_1.adj_mat) - 1) * (len(ind_1.adj_mat)) / 2

    spanning_tree_2 = graph_util.get_spanning_tree(ind_2.adj_mat)

    length = sum(len(spanning_tree_2[node_1]) for node_1 in spanning_tree_2)
    assert length == len(ind_2.adj_mat) - 2

    min_length_2 = len(ind_2.adj_mat) - 1
    max_length_2 = (len(ind_2.adj_mat) - 1) * (len(ind_2.adj_mat)) / 2

    # Determine final lengths
    final_length_1 = random.randint(min_length_1, max_length_1)
    final_length_2 = random.randint(min_length_2, max_length_2)

    graph_util.set_num_connections(ind_1.adj_mat, spanning_tree_1, final_length_1)
    graph_util.set_num_connections(ind_2.adj_mat, spanning_tree_2, final_length_2)

    return ind_1, ind_2