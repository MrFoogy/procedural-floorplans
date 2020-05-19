import random
import graph_util
import numpy
import mutation

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def init_individual(icls, config):
    # + 1 to add exterior
    num_rooms = max(2, int(round(random.gauss(config.pref_rooms, 0.7))))
    room_types = [0] + [random.randint(1, len(config.rooms) - 1) for i in range(num_rooms)]
    shape = (len(room_types), len(room_types))
    ind = icls(numpy.zeros(shape), room_types)
    ind.permute_order()
    spanning_tree = graph_util.get_spanning_tree(ind.adj_mat)
    graph_util.fill_connections_randomly(ind.adj_mat, spanning_tree)
    return ind


def get_fitness(individual, config, should_print=False):
    num_rooms_penalty = 3.0 * individual.get_num_rooms_penalty(config)
    if (should_print):
        print("Num rooms penalty: " + str(num_rooms_penalty))
    valence_penalty = 2.0 * individual.get_valence_violation(config)
    if (should_print):
        print("Valence penalty: " + str(valence_penalty))
    num_room_types_penalty = 1.0 * individual.get_num_room_types_violation(config)
    adjacency_score = individual.get_adjacency_score(config)
    if (should_print):
        print("Adjacency score: " + str(adjacency_score))
    utility_score = 5 * individual.get_utility_score(config)
    if (should_print):
        print("Utility score: " + str(utility_score))
    score = (adjacency_score + utility_score) / 2 ** (
        num_rooms_penalty + valence_penalty + num_room_types_penalty)
    return score, 


def print_fitness(individual, config):
    print("Total fitness: " + str(get_fitness(individual, config, True)))


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
    probabilities = [0.4, 0.6, 0.4, 0.2]
    mutation_type = random.uniform(0, sum(probabilities))
    if mutation_type <= sum(probabilities[:1]):
        mutation.number_of_node_mutation(individual, config)
    elif mutation_type <= sum(probabilities[:2]):
        mutation.number_of_edge_mutation(individual)
    elif mutation_type <= sum(probabilities[:3]):
        mutation.node_label_mutation(individual, config)
    elif mutation_type <= sum(probabilities[:4]):
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
    spanning_tree_2 = graph_util.get_spanning_tree(ind_2.adj_mat)

    # Fill connections
    graph_util.fill_connections_randomly(ind_1.adj_mat, spanning_tree_1)
    graph_util.fill_connections_randomly(ind_2.adj_mat, spanning_tree_2)

    return ind_1, ind_2
