import random
import graph_util
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def init_individual(icls, meta):
    shape = (len(meta.room_types), len(meta.room_types))
    ind = icls(numpy.random.randint(0, 1, shape))
    ind.meta = meta
    ind.meta.permute_order(ind)
    return ind


def get_fitness(individual, adj_pref):
    score = individual.meta.get_roomtype_multiplication(individual, adj_pref)
    return score, 
    """
    mult = numpy.multiply(individual, adj_pref)
    return sum(sum(mult)), 
    """
    #return sum(sum(individual)), 


def get_mutation(individual, indpb):
    # Since individual is a 2D matrix, iterate through rows and apply the mutFlipBit function
    for i in range(len(individual)):
        for j in range(len(individual[i])):
            # Use XOR operator to flip the bit if the conditions are met
            individual[i][j] = individual[i][j] ^ (i < j and numpy.random.uniform() < indpb)
    
    """
        individual[i], = tools.mutFlipBit(individual[i], indpb)
        for j in range(len(individual[i])):
            individual[i][j] = (i < j and individual[i][j])
    """
    return individual, 


def get_crossover(ind1, ind2, rooms):
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

    ind1.meta.permute_order(ind1)
    ind2.meta.permute_order(ind2)

    # Select cutoff points for both matrices
    cutoff1 = random.randint(1, len(ind1) - 1)
    cutoff2 = random.randint(1, len(ind2) - 1)

    graph_util.swap_lower_right(ind1, ind2, cutoff1, cutoff2)

    return ind1, ind2