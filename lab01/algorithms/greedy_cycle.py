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

        cycles = [np.zeros(shape=(nodes_n // 2,), dtype=int) for _ in range(2)]
        cycles[0][0] = start1
        cycles[1][0] = start2

        # check all unvisited nodes and see which one would elongate the current cycle the least
        for i in range(nodes_n // 2 - 1):
            for ic, cycle in enumerate(cycles):
                curr_length = self.cycle_length(cycle[:i + 1])
                best_node, best_after, best_length = None, None, np.inf
                # check all unvisited nodes
                for n, n_visited in enumerate(visited):
                    if n_visited:
                        continue
                    # check all possible places to insert the node
                    #  i - insertion after last node in cycle
                    for j in range(i+1):
                        if (new_len := curr_length - self.data[cycle[j], cycle[j + 1]] +
                                    self.data[cycle[j], n] + self.data[n, cycle[j + 1]]) \
                                < best_length:
                            best_node, best_after, best_length = n, j, new_len

                # insert the best node
                cycles[ic] = np.insert(cycle, best_after + 1, best_node)
                visited[best_node] = True

        self.solution = Solution(self.data, cycles[0][:nodes_n // 2], cycles[1][:nodes_n // 2])
        return self.solution
