import random
from copy import deepcopy
from time import perf_counter

import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab02.solution import Solution


class ILSWithPerturbation(Algorithm):
    def __init__(self, data: np.ndarray, left, right, time_limit):
        super().__init__(data)
        self.left = left
        self.right = right
        self.solution = Solution(data, left, right)

        self.time_limit = time_limit

    def run(self):
        time1 = perf_counter()
        cycles = [self.left, self.right]

        while perf_counter() - time1 < self.time_limit:
            # np. na wymianie kilku krawędzi i/lub wierzchołków na inne, wybrane losowo.
            l, r = deepcopy(self.left), deepcopy(self.right)
            for _ in range(5):
                a, b = random.sample(range(len(self.data)), 2)
                ca, pa = self._get_node_info(a)
                cb, pb = self._get_node_info(b)

                cycles[ca][pa], cycles[cb][pb] = b, a

            s = Solution(self.data, l, r)

            if (sol := sum(s.length())) < sum(self.solution.length()):
                self.solution = deepcopy(s)
                l, r = self.left, self.right
                print(f"new solution: {sol}")

        return self.solution

    def _get_node_info(self, node):
        cycles = [self.left, self.right]

        cycle = 0 if node in cycles[0] else 1
        pos = np.argwhere(cycles[cycle] == node)[0][0]

        return cycle, pos
