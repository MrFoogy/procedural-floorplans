import random
import graph_util
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def init_individual(icls, room_types):
    shape = (len(room_types), len(room_types))
    ind = icls(numpy.random.randint(0, 1, shape), room_types)
    ind.permute_order()
    return ind


def get_fitness(individual, adj_pref):
    score = individual.get_roomtype_multiplication(adj_pref)
    return score, 
    """
    mult = numpy.multiply(individual, adj_pref)
    return sum(sum(mult)), 
    """
    #return sum(sum(individual)), 


def get_mutation(individual, indpb):
    # Since individual is a 2D matrix, iterate through rows and apply the mutFlipBit function
    for i in range(len(individual.adj_mat)):
        for j in range(len(individual.adj_mat[i])):
            # Use XOR operator to flip the bit if the conditions are met
            individual.adj_mat[i][j] = int(individual.adj_mat[i][j]) ^ (i < j and numpy.random.uniform() < indpb)
    
    """
        individual[i], = tools.mutFlipBit(individual[i], indpb)
        for j in range(len(individual[i])):
            individual[i][j] = (i < j and individual[i][j])
    """
    return individual, 


def get_crossover(ind_1, ind_2, rooms):
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
    min_length_1 = len(ind_1.adj_mat) - 1
    max_length_1 = (len(ind_1.adj_mat) - 1) * (len(ind_1.adj_mat)) / 2

    spanning_tree_2 = graph_util.get_spanning_tree(ind_2.adj_mat)
    min_length_2 = len(ind_2.adj_mat) - 1
    max_length_2 = (len(ind_2.adj_mat) - 1) * (len(ind_2.adj_mat)) / 2

    # Determine final lengths
    final_length_1 = random.randint(min_length_1, max_length_1)
    final_length_2 = random.randint(min_length_2, max_length_2)

    graph_util.set_num_connections(ind_1.adj_mat, spanning_tree_1, final_length_1)
    graph_util.set_num_connections(ind_2.adj_mat, spanning_tree_2, final_length_2)

    return ind_1, ind_2