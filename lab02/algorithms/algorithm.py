from abc import ABC, abstractmethod

import numpy as np

from lab02.solution import Solution


class Algorithm(ABC):
    def __init__(self, data: np.ndarray):
        self.data = data
        self.solution = None
        # super().__init__()

    @abstractmethod
    def run(self, *args, **kwargs) -> Solution:
        raise NotImplementedError("Subclass must implement abstract method")

    def cycle_length(self, cycle, close=False):
        length = 0
        for i, n in enumerate(cycle[:-1]):
            length += self.data[n, cycle[i+1]]
        if close:
            length += self.data[cycle[-1], cycle[0]]
        return length

    def _get_node_info(self, node):
        cycles = [self.left, self.right]

        cycle = 0 if node in cycles[0] else 1
        pos = np.argwhere(cycles[cycle] == node)[0][0]

        return cycle, pos
