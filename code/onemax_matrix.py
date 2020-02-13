import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


def init_matrix(icls, shape):
    return icls(numpy.random.randint(0, 2, shape))

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", init_matrix, creator.Individual, shape=(10,10))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalOneMax(individual):
    return sum(sum(individual)),


def mutate_matrix(individual, indpb):
    # Since individual is a 2x2 matrix, iterate through rows and apply the mutFlipBit function
    for i in range(len(individual)):
        individual[i], = tools.mutFlipBit(individual[i], indpb)
    return individual,


def crossover_matrix(ind1_mat, ind2_mat, shape):
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
    
    
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", crossover_matrix, shape=(10, 10))
toolbox.register("mutate", mutate_matrix, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    
    pop = toolbox.population(n=300)
    
    # Numpy equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # numpy.array_equal or numpy.allclose solve this issue.
    hof = tools.HallOfFame(1, similar=numpy.array_equal)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=stats,
                        halloffame=hof)

    return pop, stats, hof

if __name__ == "__main__":
    main()