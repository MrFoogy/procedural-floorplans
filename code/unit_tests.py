import unittest
import numpy as np
from individual_meta import IndividualMeta

class TestGA(unittest.TestCase):
    def test_permutation(self):
        data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 1, 0, 0, 0, 0, 0, 0]))
        correct_permute_data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 0, 0, 0, 1, 0, 0, 0]))
        meta = IndividualMeta(None, [0, 1, 2])

        new_order = [2, 0, 1]
        meta.permute_order(data, new_order)

        self.assertTrue(np.array_equal(data, correct_permute_data))
        self.assertEqual(meta.order, new_order)

        # Test some random permutations
        meta.permute_order(data)
        meta.permute_order(data)
        meta.permute_order(data)
        meta.permute_order(data, [0,1,2])
        original_data = np.ndarray(shape=(3,3), buffer=np.array([0, 1, 1, 0, 0, 0, 0, 0, 0]))
        self.assertTrue(np.array_equal(data, original_data))

    def test_fitness_permutation(self):
        rooms = 6
        shape = (rooms, rooms)
        adjacencies = np.random.randint(0, 2, shape)
        preferences = np.random.randint(-3, 4, shape)
        # Make sure is diagonal
        for i in range(rooms):
            for j in range(rooms):
                # Use XOR operator to flip the bit if the conditions are met
                adjacencies[i][j] = adjacencies[i][j] and i < j
                preferences[i][j] = preferences[i][j] if i < j else 0
    

        meta = IndividualMeta(None, list(range(rooms)))
        original_fitness = meta.get_permuted_multiplication(adjacencies, preferences)
        for i in range(5):
            #print('Original adj\n', adjacencies)
            #print('Original order\n', meta.order)
            meta.permute_order(adjacencies)
            #print('Permuted adj\n', adjacencies)
            #print('Permuted order\n', meta.order)
            #print('Preferences\n', preferences)
            permuted_fitness = meta.get_permuted_multiplication(adjacencies, preferences)
            self.assertEqual(original_fitness, permuted_fitness)


if __name__ == '__main__':
    unittest.main()