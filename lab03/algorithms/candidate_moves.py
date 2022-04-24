from time import perf_counter

import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab02.solution import Solution
from lab02.algorithms.local_algorithm import LocalAlgorithm
from lab03.move import Move


class CandidateMovesAlgorithm(Algorithm):
    def __init__(self, data, left, right, n_neigh=10, time_limit=300):
        super().__init__(data)
        # get neighbours for each node
        self.left = left.copy()
        self.right = right.copy()
        self.neighbours = self.get_neighbours(n_neigh)

        self.time_limit = time_limit

    def get_neighbours(self, neighbours_count):
        neighbours = np.empty(shape=(self.data.shape[0], neighbours_count), dtype=int)
        for i, nbh in enumerate(self.data):
            neighbours[i] = nbh.argsort()[1:neighbours_count + 1]

        return neighbours

    def run(self) -> Solution:
        size = len(self.left)
        cycles = [self.left, self.right]

        # wrap this in something? add exit condition
        time1 = perf_counter()

        while perf_counter() - time1 < self.time_limit:
            # print(f"{sum(Solution(self.data, *cycles).length())}")
            move_done = False
            best_move = None
            best_change = 0
            for ic, cycle in enumerate(cycles):
                for i, node in enumerate(cycle):
                    for j, nbh in enumerate(self.neighbours[node]):
                        if (ch := self.check_v_move(node, nbh)) < best_change:
                            best_move, best_change = Move("v", (node, nbh)), ch
                        x = cycle[i-1]
                        cycle_n, pos_n = self._get_node_info(nbh)
                        for y in (cycles[cycle_n][pos_n-1], cycles[cycle_n][(pos_n+1) % len(cycles[cycle_n])]):
                            if (ch := self.check_e_move((x, node), (nbh, y))) < best_change:
                                best_move, best_change = Move("e", ((x, node), (nbh, y))), ch
                            if (ch := self.check_e_move((node, x), (nbh, y))) < best_change:
                                best_move, best_change = Move("e", ((node, x), (nbh, y))), ch

                    if best_change < -10_000:
                        break

                        # add an edge to the neighbour
                        # if nbh not in cycle:
                        #     ni = np.argwhere(cycles[ic - 1] == nbh)[0][0]
                        #     len_before = self.data[cycle[i - 2]][cycle[i - 1]] + self.data[cycle[i - 1]][cycle[i]]
                        #     len_after = self.data[cycle[i - 2]][ni] + self.data[ni][cycle[i]]
                        #     if len_after < len_before:
                        #         # swap the neighbour and a node before (or after) the current node
                        #         cycles[ic - 1][ni] = cycle[i - 1]
                        #         cycle[i - 1] = nbh
                        #         move_done = True
                        #
                        #     # get length of i-2 - i+2
                        #     # find the best placement
                        # else:
                        #     ni = np.argwhere(cycle == nbh)[0][0]
                        #     na, nb = (i, ni) if i < ni else (ni, i)
                        #     len_before = self.data[cycle[(na - 1) % size]][cycle[na % size]] + \
                        #                  self.data[cycle[nb % size]][cycle[(nb + 1) % size]]
                        #     len_after = self.data[cycle[(na - 1 % size)]][cycle[nb % size]] + \
                        #                 self.data[cycle[na % size]][cycle[(nb + 1) % size]]
                        #     if len_after < len_before:
                        #         # swap nodes between i and neighbour
                        #         if nb == len(cycle) - 1:
                        #             cycles[ic][na:] = np.flipud(cycle[na:])
                        #         else:
                        #             cycles[ic][na:nb + 1] = np.flipud(cycle[na:nb + 1])
                        #         move_done = True
            if best_move:
                self.execute_move(best_move)
            else:
                break

        self.solution = Solution(self.data, *cycles)
        return self.solution

    def check_v_move(self, a, b):
        cycles = [self.left, self.right]

        cycle_a, pos_a = self._get_node_info(a)
        cycle_b, pos_b = self._get_node_info(b)

        if cycle_a == cycle_b and pos_a > pos_b:
                a, b = b, a
                pos_a, pos_b = pos_b, pos_a

        if cycle_a == cycle_b and pos_b - pos_a == 1:
            a_n = cycles[cycle_a][pos_a - 1]
            b_n = cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])]

            a_pre = self.data[a, a_n]
            b_pre = self.data[b, b_n]
            a_post = self.data[a, b_n]
            b_post = self.data[b, a_n]
        else:
            a_n1 = cycles[cycle_a][pos_a - 1]
            a_n2 = cycles[cycle_b][(pos_a + 1) % len(cycles[cycle_a])]
            b_n1 = cycles[cycle_b][pos_b - 1]
            b_n2 = cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])]

            a_pre = self.data[a, a_n1] + self.data[a, a_n2]
            b_pre = self.data[b, b_n1] + self.data[b, b_n2]
            a_post = self.data[a, b_n2] + self.data[a, b_n1]
            b_post = self.data[b, a_n2] + self.data[b, a_n1]

        return a_post + b_post - (a_pre + b_pre)

    def check_e_move(self, e1, e2, verbose=False):
        cycles = [self.left, self.right]
        (a, b), (c, d) = e1, e2

        cycle_a, pos_a = self._get_node_info(a)
        cycle_b, pos_b = self._get_node_info(b)
        cycle_c, pos_c = self._get_node_info(c)
        cycle_d, pos_d = self._get_node_info(d)

        if verbose:
            print(f"a: {a} @ ({cycle_a}, {pos_a})")
            print(f"b: {b} @ ({cycle_b}, {pos_b})")
            print(f"c: {c} @ ({cycle_c}, {pos_c})")
            print(f"d: {d} @ ({cycle_d}, {pos_d})")

        if cycle_a != cycle_b or cycle_c != cycle_d:
            return None

        if pos_a > pos_b:
            a_n, b_n = cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], cycles[cycle_a][pos_b - 1]
        else:
            a_n, b_n = cycles[cycle_a][pos_a - 1], cycles[cycle_a][(pos_b + 1) % len(cycles[cycle_a])]
        if pos_c > pos_d:
            c_n, d_n = cycles[cycle_c][(pos_c + 1) % len(cycles[cycle_c])], cycles[cycle_c][pos_d - 1]
        else:
            c_n, d_n = cycles[cycle_c][pos_c - 1], cycles[cycle_c][(pos_d + 1) % len(cycles[cycle_c])]

        if verbose:
            print(f"a: {a} @ {cycle_a}, {pos_a}\tb: {b} @ {cycle_b} {pos_b}")
            print(f"{a_n} <- a, b -> {b_n}")
            print(f"c: {c} @ {cycle_c}, {pos_c}\td: {d} @ {cycle_d}, {pos_d}")
            print(f"{c_n} <- c, d -> {d_n}")

        pre_ab = self.data[a_n, a] + \
                 self.data[b, b_n]
        pre_cd = self.data[c_n, c] + \
                 self.data[d, d_n]

        post_ab = self.data[a_n, b] + \
                  self.data[a, b_n]
        post_cd = self.data[c_n, d] + \
                  self.data[c, d_n]

        if verbose:
            print(f"pre_ab: {self.data[a_n, a]} + {self.data[b, b_n]} = {pre_ab}")
            print(f"pre_cd: {self.data[c_n, c]} + {self.data[d, d_n]} = {pre_cd}")
            print(f"post_ab: {self.data[a_n, b]} + {self.data[a, b_n]} = {post_ab}")
            print(f"post_cd: {self.data[c_n, d]} + {self.data[c, d_n]} = {post_cd}")
            print(f"diff = {post_ab + post_cd - pre_ab - pre_cd}")

        return post_ab + post_cd - pre_ab - pre_cd

    def execute_move(self, move):
        cycles = [self.left, self.right]

        if move.type.lower() == 'e':
            # print('e', end="")
            (a, b), (c, d) = move.nodes

            cycle_a, pos_a = self._get_node_info(a)
            cycle_b, pos_b = self._get_node_info(b)
            cycle_c, pos_c = self._get_node_info(c)
            cycle_d, pos_d = self._get_node_info(d)

            if cycle_a != cycle_b or cycle_c != cycle_d:
                return None

            if cycle_a == cycle_c:
                if pos_a > pos_c:
                    a, b, c, d = c, d, a, b
                    pos_a, pos_b, pos_c, pos_d = pos_c, pos_d, pos_a, pos_b

                # if pos_a > pos_b:
                #     a_n, b_n = cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], cycles[cycle_a][pos_b - 1]
                # else:
                #     a_n, b_n = cycles[cycle_a][pos_a - 1], cycles[cycle_a][(pos_b + 1) % len(cycles[cycle_a])]
                # if pos_c > pos_d:
                #     c_n, d_n = cycles[cycle_c][(pos_c + 1) % len(cycles[cycle_c])], cycles[cycle_c][pos_d - 1]
                # else:
                #     c_n, d_n = cycles[cycle_c][pos_c - 1], cycles[cycle_c][(pos_d + 1) % len(cycles[cycle_c])]

                next = max(pos_c, pos_d) + 1
                if next == len(cycles[cycle_a]):
                    cycles[cycle_a][pos_a:] = np.flipud(cycles[cycle_a][pos_a:])
                else:
                    cycles[cycle_a][pos_a:next] = np.flipud(cycles[cycle_a][pos_a:next])

            else:
                # if pos_a > pos_b:
                #     a_n, b_n = cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], cycles[cycle_a][pos_b - 1]
                # else:
                #     a_n, b_n = cycles[cycle_a][pos_a - 1], cycles[cycle_a][(pos_b + 1) % len(cycles[cycle_a])]
                # if pos_c > pos_d:
                #     c_n, d_n = cycles[cycle_c][(pos_c + 1) % len(cycles[cycle_c])], cycles[cycle_c][pos_d - 1]
                # else:
                #     c_n, d_n = cycles[cycle_c][pos_c - 1], cycles[cycle_c][(pos_d + 1) % len(cycles[cycle_c])]

                cycles[cycle_a][pos_a], cycles[cycle_a][pos_b], cycles[cycle_c][pos_c], cycles[cycle_c][pos_d] = \
                    c, d, a, b

        elif move.type.lower() == 'v':
            # print('v', end="")
            a, b = move.nodes

            cycle_a, pos_a = self._get_node_info(a)
            cycle_b, pos_b = self._get_node_info(b)

            cycles[cycle_a][pos_a], cycles[cycle_b][pos_b] = b, a

    # get all improving moves
    #     self.find_new_moves()
    #     self._sort_moves()
    #
    #     while self.moves:
    #         # execute best move
    #         self.execute_best_move()
    #         # remove executed move from moves
    #         self.moves.pop(0)
    #         # get new improving moves
    #         self.find_new_moves()
    #         # sort moves
    #         self._sort_moves()
    #
    #     pass
    #     self.solution = Solution()
    #
    # def find_new_moves(self):
    #     """przejrzyj wszystkie nowe ruchy i dodaj do LM ruchy przynoszące poprawę"""
    #     pass
    #
    # def _sort_moves(self):
    #     """ sort self.moves by their improvement - delta, and old moves by what's moved """
    #     pass
    #
    # def execute_best_move(self):
    #     move = self.moves.pop(0)
    #     # do the move
    #     raise NotImplementedError()
