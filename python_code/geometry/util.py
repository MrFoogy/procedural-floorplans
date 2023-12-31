import random
import math

def get_random_grid(min, max, grid_size):
    val = random.uniform(min, max)
    lower = gridify_down(val, grid_size)
    upper = gridify_up(val, grid_size)
    if (val - lower) < (upper - val) or upper > max:
        return lower
    else:
        return upper

def gridify_up(val, grid_size):
    return math.ceil(val / grid_size) * grid_size

def gridify_down(val, grid_size):
    return math.floor(val / grid_size) * grid_size

def gridify_nearest(val, grid_size):
    return round(val / grid_size) * grid_size

def is_wall_overlapping(start_1, end_1, start_2, end_2):
    return is_wall_overlapping_length(start_1, end_1, start_2, end_2, 0.0)

def is_wall_overlapping_length(start_1, end_1, start_2, end_2, required_length):
    return min(end_1 - start_2, end_2 - start_1) > required_length

def is_wall_touching(start_1, end_1, start_2, end_2):
    return min(end_1 - start_2, end_2 - start_1) >= 0