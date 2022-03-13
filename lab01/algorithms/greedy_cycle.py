import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab01.solution import Solution


class GreedyCycleAlgorithm(Algorithm):
    def run(self, start1):
        nodes_n = self.data.shape[0]
        visited = np.zeros(nodes_n, dtype=bool)

        # get farthest node from start_node
        start2 = 0
        max_dist = self.data[start1, 0]
        for i, d in enumerate(self.data[start1, 1:]):
            if d > max_dist:
                max_dist, start2 = d, i

        visited[start1] = visited[start2] = True

        cycles = [np.empty(shape=(nodes_n // 2,), dtype=int) for _ in range(2)]
        cycles[0][0] = start1
        cycles[1][0] = start2

        # TODO
        # check unvisited nodes and see which one would elongate the current cycle the least
        for i in range(nodes_n // 2 - 1):
            for cycle in cycles:
                # check all unvisited nodes
                    # check all possible places to insert the node
                pass
