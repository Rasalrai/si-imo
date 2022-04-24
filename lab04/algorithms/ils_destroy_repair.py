import random
from copy import deepcopy
from time import perf_counter

import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab02.solution import Solution


class ILSDestroyRepair(Algorithm):
    def __init__(self, data: np.ndarray, left, right, time_limit=60, destroy_prob=0.2):
        super().__init__(data)
        self.left = deepcopy(left)
        self.right = deepcopy(right)
        self.destroy_prob = destroy_prob
        self.solution = Solution(data, left.copy(), right.copy())

        self.time_limit = time_limit

    def run(self):
        destroy_size = int(self.destroy_prob * len(self.left))
        time1 = perf_counter()

        while perf_counter() - time1 < self.time_limit:
            # Destroy
            visited = np.ones(self.data.shape[0], dtype=bool)
            destroy_l = random.sample(range(self.left.size), k=destroy_size)
            destroy_r = random.sample(range(self.right.size), k=destroy_size)

            for d in destroy_l:
                visited[self.left[d]] = False
                self.left[d] = -1
            for d in destroy_r:
                visited[self.right[d]] = False
                self.right[d] = -1

            # Repair - greedy NN
            cycles = [self.left, self.right]
            while not np.all(visited):
                for i in range(len(cycles[0])):
                    for ic, cycle in enumerate(cycles):
                # for ic, cycle in enumerate(cycles):
                #     for i, node in enumerate(cycle):
                        if cycle[i] == -1:
                            continue
                        if np.all(visited):
                            break
                        # find closest unvisited node
                        if cycle[(i + 1) % len(cycle)] == -1:
                            closest_node, closest_dist = None, np.inf
                            for j in np.argwhere(visited == False)[0]:
                                dist = self.data[cycle[i], j]
                                if dist < closest_dist:
                                    closest_node, closest_dist = j, dist
                            cycles[ic][(i+1) % len(cycle)] = closest_node
                            visited[closest_node] = True
            new_solution = Solution(self.data, self.left.copy(), self.right.copy())
            if np.any(self.left == -1) or np.any(self.right == -1):
                print("Error")
            if sum(new_solution.length()) < sum(self.solution.length()):
                self.solution = deepcopy(new_solution)
                print(f"New solution: {sum(self.solution.length())}")

        return self.solution
