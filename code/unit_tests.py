import unittest
import numpy as np
import graph_util
from individual_meta import IndividualMeta

class TestGA(unittest.TestCase):
    def test_permutation(self):
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 1, 0, 0, 0, 0, 0, 0]))
        correct_permute_data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 1, 0, 0, 0]))
        meta = IndividualMeta([0, 1, 2])

        new_order = [2, 0, 1]
        meta.permute_order(data, new_order)

        self.assertTrue(np.array_equal(data, correct_permute_data))
        self.assertEqual(meta.room_types, new_order)

    def test_fitness_permutation(self):
        rooms = 6
        shape = (rooms, rooms)
        adjacencies = np.random.randint(0, 2, shape)
        preferences = np.random.randint(-3, 4, shape)
        # Make sure is diagonal
        for i in range(rooms):
            for j in range(rooms):
                # Use XOR operator to flip the bit if the conditions are met
                adjacencies[i][j] = adjacencies[i][j] if i < j else 0
                preferences[i][j] = preferences[i][j] if i < j else 0
    

        meta = IndividualMeta(list(range(rooms)))
        original_fitness = meta.get_roomtype_multiplication(adjacencies, preferences)
        for i in range(5):
            """
            print('Original adj\n', adjacencies)
            print('Original order\n', meta.room_types)
            """
            meta.permute_order(adjacencies)
            """
            print('Permuted adj\n', adjacencies)
            print('Permuted order\n', meta.room_types)
            print('Preferences\n', preferences)
            """
            permuted_fitness = meta.get_roomtype_multiplication(adjacencies, preferences)
            self.assertEqual(original_fitness, permuted_fitness)


class TestGraphUtil(unittest.TestCase):
    def test_subgraph(self):
        # Test graph with no connections
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))
        subgraphs = graph_util.get_subgraphs(data)
        self.assertTrue(len(subgraphs) == 3)

        # Graph with one connection
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]))
        subgraphs = graph_util.get_subgraphs(data)
        self.assertTrue(len(subgraphs) == 2)
        self.assertTrue([0, 1] in subgraphs or [1, 0] in subgraphs)
        self.assertTrue([2] in subgraphs)

        # Fully connected
        # TODO: this test relies on specific order in the subgraph creation (bad!)
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 1, 0, 0, 0, 0, 0, 0]))
        subgraphs = graph_util.get_subgraphs(data)
        self.assertTrue(subgraphs == [[0,1,2]])
    

    def test_swap_lower_right(self):
        mat_1 = np.ndarray(shape=(3,3), buffer=np.repeat(1,9))
        mat_2 = np.ndarray(shape=(4,4), buffer=np.repeat(2,16))

        correct_1 = np.ndarray(shape=(2,2), buffer=np.array([1,0,0,2]))
        correct_2 = np.ndarray(shape=(5,5), buffer=np.array([2,2,2,0,0,
                                                             2,2,2,0,0,
                                                             2,2,2,0,0,
                                                             0,0,0,1,1,
                                                             0,0,0,1,1]))
        
        mat_1, mat_2 = graph_util.swap_lower_right(mat_1, mat_2, 1, 3)
        self.assertTrue(np.array_equal(mat_1, correct_1))
        self.assertTrue(np.array_equal(mat_2, correct_2))


if __name__ == '__main__':
    unittest.main()