import numpy as np
import random

def number_of_node_mutation(individual, is_extend = None):
    if is_extend is None:
        is_extend = bool(random.getrandbits(1))
    if not is_extend and len(individual.adj_mat) > 1:
        new_mat = individual.adj_mat[:-1,:-1].copy()
        individual.adj_mat = new_mat
    else:
        new_mat = np.zeros((len(individual.adj_mat) + 1, len(individual.adj_mat) + 1))
        new_mat[:-1,:-1] = individual.adj_mat.copy()
        individual.adj_mat = new_mat
