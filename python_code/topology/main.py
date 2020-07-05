import random
import numpy as np
import json

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from topology import graph_drawing
from topology import ga
from topology import data_format
from topology.room import Room
from topology.individual import Individual
from topology.building_config import BuildingConfig

rooms = []
rooms.append(Room("Exterior", 0, (1, 4), 10, {}))
rooms.append(Room("Entrance", 1, (2, 3), 2, {}))
rooms.append(Room("Corridor", 2, (2, 4), 10, {}))
rooms.append(Room("Kitchen", 3, (1, 2), 2, {"cooking": 1.0, "eating": 1.0}))
rooms.append(Room("Bedroom", 4, (1, 1), 10, {"sleeping": 1.0}))
rooms.append(Room("Toilet", 5, (1, 1), 10, {"wc": 1.0}))
rooms.append(Room("Bathroom", 6, (1, 1), 10, {"shower": 1.0, "wc": 1.0}))
rooms.append(Room("Living room", 7, (1, 3), 10, {"gathering": 1.0, "leisure": 1.0}))
rooms.append(Room("Dining room", 8, (1, 3), 10, {"gathering": 1.0, "eating": 1.0}))
target_utilities = {"cooking": 1.0, "sleeping": 2.0, "wc": 2.0, "shower": 1.0, "leisure": 1.0, "gathering": 1.0, "eating": 1.0}
adj_pref = np.ndarray(shape=(9,9), buffer=np.array([
     0.0,  5.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, # Exterior
     0.0, -2.0,  2.0, -2.0, -3.0, -3.0, -3.0,  1.0,  1.0, # Entrance
     0.0,  0.0, -2.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, # Corridor
     0.0,  0.0,  0.0, -2.0, -2.0, -2.0, -2.0,  1.0,  2.0, # Kitchen
     0.0,  0.0,  0.0,  0.0, -1.0,  1.0,  1.0,  1.0, -2.0, # Bedroom
     0.0,  0.0,  0.0,  0.0,  0.0, -2.0,  1.0,  1.0, -1.0, # Toilet
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0,  1.0, -1.0, # Bathroom
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0,  1.0, # Living room
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0 # Dining room
]
))
dist_pref = np.ndarray(shape=(9,9), buffer=np.array([
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, # Exterior
     0.0, -3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0, # Entrance
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, # Corridor
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  2.0, # Kitchen
     0.0,  0.0,  0.0,  0.0,  3.0,  2.0,  2.0,  0.0,  0.0, # Bedroom
     0.0,  0.0,  0.0,  0.0,  0.0, -3.0, -3.0,  0.0,  0.0, # Toilet
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -3.0,  0.0,  0.0, # Bathroom
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, # Living room
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0 # Dining room
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

model_room_types = [0, 1, 2, 3, 7, 5, 2, 4, 4, 6]
model_adj_mat = np.ndarray(shape=(10,10), buffer=np.array(
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 1, 0, 1, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
model_ind = Individual(model_adj_mat, model_room_types)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", Individual, fitness=creator.FitnessMax)



def individual_to_str(ind):
    return str(ind)


def run_ga(generations, population_size, building_size, hof_size, produce_output):
    config = BuildingConfig(rooms, adj_pref, dist_pref, building_size, target_utilities)

    toolbox = base.Toolbox()

    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", ga.init_individual, creator.Individual, config)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        
    toolbox.register("evaluate", ga.get_fitness, config=config)
    toolbox.register("mate", ga.get_crossover)
    toolbox.register("mutate", ga.get_mutation, indpb=0.8, config=config)
    toolbox.register("select", tools.selNSGA2)

    pop = toolbox.population(n=population_size)
    
    # Numpy equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # np.array_equal or np.allclose solve this issue.
    hof = tools.HallOfFame(hof_size, similar=np.array_equal)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_adj_score = tools.Statistics(lambda ind: ind.get_adjacency_score(config))
    stats_dist_score = tools.Statistics(lambda ind: ind.get_distance_score(config))
    stats_utility_score = tools.Statistics(lambda ind: ind.get_utility_score(config))
    stats_valency_pen = tools.Statistics(lambda ind: ind.get_valence_violation(config))
    stats_num_rooms_pen = tools.Statistics(lambda ind: ind.get_num_rooms_penalty(config))
    stats_types = ["fitness", "adj_score", "distance_score", "utility_score", "valency_pen", "num_rooms_pen"]
    mstats = tools.MultiStatistics(fitness=stats_fit, adj_score=stats_adj_score, dist_score=stats_dist_score, utility_score=stats_utility_score, 
        valency_pen=stats_valency_pen, num_rooms_pen=stats_num_rooms_pen)
    mstats.register("avg", np.mean)
    """
    mstats.register("std", np.std)
    """
    mstats.register("min", np.min)
    mstats.register("max", np.max)
    
    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, population_size, population_size, cxpb=0.5, mutpb=0.5, ngen=generations, stats=mstats,
                        halloffame=hof)
    """
    algorithms.eaSimple(pop, toolbox, cxpb=0.3, mutpb=0.8, ngen=60, stats=stats,
                        halloffame=hof)
    """


    #return pop, mstats, hof
    return data_format.format_full_output(logbook.chapters, hof, model_ind, config)

if __name__ == "__main__":
    run_ga(10, 300, 8, 10, False)