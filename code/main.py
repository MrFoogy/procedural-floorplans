import random
import numpy
import graph_drawing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import ga
from room import Room
from individual import Individual

rooms = []
rooms.append(Room("Exterior", 0, 10, 1))
rooms.append(Room("Entrance", 1, 2, 2))
rooms.append(Room("Corridor", 2, 4, 10))
rooms.append(Room("Kitchen", 3, 2, 2))
rooms.append(Room("Bedroom", 4, 2, 10))
rooms.append(Room("Toilet", 5, 1, 10))
adj_pref = numpy.ndarray(shape=(6,6), buffer=numpy.array([
     0,  3, -1.0,  -1.0,  -1.0,  -1.0,
     0,  0,  2, -2.0, -3.0, -3.0,
     0,  0,  0,  2,  2,  1,
     0,  0,  0,  0, -2.0, -2.0, 
     0,  0,  0,  0,  0,  1,
     0,  0,  0,  0,  0,  0
]
))

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", Individual, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", ga.init_individual, creator.Individual, room_types=list(range(len(rooms))))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
toolbox.register("evaluate", ga.get_fitness, adj_pref=adj_pref, pref_rooms=8, rooms=rooms,
                 max_valences = [room.max_valence for room in rooms],
                 max_rooms = [room.max_num for room in rooms])
toolbox.register("mate", ga.get_crossover, rooms=rooms)
toolbox.register("mutate", ga.get_mutation, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def individual_to_str(ind):
    return str(ind)


def main():
    
    pop = toolbox.population(n=500)
    
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