import os.path

import numpy as np

from instance_reader import InstanceReader
from lab02.algorithms.greedy_nn import GreedyNNAlgorithm
from lab02.algorithms.random import RandomAlgorithm
from lab02.algorithms.greedy_local import GreedyLocal
from lab02.algorithms.steepest_local import SteepestLocal


if __name__ == '__main__':
    for problem_file in ("kroA100.tsp", "kroB100.tsp"):
        print(f"\n\n--- {problem_file} ---")
        problem = InstanceReader(os.path.join("data", problem_file))
        nodes = problem.matrix

        # # random algorithm
        random_alg = RandomAlgorithm(nodes)
        # TODO adjust main function for testing
        # TODO add random local search for benchmark
        results, res = [], [[], []]
        # , , best_start = np.inf, None, -1
        best_result, best_result_greedy = np.inf, [np.inf, np.inf]
        best_solution, best_solution_greedy = None, [None, None]
        for _ in range(3):
            random_alg.run()
            local_algorithms = [
                GreedyLocal(
                    "edges",
                    random_alg.solution.left_i,
                    random_alg.solution.right_i,
                    nodes,
                ),
                GreedyLocal(
                    "vertices",
                    random_alg.solution.left_i,
                    random_alg.solution.right_i,
                    nodes,
                ),
                # SteepestLocal("edges", random_alg.solution.left_i, random_alg.solution.right_i, nodes),
                # SteepestLocal("vertices", random_alg.solution.left_i, random_alg.solution.right_i, nodes),
            ]
            l = sum(random_alg.solution.length())
            results.append(l)
            if l < best_result:
                best_result, best_solution = l, random_alg.solution
            for i, local_algorithm in enumerate(local_algorithms):
                print("=====", i, "=====")
                local_algorithm.run()
                l = sum(local_algorithm.solution.length())
                res[i].append(l)
                if l < best_result_greedy[i]:
                    best_result_greedy[i], best_solution_greedy[i] = l, local_algorithm.solution
        best_solution.plot(problem.points, f"Random: best result for {problem_file}", show=True)
        best_solution_greedy[0].plot(problem.points, f"GreedyLocal edge : best result for {problem_file}", show=True)
        best_solution_greedy[1].plot(problem.points, f"SteepestLocal edge: best result for {problem_file}", show=True)

        print(f"algorithm: Random\n\tbest: {min(results)}\n\tworst: {max(results)}\n\tavg: {sum(results)/len(results)}")
        print(f"algorithm: GreedyLocal edge\n\tbest: {min(res[0])}\n\tworst: {max(res[0])}\n\tavg: {sum(res[0])/len(res[0])}")
        print(f"algorithm: SteepestLocal edge\n\tbest: {min(res[1])}\n\tworst: {max(res[1])}\n\tavg: {sum(res[1])/len(res[1])}")

        # algorithms = [
        #     # GreedyNNAlgorithm(nodes),
        #     # GreedyCycleAlgorithm(nodes),
        #     # RandomAlgorithm(nodes),
        # ]
        #
        # best = []
        #
        # # local_algorithms = [
        # #     GreedyLocal("edges"),
        # #     GreedyLocal("vertices"),
        # #     SteepestLocal("edges"),
        # #     SteepestLocal("vertices"),
        # # ]
        #
        # for algorithm in algorithms:
        #     results = []
        #     best_result, best_solution, best_start = np.inf, None, -1
        #     for start_node in range(100):
        #         algorithm.run(start_node)
        #         l = sum(algorithm.solution.length())
        #         results.append(l)
        #         if l < best_result:
        #             best_result, best_solution = l, algorithm.solution
        #             best_start = start_node
        #
        #     # for local_algorithm in local_algorithms:
        #
        #     best.append([best_solution, best_start])
        #     best_solution.plot(problem.points, f"{algorithm.__class__.__name__}: best result for {problem_file}", show=True)
        #
        #     print(f"algorithm: {algorithm.__class__.__name__}\n\tbest: {min(results)}\n\tworst: {max(results)}\n\tavg: {sum(results)/len(results)}")
