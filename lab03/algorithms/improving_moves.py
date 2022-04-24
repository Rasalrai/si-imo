from copy import deepcopy
from time import perf_counter

import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab02.solution import Solution
from lab02.algorithms.local_algorithm import LocalAlgorithm
from lab03.move import Move


class ImprovingMovesAlgorithm(Algorithm):
    def __init__(self, data, left, right, time_limit=300):
        super().__init__(data)
        self.moves: [Move] = []
        self.old_moves = []
        self.left = left
        self.right = right

        self.time_limit = time_limit

    def run(self) -> Solution:
        # self.left = left
        # self.right = right
        # get all improving moves
        self.find_all_moves()
        time1 = perf_counter()
        s_old = sum(Solution(self.data, self.left, self.right).length())
        self.cycles_old = [deepcopy(self.left), deepcopy(self.right)]

        while self.moves and perf_counter() - time1 < self.time_limit:
            # print("*", end="")
            if self.execute_best_move() == -1:  # no more improving moves
                break
            else:
                s = sum(Solution(self.data, self.left, self.right).length())
                if s > s_old:
                    print(f" ! {s} > {s_old} [rolling back]")
                    self.find_all_moves()
                    self.left, self.right = self.cycles_old
                else:
                    print("*", end="")
                s_old = s

        self.solution = Solution(self.data, self.left, self.right)
        # print(f"=== result: {sum(self.solution.length())}")
        return self.solution

    def find_all_moves(self):
        """przejrzyj wszystkie nowe ruchy (zamiana krawędzi) i dodaj do LM (self.moves) ruchy przynoszące poprawę"""
        cycles = [self.left, self.right]
        possible = []

        # for each edge, find all edges that can be swapped with it
        edges = []
        for ic, cycle in enumerate(cycles):
            edges += [(cycle[i - 1], cycle[i]) for i, _ in enumerate(cycle)]
        for ie1, e1 in enumerate(edges):
            for ie2, e2 in enumerate(edges[ie1 + 1:]):
                possible.append(Move("e", (e1, e2)))

        # for each node, find all nodes that can be swapped with it
        for node1 in range(len(self.data)):
            for node2 in range(node1 + 1, len(self.data)):
                possible.append(Move(type="v", nodes=(node1, node2)))

        self.moves = possible
        self._sort_moves(calculate_delta=True)

    def _get_node_info(self, node):
        cycles = [self.left, self.right]

        cycle = 0 if node in cycles[0] else 1
        pos = np.argwhere(cycles[cycle] == node)[0][0]

        return cycle, pos

    def _get_move_delta(self, move: 'Move', verbose=False):
        cycles = [self.left, self.right]

        if move.type.lower() == 'e':
            if verbose:
                pass

            (a, b), (c, d) = move.nodes

            cycle_a, pos_a = self._get_node_info(a)
            cycle_b, pos_b = self._get_node_info(b)
            cycle_c, pos_c = self._get_node_info(c)
            cycle_d, pos_d = self._get_node_info(d)

            if cycle_a != cycle_b or cycle_c != cycle_d:
                return None

            # if pos_a > pos_b:
            #     a, b = b, a
            #     pos_a, pos_b = pos_b, pos_a
            # # if pos_c > pos_d:
            #     c, d = d, c
            #     pos_c, pos_d = pos_d, pos_c

            # prev_a = min(pos_a, pos_b) - 1
            # prev_c = min(pos_c, pos_d) - 1
            # next_a = (max(pos_a, pos_b) + 1) % len(cycles[cycle_a])
            # next_c = (max(pos_c, pos_d) + 1) % len(cycles[cycle_c])
            if pos_a > pos_b:
                a_n, b_n = cycles[cycle_a][(pos_a+1) % len(cycles[cycle_a])], cycles[cycle_a][pos_b - 1]
            else:
                a_n, b_n = cycles[cycle_a][pos_a - 1], cycles[cycle_a][(pos_b+1) % len(cycles[cycle_a])]
            if pos_c > pos_d:
                c_n, d_n = cycles[cycle_c][(pos_c+1) % len(cycles[cycle_c])], cycles[cycle_c][pos_d - 1]
            else:
                c_n, d_n = cycles[cycle_c][pos_c - 1], cycles[cycle_c][(pos_d+1) % len(cycles[cycle_c])]

            if pos_b - 1 != pos_a or pos_d - 1 != pos_c:
                return None

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

        elif move.type.lower() == 'v':
            a, b = move.nodes

            cycle_a, pos_a = self._get_node_info(a)
            cycle_b, pos_b = self._get_node_info(b)

            if verbose:
                print(f"a: {a} @ {cycle_a}, {pos_a}\tb: {b} @ {cycle_b}, {pos_b}")
                print(f"{cycles[cycle_a][pos_a - 1]} <- a -> {cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])]}")
                print(f"{cycles[cycle_b][pos_b - 1]} <- b -> {cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])]}")

            if cycle_a != cycle_b or not (-1 <= pos_a - pos_b <= 1):
                # print("+", end="")
                a_pre = self.data[cycles[cycle_a][pos_a - 1], a] + \
                        self.data[cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], a]
                b_pre = self.data[cycles[cycle_b][pos_b - 1], b] + \
                        self.data[cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])], b]

                a_post = self.data[cycles[cycle_a][pos_a - 1], b] + \
                         self.data[cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], b]
                b_post = self.data[cycles[cycle_b][pos_b - 1], a] + \
                         self.data[cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])], a]

                if verbose:
                    print("non-adjacent")
                    print(f"a_pre: {self.data[cycles[cycle_a][pos_a - 1], a]} + {self.data[cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], a]} = {a_pre}")
                    print(f"b_pre: {self.data[cycles[cycle_b][pos_b - 1], b]} + {self.data[cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])], b]} = {b_pre}")
                    print(f"a_post: {self.data[cycles[cycle_a][pos_a - 1], b]} + {self.data[cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], b]} = {a_post}")
                    print(f"b_post: {self.data[cycles[cycle_b][pos_b - 1], a]} + {self.data[cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])], a]} = {b_post}")

            else:   # a and b are next to each other
                # print("-", end="")
                if pos_a > pos_b:
                    a, b = b, a
                    pos_a, pos_b = pos_b, pos_a
                a_pre = self.data[cycles[cycle_a][pos_a - 1], a]
                b_pre = self.data[cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])], b]
                a_post = self.data[cycles[cycle_a][pos_a - 1], b]
                b_post = self.data[cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])], a]

                if verbose:
                    print("adjacent")
                    print(f"a_pre: {a_pre}\tb_pre: {b_pre}\tsum: {a_pre + b_pre}")
                    print(f"a_post: {a_post}\tb_post: {b_post}\tsum: {a_post + b_post}")

            delta = a_post + b_post - a_pre - b_pre
            if verbose:
                print(f"delta: {delta}")
            return delta

        else:
            raise ValueError('Unknown move type')

        # position in cycle or node id?

    def _sort_moves(self, calculate_delta=False):
        """ sort self.moves by their improvement - delta, and old moves by what's moved """
        # ??? old moves by what's moved
        if calculate_delta:
            for im, m in enumerate(self.moves):
                self.moves[im].delta = self._get_move_delta(m)
        else:
            for im, m in enumerate(self.moves[:10]):
                self.moves[im].delta = self._get_move_delta(m)

        self.moves = sorted(self.moves, key=lambda x: x.delta or 0)

    def execute_best_move(self):
        # remove invalid moves
        self.moves = [m for m in self.moves if m.delta is not None]
        self._sort_moves(calculate_delta=True)

        while len(self.moves) and self.moves[0].delta < 0:
            best_move = self.moves.pop(0)
            if (d := self._get_move_delta(best_move, verbose=False)) < 0:  # check again
                # if d != best_move.delta:
                #     print(f"unexpected delta: {d} != (expected) {best_move.delta}")
                # print(f"E: {best_move.nodes}; d={d}")
                # print(f"\nE: {best_move.nodes}; d={d}")
                self._execute_move(best_move)
                return 0
            # else:
            #     print("% ", end="")
            #     print(f'Invalid move: {best_move.nodes}; expected delta: {best_move.delta}, actual: {d}')
        return -1

    def _execute_move(self, move):
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

            # if pos_a > pos_b:
            #     a, b = b, a
            #     pos_a, pos_b = pos_b, pos_a
            # # if pos_c > pos_d:
            #     c, d = d, c
            #     pos_c, pos_d = pos_d, pos_c

            if cycle_a == cycle_c:
                if pos_a > pos_c:
                    a, b, c, d = c, d, a, b
                    pos_a, pos_b, pos_c, pos_d = pos_c, pos_d, pos_a, pos_b

                if pos_a > pos_b:
                    a_n, b_n = cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], cycles[cycle_a][pos_b - 1]
                else:
                    a_n, b_n = cycles[cycle_a][pos_a - 1], cycles[cycle_a][(pos_b + 1) % len(cycles[cycle_a])]
                if pos_c > pos_d:
                    c_n, d_n = cycles[cycle_c][(pos_c + 1) % len(cycles[cycle_c])], cycles[cycle_c][pos_d - 1]
                else:
                    c_n, d_n = cycles[cycle_c][pos_c - 1], cycles[cycle_c][(pos_d + 1) % len(cycles[cycle_c])]

                next = max(pos_c, pos_d) + 1
                if next == len(cycles[cycle_a]):
                    cycles[cycle_a][pos_a:] = np.flipud(cycles[cycle_a][pos_a:])
                else:
                    cycles[cycle_a][pos_a:next] = np.flipud(cycles[cycle_a][pos_a:next])

            else:
                # prev_a = min(pos_a, pos_b) - 1
                # prev_c = min(pos_c, pos_d) - 1
                # next_a = (max(pos_a, pos_b) + 1) % len(cycles[cycle_a])
                # next_c = (max(pos_c, pos_d) + 1) % len(cycles[cycle_c])

                if pos_a > pos_b:
                    a_n, b_n = cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])], cycles[cycle_a][pos_b - 1]
                else:
                    a_n, b_n = cycles[cycle_a][pos_a - 1], cycles[cycle_a][(pos_b + 1) % len(cycles[cycle_a])]
                if pos_c > pos_d:
                    c_n, d_n = cycles[cycle_c][(pos_c + 1) % len(cycles[cycle_c])], cycles[cycle_c][pos_d - 1]
                else:
                    c_n, d_n = cycles[cycle_c][pos_c - 1], cycles[cycle_c][(pos_d + 1) % len(cycles[cycle_c])]

                cycles[cycle_a][pos_a], cycles[cycle_a][pos_b], cycles[cycle_c][pos_c], cycles[cycle_c][pos_d] = \
                    c, d, a, b
                self._add_moves_with_edge(cycles[cycle_a][pos_b],
                                          b_n)
                self._add_moves_with_edge(c_n,
                                          cycles[cycle_c][pos_c])

            # add new possible moves to the list
            self._add_moves_with_edge(a_n,
                                      cycles[cycle_a][pos_a])
            self._add_moves_with_edge(cycles[cycle_c][pos_d],
                                      d_n)

            self._update_deltas_from_nodes([a, b, c, d,
                                            a_n, b_n, c_n, d_n])

        elif move.type.lower() == 'v':
            # print('v', end="")
            a, b = move.nodes

            cycle_a, pos_a = self._get_node_info(a)
            cycle_b, pos_b = self._get_node_info(b)

            cycles[cycle_a][pos_a], cycles[cycle_b][pos_b] = b, a

            # add new possible moves to the list
            # moves with (a-1), a
            # moves with (a+1), a
            # moves with (b-1), b
            # moves with (b+1), b
            self._add_moves_with_edge(cycles[cycle_a][pos_a - 1],
                                      cycles[cycle_a][pos_a])
            self._add_moves_with_edge(cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])],
                                      cycles[cycle_a][pos_a])
            self._add_moves_with_edge(cycles[cycle_b][pos_b - 1],
                                      cycles[cycle_b][pos_b])
            self._add_moves_with_edge(cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])],
                                      cycles[cycle_b][pos_b])

            self._update_deltas_from_nodes([a, b,
                                            cycles[cycle_a][pos_a - 1],
                                            cycles[cycle_a][(pos_a + 1) % len(cycles[cycle_a])],
                                            cycles[cycle_b][pos_b - 1],
                                            cycles[cycle_b][(pos_b + 1) % len(cycles[cycle_b])]])

    def _add_moves_with_edge(self, a, b):
        edges = []
        for ic, cycle in enumerate([self.left, self.right]):
            edges += [(cycle[i - 1], cycle[i]) for i, _ in enumerate(cycle) if cycle[i - 1] != a and cycle[i] != b]

        self.moves += [Move(type="e", nodes=((a, b), x)) for x in edges]

    def _update_deltas_from_nodes(self, nodes):
        for im, move in enumerate(self.moves):
            if type(move.nodes[0]) == int:
                for node in nodes:
                    if move.nodes[0] == node or move.nodes[1] == node:
                        self.moves[im].delta = self._get_move_delta(move)
                        break
            else:
                for node in nodes:
                    # if type(move.nodes[0]) == int and (move.nodes[0] == node or move.nodes[1] == node):
                    #     self.moves[im].delta = self._get_move_delta(move)
                    #     break

                    if move.nodes[0][0] == node or move.nodes[0][1] == node \
                            or move.nodes[1][0] == node or move.nodes[1][1] == node:
                        # if move.nodes[0] == node or move.nodes[1] == node \
                        #         or move.nodes[0][0] == node or move.nodes[0][1] == node \
                        #         or move.nodes[1][0] == node or move.nodes[1][1] == node:
                        self.moves[im].delta = self._get_move_delta(move)
                        break
