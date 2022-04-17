import numpy as np


class Move:
    def __init__(self, delta: float, move: tuple, where: tuple):
        self.delta = delta
        self.move = move
        self.where = where

    def is_valid(self, left, right):
        # possible results:
        #  1: move is possible
        # -1: move is not possible now, but possible in the future
        # 0: edges don't exist anymore - assume never possible

        raise NotImplementedError()
