import random

import numpy as np

from lab02.algorithms.algorithm import Algorithm
from lab02.solution import Solution


class RandomAlgorithm(Algorithm):

    def run(self, *args, **kwargs):
        size = self.data.shape[0]

        # split data randomly into two parts
        split = random.sample(range(size), size // 2)
        random.shuffle(nodes_right := [i for i in range(size) if i not in split])

        nodes_left = np.array(split)
        nodes_right = np.array(nodes_right)

        # save the solution
        self.solution = Solution(self.data, nodes_left, nodes_right)
        return self.solution
