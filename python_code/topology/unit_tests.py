import unittest
import random
import numpy as np
from topology import graph_util
from topology import mutation
from topology.individual import Individual
from topology.room import Room
from topology.building_config import BuildingConfig

class TestGA(unittest.TestCase):
    def test_permutation(self):
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 0, 1, 0, 0, 1, 0, 0, 0]), dtype=np.int32)
        correct_permute_data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 1, 0, 0, 0]), dtype=np.int32)
        individual = Individual(data, [0, 1, 2])

        new_order = [0, 2, 1]
        individual.permute_order(new_order)

        self.assertTrue(np.array_equal(individual.adj_mat, correct_permute_data))
        self.assertEqual(individual.room_types, new_order)

        for i in range(10):
            mat = np.random.randint(0, 2, (5, 5))
            individual = Individual(mat, [0, 1, 2, 3, 4])
            individual.permute_order()
            self.assertEqual(individual.room_types[0], 0)

    def test_fitness_permutation(self):
        rooms = 6
        shape = (rooms, rooms)
        adjacencies = np.random.randint(0, 2, shape)
        preferences = np.random.randint(-3, 4, shape)
        config = BuildingConfig([], preferences, None, None, None)
        # Make sure is diagonal
        for i in range(rooms):
            for j in range(rooms):
                # Use XOR operator to flip the bit if the conditions are met
                adjacencies[i][j] = adjacencies[i][j] if i < j else 0
                preferences[i][j] = preferences[i][j] if i < j else 0
    

        individual = Individual(adjacencies, list(range(rooms)))
        original_fitness = individual.get_adjacency_score(config)
        for i in range(5):
            """
            print('Original adj\n', adjacencies)
            print('Original order\n', meta.room_types)
            """
            individual.permute_order()
            """
            print('Permuted adj\n', adjacencies)
            print('Permuted order\n', meta.room_types)
            print('Preferences\n', preferences)
            """
            permuted_fitness = individual.get_adjacency_score(config)
            self.assertEqual(original_fitness, permuted_fitness)


class TestGraphUtil(unittest.TestCase):
    def test_subgraph(self):
        # Test graph with no connections
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        subgraphs = graph_util.get_subgraphs(data)
        self.assertTrue(len(subgraphs) == 3)

        # Graph with one connection
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        subgraphs = graph_util.get_subgraphs(data)
        self.assertTrue(len(subgraphs) == 2)
        self.assertTrue([0, 1] in subgraphs or [1, 0] in subgraphs)
        self.assertTrue([2] in subgraphs)

        # Fully connected
        # TODO: this test relies on specific order in the subgraph creation (bad!)
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 1, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        subgraphs = graph_util.get_subgraphs(data)
        self.assertTrue(subgraphs == [[0,1,2]])
    

    def test_swap_lower_right(self):
        mat_1 = np.ndarray(shape=(3,3), buffer=np.repeat(1,9), dtype=np.int32)
        mat_2 = np.ndarray(shape=(4,4), buffer=np.repeat(2,16), dtype=np.int32)

        correct_1 = np.ndarray(shape=(2,2), buffer=np.array([1,2,0,2]), dtype=np.int32)
        correct_2 = np.ndarray(shape=(5,5), buffer=np.array([2,2,2,1,1,
                                                             2,2,2,0,0,
                                                             2,2,2,0,0,
                                                             0,0,0,1,1,
                                                             0,0,0,1,1]), dtype=np.int32)
        
        mat_1, mat_2 = graph_util.swap_lower_right(mat_1, mat_2, 1, 3)
        self.assertTrue(np.array_equal(mat_1, correct_1))
        self.assertTrue(np.array_equal(mat_2, correct_2))


    def test_set_num_connections(self):
        for i in range(50):
            mat = np.random.randint(0, 2, (5, 5))
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if i >= j:
                        mat[i][j] = 0
            spanning_tree = graph_util.get_spanning_tree(mat)
            min_length = len(mat) - 1
            max_length = (len(mat) - 1) * (len(mat)) / 2

            # Determine final lengths
            length = random.randint(min_length, max_length)
            graph_util.set_num_connections(mat, spanning_tree, length)
            self.assertEqual(sum(sum(mat)), length)
            for node_1 in spanning_tree:
                for node_2 in spanning_tree[node_1]:
                    self.assertEqual(mat[min(node_1, node_2)][max(node_1, node_2)], 1)
    
    def test_spanning_tree(self):
        for i in range(50):
            mat = np.random.randint(0, 2, (5, 5))
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if i >= j:
                        mat[i][j] = 0
            spanning_tree = graph_util.get_spanning_tree(mat)
            length = sum(len(spanning_tree[node_1]) for node_1 in spanning_tree)
            self.assertEqual(length, len(mat) - 2)
    
    def test_make_exterior_connected(self):
        mat = np.ndarray(shape=(3,3), buffer=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        graph_util.make_exterior_connected(mat)
        self.assertTrue((mat[0,1] == 1) or (mat[0,2] == 1))
        mat = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        correct = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        graph_util.make_exterior_connected(mat)
        self.assertTrue(np.array_equal(mat, correct))

    def test_pair_distances(self):
        data = np.ndarray(shape=(4,4), buffer=np.array([0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        correct_result = np.ndarray(shape=(4,4), buffer=np.array([0, 1, 1, 1, 1, 0, 2, 1, 1, 2, 0, 2, 1, 1, 2, 0]), dtype=np.int32)
        ind = Individual(data, [0, 1, 2, 3])
        pair_distances = ind.get_all_pairs_distances()
        self.assertTrue(np.array_equal(pair_distances, correct_result))

        # Also test distance score
        """
        dist_pref = np.ndarray(shape=(4,4), buffer=np.array([0, 1, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]), dtype=np.int32)
        config = BuildingConfig([], None, dist_pref, None, None)
        self.assertEqual(ind.get_distance_score(config), 1)
        """


class TestMutation(unittest.TestCase):
    def test_number_of_node_mutation(self):
        config = BuildingConfig([Room("A", 0, (2, 4), 1, None), Room("B", 0, (2, 4), 1, None), Room("C", 0, (2, 4), 1, None)], None, None, None, None)
        data = np.zeros((3,3))
        ind = Individual(data, [0, 1, 2])
        mutation.number_of_node_mutation(ind, config, True)
        self.assertEqual(len(ind.adj_mat), 4)
        self.assertEqual(len(ind.adj_mat), len(ind.room_types))
        mutation.number_of_node_mutation(ind, config, False)
        mutation.number_of_node_mutation(ind, config, False)
        self.assertEqual(len(ind.adj_mat), 2)
        self.assertEqual(len(ind.adj_mat), len(ind.room_types))
    
    def test_number_of_edge_mutation(self):
        # For some reason it doesn't work unless the 1:s are floats
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 0, 1.0, 0, 0, 1.0, 0, 0, 0]))
        individual = Individual(data, [0, 1, 2])
        mutation.number_of_edge_mutation(individual, True)
        self.assertEqual(individual.get_sum(), 3)
        mutation.number_of_edge_mutation(individual, False)
        mutation.number_of_edge_mutation(individual, False)
        self.assertEqual(individual.get_sum(), 3)

        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1.0, 1.0, 0, 0, 0, 0, 0, 0]))
        individual = Individual(data, [0, 1, 2])
        mutation.number_of_edge_mutation(individual, True)
        self.assertEqual(individual.get_sum(), 3)

        # No connections
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 0, 0.0, 0, 0, 0.0, 0, 0, 0]))
        individual = Individual(data, [0, 1, 2])
        mutation.number_of_edge_mutation(individual, True)
        self.assertEqual(individual.get_sum(), 1)
        mutation.number_of_edge_mutation(individual, False)
        self.assertEqual(individual.get_sum(), 2)

        # Full connections
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1.0, 1.0, 0, 0, 1.0, 0, 0, 0]))
        individual = Individual(data, [0, 1, 2])
        mutation.number_of_edge_mutation(individual, True)
        self.assertEqual(individual.get_sum(), 2)

    def test_node_label_mutation(self):
        config = BuildingConfig([Room("A", 0, (2, 4), 1, None), Room("B", 0, (2, 4), 1, None), Room("C", 0, (2, 4), 1, None)], None, None, None, None)
        data = np.zeros((3,3))
        ind = Individual(data, [0, 1, 2])
        for i in range(10):
            mutation.node_label_mutation(ind, config)
            self.assertTrue(ind.room_types[1] in [1,2] and ind.room_types[2] in [1,2])

    def test_swap_node_mutation(self):
        data = np.zeros((3,3))
        ind = Individual(data, [0, 1, 2])
        for i in range(10):
            mutation.swap_node_mutation(ind)
            self.assertTrue(ind.room_types == [0,1,2] or ind.room_types == [0,2,1])

        data = np.zeros((2,2))
        ind = Individual(data, [0, 1])
        # Should not be able to do anything with only one non-exterior room
        mutation.swap_node_mutation(ind)
        self.assertTrue(ind.room_types == [0,1])


if __name__ == '__main__':
    unittest.main()