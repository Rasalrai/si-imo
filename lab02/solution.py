import numpy as np
import matplotlib.pyplot as plt


class Solution:
    def __init__(self, matrix, l, r):
        self.matrix = matrix
        # indices of subsequent nodes in left and right cycles
        self.left_i = l
        self.right_i = r

        self.distances = self.get_nodes_distances()

    def get_nodes_distances(self):
        size = self.matrix.shape[0]
        left = np.ndarray(shape=(size // 2), dtype=np.int)
        right = np.empty_like(left)
        for distances, nodes in zip((left, right), (self.left_i, self.right_i)):
            for i, n in enumerate(nodes):
                if i == 0:
                    distances[i] = self.matrix[n, nodes[-1]]
                    continue
                distances[i] = self.matrix[nodes[i - 1], n]

        return left, right

    def length(self):
        """ Return lengths of left and right cycles"""
        return [d.sum() for d in self.distances]

    def plot(self, points, title="", show=True):
        """ Create a matplotlib visualization of the solution """
        # points for plotting - add the first point at the end to close the cycle
        left_pts = np.array([points[i] for i in self.left_i] + [points[self.left_i[0]]])
        right_pts = np.array([points[i] for i in self.right_i] + [points[self.right_i[0]]])

        fig, ax = plt.subplots()
        ax.plot(left_pts[:, 0], left_pts[:, 1], 'o-', color='red')
        ax.plot(right_pts[:, 0], right_pts[:, 1], 'o-', color='blue')

        ax.set_title(title)

        if show:
            plt.show()
