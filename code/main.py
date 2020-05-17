import random
import numpy as np
import graph_drawing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import ga
from room import Room
from individual import Individual
from building_config import BuildingConfig

rooms = []
rooms.append(Room("Exterior", 0, (1, 4), 10, {}))
rooms.append(Room("Entrance", 1, (2, 3), 2, {}))
rooms.append(Room("Corridor", 2, (2, 4), 10, {}))
rooms.append(Room("Kitchen", 3, (1, 2), 2, {"cooking": 1.0, "eating": 1.0}))
rooms.append(Room("Bedroom", 4, (1, 1), 10, {"sleeping": 1.0}))
rooms.append(Room("Toilet", 5, (1, 1), 10, {"wc": 1.0}))
rooms.append(Room("Bathroom", 6, (1, 1), 10, {"shower": 1.0, "wc": 1.0}))
rooms.append(Room("Living room", 7, (1, 2), 10, {"gathering": 1.0, "leisure": 1.0}))
rooms.append(Room("Dining room", 8, (1, 2), 10, {"gathering": 1.0, "eating": 1.0}))
target_utilities = {"cooking": 1.0, "sleeping": 2.0, "wc": 2.0, "shower": 1.0, "leisure": 1.0, "gathering": 1.0, "eating": 1.0}
adj_pref = np.ndarray(shape=(9,9), buffer=np.array([
     0.0,  3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, # Exterior
     0.0, -2.0,  2.0, -2.0, -3.0, -3.0, -3.0,  1.0,  1.0, # Entrance
     0.0,  0.0,  0.0,  2.0,  2.0,  1.0,  2.0,  2.0,  2.0, # Corridor
     0.0,  0.0,  0.0, -2.0, -2.0, -2.0, -2.0,  1.0,  2.0, # Kitchen
     0.0,  0.0,  0.0,  0.0, -1.0,  1.0,  1.0,  1.0, -2.0, # Bedroom
     0.0,  0.0,  0.0,  0.0,  0.0, -2.0,  1.0,  1.0, -1.0, # Toilet
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0,  1.0, -1.0, # Bathroom
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0,  1.0, # Living room
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0 # Dining room
]
))
rel_ratios = np.ndarray(shape=(9,9), buffer=np.array([
     0,  1,  1,  1,  1,  1,  1,  1,  1,
     0,  0,  1,  1,  1,  1,  1,  1,  1,
     0,  0,  0,  1,  1,  1,  1,  1,  1,
     0,  0,  0,  0,  1,  1,  1,  1,  1,
     0,  0,  0,  0,  0,  1,  1,  1,  1,
     0,  0,  0,  0,  0,  0,  1,  1,  1,
     0,  0,  0,  0,  0,  0,  0,  1,  1,
     0,  0,  0,  0,  0,  0,  0,  0,  1,
     0,  0,  0,  0,  0,  0,  0,  0,  0
]
), dtype=np.int32)

config = BuildingConfig(rooms, adj_pref, rel_ratios, 8, target_utilities)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", Individual, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", ga.init_individual, creator.Individual, config)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
toolbox.register("evaluate", ga.get_fitness, config=config)
toolbox.register("mate", ga.get_crossover)
toolbox.register("mutate", ga.get_mutation, indpb=0.8, config=config)
toolbox.register("select", tools.selNSGA2)


def individual_to_str(ind):
    return str(ind)


def main():
    population_size = 300
    num_results = 5
    pop = toolbox.population(n=population_size)
    
    # Numpy equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # np.array_equal or np.allclose solve this issue.
    hof = tools.HallOfFame(num_results, similar=np.array_equal)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_adj_score = tools.Statistics(lambda ind: ind.get_adjacency_score(config))
    stats_utility_score = tools.Statistics(lambda ind: ind.get_utility_score(config))
    stats_valence_pen = tools.Statistics(lambda ind: ind.get_valence_violation(config))
    stats_num_rooms_pen = tools.Statistics(lambda ind: ind.get_num_rooms_penalty(config))
    mstats = tools.MultiStatistics(fitness=stats_fit, adj_score=stats_adj_score, utility_score=stats_utility_score, valence_pen=stats_valence_pen, num_rooms_pen=stats_num_rooms_pen)
    mstats.register("avg", np.mean)
    """
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)
    """
    
    algorithms.eaMuPlusLambda(pop, toolbox, population_size, population_size, cxpb=0.5, mutpb=0.5, ngen=100, stats=mstats,
                        halloffame=hof)
    """
    algorithms.eaSimple(pop, toolbox, cxpb=0.3, mutpb=0.8, ngen=60, stats=stats,
                        halloffame=hof)
    """
    best = hof[0]

    print("Best: \n", individual_to_str(best))
    ga.print_fitness(best, config)

    for i in range(num_results):
        graph_drawing.visualize(rooms, hof[i])

    return pop, mstats, hof

if __name__ == "__main__":
    main()