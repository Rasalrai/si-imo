import numpy as np
import random

from lab01.algorithms.algorithm import Algorithm
from lab01.solution import Solution


class RegretAlgorithm(Algorithm):
    def run(self, start1=None):
        nodes_n = self.data.shape[0]
        if start1 is None:
            start1 = random.randint(0, self.data.shape[0])
        visited = np.zeros(nodes_n, dtype=bool)

        # get farthest node from start_node
        start2, max_dist = None, self.data[start1, 0]
        for i, d in enumerate(self.data[start1, 1:]):
            if d > max_dist:
                max_dist, start2 = d, i

        visited[start1] = visited[start2] = True
        cycles = [np.zeros(shape=(nodes_n // 2,), dtype=int) for _ in range(2)]
        cycles[0][0] = start1
        cycles[1][0] = start2

        # insert the second node in a greedy way
        for cycle in cycles:
            first = cycle[0]
            best_node, best_dist = -1, np.inf
            for i, d in enumerate(self.data[first]):
                if d < best_dist and not visited[i]:
                    best_dist, best_node = d, i
            cycle[1] = best_node
            visited[best_node] = True

        # regret
        for i in range(1, nodes_n // 2 - 1):
            for ic, cycle in enumerate(cycles):
                # setup
                # best spot, its 2-regret - for each non-visited node
                regrets = np.zeros(shape=(nodes_n, 2), dtype=int)
                for n, n_visited in enumerate(visited):
                    if n_visited:
                        regrets[n] = [-1, -1]
                        continue

                    # get costs of inserting into each spot
                    insert_options = np.zeros(shape=(i+1, 2), dtype=int)    # [where, how good]
                    for j in range(i + 1):
                        if i == j:
                            replaced_edge = self.data[cycle[j], cycle[0]]
                            new_edges = self.data[cycle[j], n] + self.data[n, cycle[0]]
                        else:
                            replaced_edge = self.data[cycle[j], cycle[j+1]]
                            new_edges = self.data[cycle[j], n] + self.data[n, cycle[j+1]]
                        insert_options[j] = [j, new_edges - replaced_edge]

                    # sort them by regret (asc) and save the 2-regret
                    insert_options = insert_options[insert_options[:, 1].argsort()][:2]
                    regrets[n] = insert_options[0, 0], insert_options[1, 1] - insert_options[0, 1]

                # best node, best spot (for best node), regret of it
                non, rien_de_rien, je_ne_regrette_rien = -1, -1, -1
                for j, (wh, r) in enumerate(regrets):
                    if r > je_ne_regrette_rien:
                        non, rien_de_rien, je_ne_regrette_rien = j, wh, r

                cycles[ic] = np.insert(cycle, rien_de_rien + 1, non)
                visited[non] = True

        self.solution = Solution(self.data, cycles[0][:nodes_n // 2], cycles[1][:nodes_n // 2])
        return self.solution
