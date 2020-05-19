import numpy as np
import graph_util


data = np.ndarray(shape=(4,4), buffer=np.array([0, 0, 0, 0,
                                                0, 0, 1, 0, 
                                                0, 0, 0, 0,
                                                0, 0, 0, 0]))

print(graph_util.get_spanning_subtrees(data))
print(graph_util.get_spanning_tree(data))