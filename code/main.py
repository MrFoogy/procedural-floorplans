import random
import numpy
import graph_drawing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import ga
from room import Room
from individual_meta import IndividualMeta

rooms = []
rooms.append(Room("Exterior", 0))
rooms.append(Room("Entrance", 1))
rooms.append(Room("Corridor", 2))
rooms.append(Room("Kitchen", 3))
rooms.append(Room("Bedroom", 4))
rooms.append(Room("Toilet", 5))
adj_pref = numpy.ndarray(shape=(6,6), buffer=numpy.array([
     0,  3, -1.0,  1,  1,  1,
     0,  0,  2, -2.0, -3.0, -3.0,
     0,  0,  0,  2,  2,  1,
     0,  0,  0,  0, -2.0, -2.0, 
     0,  0,  0,  0,  0,  1,
     0,  0,  0,  0,  0,  0
]
))

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax, meta=None)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", ga.init_individual, creator.Individual, meta=IndividualMeta(list(range(len(rooms))) + [5, 5, 5]))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
toolbox.register("evaluate", ga.get_fitness, adj_pref=adj_pref)
toolbox.register("mate", ga.get_crossover, rooms=rooms)
toolbox.register("mutate", ga.get_mutation, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def individual_to_str(ind):
    return str(ind)


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

    print("Best: \n", individual_to_str(hof[0]))

    graph_drawing.visualize(rooms, hof[0])

    return pop, stats, hof

if __name__ == "__main__":
    main()