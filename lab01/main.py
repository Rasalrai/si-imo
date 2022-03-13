import os.path

import numpy as np

from instance_reader import InstanceReader
from lab01.algorithms.greedy_nn import GreedyNNAlgorithm
from lab01.algorithms.greedy_cycle import GreedyCycleAlgorithm
from lab01.algorithms.regret import RegretAlgorithm
from lab01.algorithms.random import RandomAlgorithm


if __name__ == '__main__':
    for problem_file in ("kroA100.tsp", "kroB100.tsp"):
        print(f"\n\n--- {problem_file} ---")
        problem = InstanceReader(os.path.join("data", problem_file))
        nodes = problem.matrix

        # # # random algorithm
        # random_alg = RandomAlgorithm(nodes)
        # results = []
        # best_result, best_solution, best_start = np.inf, None, -1
        # for _ in range(100):
        #     random_alg.run()
        #     l = sum(random_alg.solution.length())
        #     results.append(l)
        #     if l < best_result:
        #         best_result, best_solution = l, random_alg.solution
        # best_solution.plot(problem.points, f"{random_alg.__class__.__name__}: best result for {problem_file}", show=True)
        #
        # print(f"algorithm: {random_alg.__class__.__name__}\n\tbest: {min(results)}\n\tworst: {max(results)}\n\tavg: {sum(results)/len(results)}")

        algorithms = [
            GreedyNNAlgorithm(nodes),
            GreedyCycleAlgorithm(nodes),
            RegretAlgorithm(nodes),
        ]

        best = []

        for algorithm in algorithms:
            results = []
            best_result, best_solution, best_start = np.inf, None, -1
            for start_node in range(100):
                algorithm.run(start_node)
                l = sum(algorithm.solution.length())
                results.append(l)
                if l < best_result:
                    best_result, best_solution = l, algorithm.solution
                    best_start = start_node

            best.append([best_solution, best_start])
            best_solution.plot(problem.points, f"{algorithm.__class__.__name__}: best result for {problem_file}", show=True)

            print(f"algorithm: {algorithm.__class__.__name__}\n\tbest: {min(results)}\n\tworst: {max(results)}\n\tavg: {sum(results)/len(results)}")
