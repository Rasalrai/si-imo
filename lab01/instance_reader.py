from math import sqrt

import numpy as np


# helper functions
def _get_distance(n1, n2):
    return sqrt(
        (n1[0] - n2[0]) * (n1[0] - n2[0]) +
        (n1[1] - n2[1]) * (n1[1] - n2[1])
    )


class InstanceReader:
    def __init__(self, filename):
        self.filename: str = filename
        self.size: int = 0
        self.points = None
        self.matrix = None

        self._read_nodes()
        self._get_matrix()

    def _read_nodes(self):
        DESC_LINES = 6  # Number of description lines in file that we ignore
        points = []

        with open(self.filename, 'r') as f:
            for _ in range(DESC_LINES):
                l = f.readline().split(" ")
                if l[0] == "DIMENSION:":
                    self.size = int(l[1])

            while (l := f.readline()) != "EOF\n":
                points.append([int(x) for x in l.split(" ")[-2:]])
            self.points = np.array(points)

        self.matrix = np.ndarray(shape=(self.size, self.size), dtype=int)

    def _get_matrix(self) -> np.ndarray:
        for i in range(len(self.points)):
            self.matrix[i, i] = 0
            for j in range(i + 1, len(self.points)):
                self.matrix[i, j] = self.matrix[j, i] = _get_distance(self.points[i], self.points[j]) + .5

        return self.matrix
