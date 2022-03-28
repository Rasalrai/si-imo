import numpy as np
import random
import time

from lab02.algorithms.local_algorithm import LocalAlgorithm
from lab02.solution import Solution


class RandomLocal(LocalAlgorithm):
    time_limit = 3

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def run(self):
        random.seed()
        start = time.time()
        # end = time.time()
        best_length = self.cycle_length(self.data_l) + self.cycle_length(self.data_r)
        best_l, best_r = self.data_l, self.data_r

        while time.time() - start < self.time_limit:
            move = random.choice(self.moves)
            self.data_l, self.data_r = move()

            new_len = self.cycle_length(self.data_l) + self.cycle_length(self.data_r)
            if new_len < best_length:
                best_length = new_len
                best_l, best_r = self.data_l.copy(), self.data_r.copy()

        self.solution = Solution(self.data, best_l, best_r)
        return self.solution

    def inside_move(self):
        random.seed()
        left_cycle = self.data_l.copy()
        right_cycle = self.data_r.copy()
        for cycle in [left_cycle, right_cycle]:
            possible_change = self.find_possible(cycle, "inside")
            random.shuffle(possible_change)
            self.variant = "edges" if random.randint(0, 1) == 0 else "vertices"
            # print(self.variant)
            for i, j in possible_change:
                if self.variant == "edges":
                    gain = self.delta_edge_inside(cycle, i, j)
                else:
                    gain = self.delta_vert_inside(cycle, i, j)
                if self.variant == "vertices":
                    cycle[i], cycle[j] = cycle[j], cycle[i]
                    return left_cycle, right_cycle
                elif self.variant == "edges":
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
                if np.array_equiv(cycle, left_cycle):
                    cycle[i], right_cycle[j] = right_cycle[j], cycle[i]
                else:
                    cycle[i], left_cycle[j] = left_cycle[j], cycle[i]
                return left_cycle, right_cycle
        return left_cycle, right_cycle
