import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab01.solution import Solution


class GreedyNNAlgorithm(Algorithm):
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

        # find nearest available neighbours - v2
        #  check with breaking all existing edges
        for i in range(nodes_n // 2 - 1):
            for ic, cycle in enumerate(cycles):
                last = cycle[i]
                # get next node to add
                best_node, best_dist = -1, np.inf
                for j, d in enumerate(self.data[last]):
                    if i != j and d < best_dist and not visited[j]:
                        best_node, best_dist = j, d

                cycle[i + 1] = best_node
                visited[best_node] = True

                # check where it's best to add this node
                curr_length = self.cycle_length(cycle[:i + 1])
                best_after, best_length = i, curr_length + self.data[last, best_node]

                for j in range(0, i):
                    new_len = curr_length - self.data[cycle[j], cycle[j+1]] + \
                              self.data[cycle[j], best_node] + \
                              self.data[best_node, cycle[j + 1]]
                    if new_len < best_length:
                        best_after, best_length = j, new_len

                # insert the node and update distances
                cycles[ic] = np.insert(cycle, best_after + 1, best_node)
                visited[best_node] = True

        self.solution = Solution(self.data, cycles[0][:nodes_n // 2], cycles[1][:nodes_n // 2])
        return self.solution
