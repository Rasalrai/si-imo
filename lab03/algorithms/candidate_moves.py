from time import perf_counter

import numpy as np

from lab01.algorithms.algorithm import Algorithm
from lab02.solution import Solution
from lab02.algorithms.local_algorithm import LocalAlgorithm


class CandidateMovesAlgorithm(Algorithm):
    def __init__(self, data, left, right, n_neigh=10, time_limit=300):
        super().__init__(data)
        # get neighbours for each node
        self.left = left.copy()
        self.right = right.copy()
        self.neighbours = self.get_neighbours(n_neigh)

        self.time_limit = time_limit

    def get_neighbours(self, neighbours_count):
        neighbours = np.empty(shape=(self.data.shape[0], neighbours_count))
        for i, nbh in enumerate(self.data):
            neighbours[i] = nbh.argsort()[1:neighbours_count + 1]

        return neighbours

    def run(self) -> Solution:
        size = len(self.left)
        cycles = [self.left, self.right]

        # wrap this in something? add exit condition
        time1 = perf_counter()

        while perf_counter() - time1 < self.time_limit:
            move_done = False
            for ic, cycle in enumerate(cycles):
                for i, node in enumerate(cycle):
                    for j, nbh in enumerate(self.neighbours[node]):
                        # add an edge to the neighbour
                        if nbh not in cycle:
                            ni = np.argwhere(cycles[ic - 1] == nbh)[0][0]
                            len_before = self.data[cycle[i - 2]][cycle[i - 1]] + self.data[cycle[i - 1]][cycle[i]]
                            len_after = self.data[cycle[i - 2]][ni] + self.data[ni][cycle[i]]
                            if len_after < len_before:
                                # swap the neighbour and a node before (or after) the current node
                                cycles[ic - 1][ni] = cycle[i - 1]
                                cycle[i - 1] = nbh
                                move_done = True

                            # get length of i-2 - i+2
                            # find the best placement
                        else:
                            ni = np.argwhere(cycle == nbh)[0][0]
                            na, nb = (i, ni) if i < ni else (ni, i)
                            len_before = self.data[cycle[(na - 1) % size]][cycle[na % size]] + \
                                         self.data[cycle[nb % size]][cycle[(nb + 1) % size]]
                            len_after = self.data[cycle[(na - 1 % size)]][cycle[nb % size]] + \
                                        self.data[cycle[na % size]][cycle[(nb + 1) % size]]
                            if len_after < len_before:
                                # swap nodes between i and neighbour
                                if nb == len(cycle) - 1:
                                    cycles[ic][na:] = np.flipud(cycle[na:])
                                else:
                                    cycles[ic][na:nb + 1] = np.flipud(cycle[na:nb + 1])
                                move_done = True
            if not move_done:
                break

        self.solution = Solution(self.data, *cycles)
        return self.solution

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
