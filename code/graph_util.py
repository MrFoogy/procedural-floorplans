import random
import numpy as np

def get_subgraphs(individual):
    # First find subgraphs
    subgraphs_map = { index : [index] for index in range(len(individual)) }
    subgraphs = list(subgraphs_map.values())

    # Loop through the adjacency matrix to connect the subgraphs
    for i in range(len(individual)):
        for j in range(len(individual[i])):
            if individual[i][j]:
                # If not already in same subgraph
                if subgraphs_map[i] is not subgraphs_map[j]:
                    merged = subgraphs_map[i] + subgraphs_map[j]
                    subgraphs.remove(subgraphs_map[i])
                    subgraphs.remove(subgraphs_map[j])
                    subgraphs.append(merged)
                    subgraphs_map[i] = merged
                    subgraphs_map[j] = merged
    
    return subgraphs


def get_spanning_subtrees(matrix):
    # Basically a breadth-first search from every node to find all individual subtrees
    visited = set()
    connected = set()
    subtrees = []
    start_node = 0
    for start_node in range(len(matrix)):
        if start_node in visited:
            continue
        frontier = [start_node]
        current_tree = {}
        connected.add(start_node)
        while len(frontier) > 0:
            current = frontier.pop()
            current_tree[current] = []
            if current in visited:
                continue
            visited.add(current)
            for candidate in range(len(matrix)):
                if (matrix[current][candidate] > 0 or matrix[candidate][current] > 0) and candidate not in connected:
                    frontier.append(candidate)
                    connected.add(candidate)
                    current_tree[current].append(candidate)
        subtrees.append(current_tree)
    return subtrees


def get_spanning_tree(matrix):
    # TODO: unit test?
    trees = get_spanning_subtrees(matrix)
    # Connect the subtrees
    while len(trees) > 1:
        # Combine the first two trees
        connect_1 = random.choice(list(trees[0].keys()))
        connect_2 = random.choice(list(trees[1].keys()))
        trees[0].update(trees[1]) 
        trees[0][connect_1].append(connect_2)
        del trees[1]

    return trees[0]


def swap_lower_right(mat_1, mat_2, cutoff_1, cutoff_2):
    swap_mat_1 = mat_1[cutoff_1:, cutoff_1:].copy()
    swap_mat_2 = mat_2[cutoff_2:, cutoff_2:].copy()

    keep_mat_1 = mat_1[:cutoff_1, :cutoff_1].copy()
    keep_mat_2 = mat_2[:cutoff_2:, :cutoff_2].copy()

    new_size_1 = cutoff_1 + len(mat_2) - cutoff_2
    new_size_2 = cutoff_2 + len(mat_1) - cutoff_1

    new_mat_1 = np.zeros((new_size_1, new_size_1))
    new_mat_2 = np.zeros((new_size_2, new_size_2))

    new_mat_1[:cutoff_1,:cutoff_1] = keep_mat_1
    new_mat_2[:cutoff_2,:cutoff_2] = keep_mat_2

    new_mat_1[cutoff_1:, cutoff_1:] = swap_mat_2
    new_mat_2[cutoff_2:, cutoff_2:] = swap_mat_1

    return new_mat_1, new_mat_2


def set_num_connections(mat, spanning_tree, target_num_connections):
    # Make sure the spanning tree is included in the matrix
    for node_1 in spanning_tree:
        for node_2 in spanning_tree[node_1]:
            mat[min(node_1, node_2)][max(node_1, node_2)] = 1

    num_connections = sum(sum(mat))
    if num_connections < target_num_connections:
        add_candidates = []
        for i in range(len(mat)):
            for j in range(len(mat)):
                if i >= j:
                    continue
                if mat[i][j] == 0:
                    add_candidates.append((i, j))
        random.shuffle(add_candidates)
        for pair in add_candidates[:target_num_connections - num_connections]:
            mat[pair[0]][pair[1]] = 1

    elif num_connections > target_num_connections:
        remove_candidates = []
        for i in range(len(mat)):
            for j in range(len(mat)):
                if i >= j:
                    continue
                if mat[i][j] == 1 and (j not in spanning_tree[i]) and (i not in spanning_tree[j]):
                    remove_candidates.append((i, j))
        random.shuffle(remove_candidates)
        for pair in remove_candidates[:num_connections - target_num_connections]:
            mat[pair[0]][pair[1]] = 0
