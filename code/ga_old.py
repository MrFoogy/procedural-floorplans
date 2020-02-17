import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def init_individual(icls, rooms):
    shape = (len(rooms), len(rooms))
    ind = icls(numpy.random.randint(0, 1, shape))
    ind.row_ids = [room.ident for room in rooms]
    return ind


def get_fitness(individual, adj_pref):
    mult = numpy.multiply(individual, adj_pref)
    return sum(sum(mult)), 
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


def get_crossover(ind1_mat, ind2_mat, rooms):
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

    # Need to do some special things because the individuals are 2D matrices.
    # TODO: can probably optimize???
    shape = (len(rooms), len(rooms))

    ind1 = ind1_mat.flatten()
    ind2 = ind2_mat.flatten()
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
        = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()

    for i in range(shape[0]):
        ind1_mat[i] = ind1[i * shape[1]:(i+1)*shape[1]]
        ind2_mat[i] = ind2[i * shape[1]:(i+1)*shape[1]]
        
    return ind1_mat, ind2_mat