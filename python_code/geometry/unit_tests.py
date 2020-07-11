import unittest
import random
import numpy as np
from building import BuildingShape

class TestBuilding(unittest.TestCase):
    def test_area(self):
        points = [(0.0, 0.0), (3.0, 0.0), (3.0, 1.0), (2.0, 1.0), (2.0, 2.0), (1.0, 2.0), (1.0, 1.0), (0.0, 1.0)]
        building_shape = BuildingShape(points)
        self.assertEqual(4.0, building_shape.get_area())
        points = [(point[0] - 5.0, point[1] - 1.5) for point in points]
        building_shape = BuildingShape(points)

    def test_aabb(self):
        points = [(0.0, 0.0), (3.0, 0.0), (3.0, 1.0), (2.0, 1.0), (2.0, 2.0), (1.0, 2.0), (1.0, 1.0), (0.0, 1.0)]
        building_shape = BuildingShape(points)
        self.assertEqual([(0.0, 0.0), (3.0, 2.0)], building_shape.get_aabb())
        self.assertEqual(1.5, building_shape.get_aspect())

if __name__ == '__main__':
    unittest.main()