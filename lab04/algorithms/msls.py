# Multiple Start Local Search
from copy import deepcopy

import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab01.algorithms.random import RandomAlgorithm
from lab02.solution import Solution
from lab03.algorithms.improving_moves import ImprovingMovesAlgorithm


class MultipleStartLocalSearch(Algorithm):
    def __init__(self, data: np.ndarray, left, right, time_limit=2):
        super().__init__(data)
        self.left = left
        self.right = right
        self.time_limit = time_limit
        self.random_algorithm = RandomAlgorithm(data)
        self.solution = self.random_algorithm.run()

    def run(self) -> Solution:
        for _ in range(50):
            random_s = self.random_algorithm.run()
            self.left, self.right = deepcopy(random_s.left_i), deepcopy(random_s.right_i)
            s = ImprovingMovesAlgorithm(self.data, random_s.left_i, random_s.right_i, self.time_limit).run()

            if sum(s.length()) < sum(self.solution.length()):
                self.solution = s

        return self.solution
