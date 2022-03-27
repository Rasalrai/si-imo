import numpy as np
import random
import time

from lab02.algorithms.local_algorithm import LocalAlgorithm
from lab02.solution import Solution


class GreedyLocal(LocalAlgorithm):
    def run(self):
        random.seed()
        # start = time.time()
        # end = time.time()
        while True:
            order = random.sample(self.moves, 2)
            gain = order[0]()
            # end = time.time()
            if gain <= 0:
                gain = order[1]()
                if gain <= 0:
                    break
        self.solution = Solution(self.data, self.data_l, self.data_r)
        return self.solution

    def inside_move(self):
        random.seed()
        gain = 0
        for cycle in [self.data_l, self.data_r]:
            possible_change = self.find_possible(cycle, "inside")
            random.shuffle(possible_change)
            for i, j in possible_change:
                if self.variant == "edges":
                    gain = self.delta_edge_inside(cycle, i, j)
                else:
                    gain = self.delta_vert_inside(cycle, i, j)
                if gain > 0 and self.variant == "vertices":
                    cycle[i], cycle[j] = cycle[j], cycle[i]
                    return gain
                elif gain > 0 and self.variant == "edges":
                    cycle[i:j+1] = np.flipud(cycle[i:j+1])
                    return gain
        return gain

    def outside_move(self):
        random.seed()
        gain = 0
        for cycle in [self.data_l, self.data_r]:
            possible_change = self.find_possible(cycle, "outside")
            random.shuffle(possible_change)
            for i, j in possible_change:
                gain = self.delta_vert_outside(cycle, i, j)
                if gain > 0:
                    if np.array_equiv(cycle, self.data_l):
                        cycle[i], self.data_r[j] = self.data_r[j], cycle[i]
                    else:
                        cycle[i], self.data_l[j] = self.data_l[j], cycle[i]
                    return gain
        return gain
