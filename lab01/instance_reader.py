from math import sqrt

import numpy as np


# helper functions

def _get_distance(n1, n2):
    return sqrt(
        (n1[0] - n2[0]) * (n1[0] - n2[0]) +
        (n1[1] - n2[1]) * (n1[1] - n2[1])
    )


class InstanceReader:
    def __init__(self, filename, size=100):
        self.filename: str = filename
        self.nodes = []
        self.size = size
        self.matrix = np.ndarray(shape=(size, size), dtype=int)

        self.read_nodes()

    def read_nodes(self):
        DESC_LINES = 6  # Number of description lines in file that we ignore

        with open(self.filename, 'r') as f:
            for _ in range(DESC_LINES):
                f.readline()
            while (l := f.readline()) != "EOF\n":
                self.nodes.append(tuple([int(x) for x in l.split(" ")[-2:]]))

    def get_matrix(self) -> np.ndarray:
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                self.matrix[i, j] = _get_distance(self.nodes[i], self.nodes[j]) + .5

        return self.matrix
