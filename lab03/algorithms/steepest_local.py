import numpy as np

from lab02.algorithms.local_algorithm import LocalAlgorithm
from lab01.solution import Solution


class SteepestLocal(LocalAlgorithm):
    def run(self):
        # self.data_l = left.copy()
        # self.data_r = right.copy()
        while True:
            gain_inside, first_ver_in, second_ver_in, sel_cycle = self.moves[0]()
            gain_outside, first_ver_out, second_ver_out, first_cycle, second_cycle = self.moves[1]()
            gain = max(gain_inside, gain_outside)
            if gain <= 0:
                break
            else:
                if gain == gain_inside and self.variant == "vertices":
                    sel_cycle[first_ver_in], \
                    sel_cycle[second_ver_in] = sel_cycle[second_ver_in], \
                                               sel_cycle[first_ver_in]
                elif gain == gain_inside and self.variant == "edges":
                    sel_cycle[first_ver_in:second_ver_in+1] = np.flipud(sel_cycle[first_ver_in:second_ver_in+1])
                else:
                    first_cycle[first_ver_out], second_cycle[second_ver_out] = second_cycle[second_ver_out],\
                                                                               first_cycle[first_ver_out]

        self.solution = Solution(self.data, self.data_l, self.data_r)
        return self.solution

    def inside_move(self):
        max_gain, first_ver, second_ver, sel_cycle = 0, None, None, None
        for cycle in [self.data_l, self.data_r]:
            possible_change = self.find_possible(cycle, "inside")
            for i, j in possible_change:
                if self.variant == "edges":
                    gain = self.delta_edge_inside(cycle, i, j)
                else:
                    gain = self.delta_vert_inside(cycle, i, j)
                if gain > max_gain:
                    max_gain, first_ver, second_ver, sel_cycle = gain, i, j, cycle
        return max_gain, first_ver, second_ver, sel_cycle

    def outside_move(self):
        max_gain, first_ver, second_ver, first_cycle, second_cycle = 0, None, None, None, None
        for cycle in [self.data_l, self.data_r]:
            possible_change = self.find_possible(cycle, "outside")
            for i, j in possible_change:
                gain = self.delta_vert_outside(cycle, i, j)
                if gain > max_gain:
                    max_gain, first_ver, second_ver = gain, i, j
                    first_cycle = cycle if np.array_equiv(cycle, self.data_l) else self.data_r
                    second_cycle = self.data_r if np.array_equiv(cycle, self.data_l) else self.data_l
        return max_gain, first_ver, second_ver, first_cycle, second_cycle
