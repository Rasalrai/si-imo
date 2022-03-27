from abc import ABC, abstractmethod

import numpy as np

from lab02.solution import Solution


class LocalAlgorithm(ABC):
    def __init__(self, variant: str, data_l: np.ndarray, data_r: np.ndarray, data: np.ndarray):
        self.data = data
        self.data_l = data_l.copy()
        self.data_r = data_r.copy()
        self.variant = variant
        self.moves = [self.inside_move, self.outside_move]
        self.solution = None
        # super().__init__()

    @abstractmethod
    def run(self, *args, **kwargs) -> Solution:
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def inside_move(self):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def outside_move(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def find_possible(self, cycle, direction):
        possible = []
        if direction == "inside":
            for l in range(cycle.shape[0]):
                for r in range(l + 1, cycle.shape[0]):
                    possible.append([l, r])
        else:
            for cycle_1 in range(cycle.shape[0]):
                for cycle_2 in range(cycle.shape[0]):
                    possible.append([cycle_1, cycle_2])
        return possible

    def delta_vert_inside(self, cycle, a, b):
        original_cycle = self.cycle_length(cycle, close=True)
        new_cycle = cycle.copy()
        new_cycle[a], new_cycle[b] = new_cycle[b], new_cycle[a]
        new_cycle = self.cycle_length(new_cycle, close=True)
        return original_cycle - new_cycle

    def delta_edge_inside(self, cycle, a, b):
        original_cycle = self.cycle_length(cycle, close=True)
        changed_cycle = cycle.copy()
        changed_cycle[a:b + 1] = np.flipud(changed_cycle[a:b + 1])
        new_cycle = self.cycle_length(changed_cycle, close=True)
        return original_cycle - new_cycle

    def delta_vert_outside(self, cycle, a, b):
        before_i, i, after_i = cycle[a - 1], cycle[a], cycle[(a + 1) % cycle.shape[0]]
        if np.array_equiv(cycle, self.data_l):
            before_j, j, after_j = self.data_r[b - 1], self.data_r[b], self.data_r[(b + 1) % self.data_r.shape[0]]
        else:
            before_j, j, after_j = self.data_l[b - 1], self.data_l[b], self.data_l[(b + 1) % self.data_l.shape[0]]

        original_cycles = self.data[before_i][i] + \
                          self.data[i][after_i] + \
                          self.data[before_j][j] + \
                          self.data[j][after_j]
        new_cycles = self.data[before_i][j] + \
                     self.data[j][after_i] + \
                     self.data[before_j][i] + \
                     self.data[i][after_j]

        return original_cycles - new_cycles

    def cycle_length(self, cycle, close=False):
        length = 0
        for i, n in enumerate(cycle[:-1]):
            length += self.data[n, cycle[i + 1]]
        if close:
            length += self.data[cycle[-1], cycle[0]]
        return length

    # def
