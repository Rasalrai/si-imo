import os
import numpy as np

from time import perf_counter

from instance_reader import InstanceReader
from lab02.algorithms.greedy_nn import GreedyNNAlgorithm
from lab02.algorithms.random import RandomAlgorithm
from lab02.algorithms.greedy_local import GreedyLocal
from lab02.algorithms.steepest_local import SteepestLocal


if __name__ == '__main__':
    t1 = perf_counter()
    for problem_file in ("kroA100.tsp", "kroB100.tsp"):
        print(f"\n\n--- {problem_file} ---")
        problem = InstanceReader(os.path.join("data", problem_file))
        nodes = problem.matrix

        # # random algorithm
        # random_alg = RandomAlgorithm(nodes)
        base_algorithm = GreedyNNAlgorithm(nodes)
        # TODO adjust main function for testing
        # TODO add random local search for benchmark
        results = []
        best_result, best_solution = np.inf, None

        algorithms = {
            "GreedyEdges": (GreedyLocal, {"variant": "edges", "data": nodes}),
            "GreedyVert": (GreedyLocal, {"variant": "vertices", "data": nodes}),
            "SteepestEdges": (SteepestLocal, {"variant": "edges", "data": nodes}),
            "SteepestVert": (SteepestLocal, {"variant": "vertices", "data": nodes}),
        }
        res = {k: [] for k in algorithms.keys()}
        best_result_greedy = {k: np.inf for k in algorithms.keys()}
        best_solution_greedy = {k: None for k in algorithms.keys()}

        # to adjust no. of iterations on Windows - change the second value :)
        for j in range(100 if os.name == "posix" else 2):
            # print("=====", j, "=====")
            if not j % 10: print(".", end="")
            base_algorithm.run(j)
            results.append(l := sum(base_algorithm.solution.length()))

            if l < best_result:
                best_result, best_solution = l, base_algorithm.solution
            for k, v in algorithms.items():
                alg = v[0](**v[1],
                           data_l=base_algorithm.solution.left_i,
                           data_r=base_algorithm.solution.right_i)
                alg.run()
                l = sum(alg.solution.length())
                res[k].append(l)
                if l < best_result_greedy[k]:
                    best_result_greedy[k], best_solution_greedy[k] = l, alg.solution
        best_solution.plot(problem.points, f"Base solution: best result for {problem_file}", show=True)

        for k, v in best_solution_greedy.items():
            v.plot(problem.points, f"{k}: best result for {problem_file}", show=True, save=True)
        print()

        print(f"algorithm: base\n"
              f"\tbest: {min(results)}\n"
              f"\tworst: {max(results)}\n"
              f"\tavg: {sum(results) / len(results)}")

        for k, v in res.items():
            print(f"algorithm: {k}\n"
                  f"\tbest: {min(v)}\n"
                  f"\tworst: {max(v)}\n"
                  f"\tavg: {sum(v) / len(v)}")
    print(f"\nTIME: {perf_counter() - t1}")
