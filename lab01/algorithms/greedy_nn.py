import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab01.solution import Solution


class GreedyNNAlgorithm(Algorithm):
    def run(self, start1):
        nodes_n = self.data.shape[0]

        # get farthest node from start_node
        start2 = 0
        max_dist = self.data[start1, 0]
        for i, d in enumerate(self.data[start1, 1:]):
            if d > max_dist:
                max_dist, start2 = d, i

        # saving indices of nodes that are a part of a cycle
        visited = np.zeros(nodes_n, dtype=bool)
        visited[start1] = visited[start2] = True

        cycles = [np.empty(shape=(nodes_n // 2,), dtype=int) for _ in range(2)]
        cycles[0][0] = start1
        cycles[1][0] = start2

        # find nearest available neighbours
        for i in range(nodes_n // 2 - 1):
            for cycle in cycles:
                last = cycle[i]
                best_node, best_dist = -1, self.data.max()
                for j, d in enumerate(self.data[last]):
                    if i != j and d < best_dist and not visited[j]:
                        best_node, best_dist = j, d

                cycle[i + 1] = best_node
                visited[best_node] = True

        self.solution = Solution(self.data, *cycles)
