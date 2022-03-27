import numpy as np
import random
import time

from lab02.algorithms.local_algorithm import LocalAlgorithm
from lab02.solution import Solution


class RandomLocal(LocalAlgorithm):
    def run(self):
        random.seed()
        start = time.time()
        # end = time.time()
        length = self.cycle_length(self.data_l) + self.cycle_length(self.data_r)
        while True and time.time() - start < 3:
            order = random.choice(self.moves)
            left_cycle, right_cycle = order()
            # end = time.time()
            gain = self.cycle_length(left_cycle) + self.cycle_length(right_cycle)
            if gain < length:
                length = gain
                self.data_l = left_cycle.copy()
                self.data_r = right_cycle.copy()
        self.solution = Solution(self.data, self.data_l, self.data_r)
        return self.solution

    def inside_move(self):
        random.seed()
        left_cycle = self.data_l.copy()
        right_cycle = self.data_r.copy()
        for cycle in [left_cycle, right_cycle]:
            possible_change = self.find_possible(cycle, "inside")
            random.shuffle(possible_change)
            self.variant = "edges" if random.randint(0, 1) == 0 else "vertices"
            print(self.variant)
            for i, j in possible_change:
                if self.variant == "edges":
                    gain = self.delta_edge_inside(cycle, i, j)
                else:
                    gain = self.delta_vert_inside(cycle, i, j)
                if gain > 0 and self.variant == "vertices":
                    cycle[i], cycle[j] = cycle[j], cycle[i]
                    return left_cycle, right_cycle
                elif gain > 0 and self.variant == "edges":
                    cycle[i:j+1] = np.flipud(cycle[i:j+1])
                    return left_cycle, right_cycle
        return left_cycle, right_cycle

    def outside_move(self):
        random.seed()
        left_cycle = self.data_l.copy()
        right_cycle = self.data_r.copy()
        for cycle in [left_cycle, right_cycle]:
            possible_change = self.find_possible(cycle, "outside")
            random.shuffle(possible_change)
            for i, j in possible_change:
                gain = self.delta_vert_outside(cycle, i, j)
                if gain > 0:
                    if np.array_equiv(cycle, left_cycle):
                        cycle[i], right_cycle[j] = right_cycle[j], cycle[i]
                    else:
                        cycle[i], left_cycle[j] = left_cycle[j], cycle[i]
                    return left_cycle, right_cycle
        return left_cycle, right_cycle
