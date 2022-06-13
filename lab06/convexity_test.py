import os
from copy import deepcopy
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

from lab02.algorithms.greedy_local import GreedyLocal
from lab02.algorithms.random import RandomAlgorithm
from lab02.instance_reader import InstanceReader


def similarity_nodes(s1, s2):
    similarities = [len(np.intersect1d(a, b)) for a in (s1.left_i, s1.right_i) for b in (s2.left_i, s2.right_i)]
    return sum(s1.length()), (max(similarities[:2]) + max(similarities[2:])) / 200


def similarity_edges(s1, s2):
    edges = [np.empty(100, dtype=str) for _ in range(4)]
    for i, cycle in enumerate((s1.left_i, s1.right_i, s2.left_i, s2.right_i)):
        # edges[i][:, 0] = cycle
        # edges[i][:, 1] = np.roll(cycle, -1)
        rolled = np.roll(cycle, -1)
        edges[i] = np.array([
            f"{cycle[j]}-{rolled[j]}"
            for j in range(len(cycle))
        ])
    similarities = [len(np.intersect1d(a, b)) for a in edges[:2] for b in edges[2:]]
    return sum(s1.length()), (max(similarities[:2]) + max(similarities[2:])) / 200


if __name__ == '__main__':
    problem_files = [
        # "kroA200.tsp",
        "kroB200.tsp",
    ]
    iter = 500 # 1000
    all_solutions = []

    for f in problem_files:
        print(f"\n\n--- {f} ---")
        problem = InstanceReader(os.path.join("data", f))
        nodes = problem.matrix
        best_sol = None
        solutions = []

        for i in range(iter):
            t0 = perf_counter()
            rand_sol = RandomAlgorithm(nodes).run()
            greedy_sol = GreedyLocal("edges", rand_sol.left_i, rand_sol.right_i, nodes).run()

            if best_sol is None or sum(greedy_sol.length()) < sum(best_sol.length()):
                best_sol = deepcopy(greedy_sol)
            solutions.append(deepcopy(greedy_sol))
            # print(perf_counter() - t0, end="\t")
            print(".", end="")

        all_solutions.append(deepcopy(solutions))

        # calculate the two similarity metrics
        print("\n")
        nodes_similarity = np.empty((iter, 2))  # x, y
        edges_similarity = np.empty((iter, 2))  # x, y
        for i, s in enumerate(solutions):
            # shared nodes
            nodes_similarity[i] = similarity_nodes(s, best_sol)
            # print(f"{i}: {nodes_similarity[i]}")

            # shared edges
            edges_similarity[i] = similarity_edges(s, best_sol)

        # plot
        plt.scatter(nodes_similarity[:, 0], nodes_similarity[:, 1])
        plt.xlabel("cycles length")
        plt.ylabel("shared nodes")
        plt.title(f"{f} - nodes similarity")
        plt.savefig(f"results/{f}_nodes_similarity.png")
        plt.close()

        plt.scatter(edges_similarity[:, 0], edges_similarity[:, 1])
        plt.xlabel("cycles length")
        plt.ylabel("shared edges")
        plt.title(f"{f} - edges similarity")
        plt.savefig(f"results/{f}_edges_similarity.png")
        plt.close()

        # correlation
        print(f"nodes similarity correlation: {np.corrcoef(nodes_similarity[:, 0], nodes_similarity[:, 1])[0, 1]}")
        print(f"edges similarity correlation: {np.corrcoef(edges_similarity[:, 0], edges_similarity[:, 1])[0, 1]}")

