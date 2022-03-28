import os
import numpy as np

from time import perf_counter

from instance_reader import InstanceReader
from lab02.algorithms.greedy_nn import GreedyNNAlgorithm
from lab02.algorithms.random import RandomAlgorithm
from lab02.algorithms.random_local import RandomLocal
from lab02.algorithms.greedy_local import GreedyLocal
from lab02.algorithms.steepest_local import SteepestLocal

if __name__ == '__main__':
    t0 = perf_counter()
    for problem_file in ("kroA100.tsp", "kroB100.tsp"):
        print(f"\n\n--- {problem_file} ---")
        problem = InstanceReader(os.path.join("data", problem_file))
        nodes = problem.matrix

        results = []
        best_result, best_solution = np.inf, None

        algorithms = {
            "GreedyEdges": (GreedyLocal, {"variant": "edges", "data": nodes}),
            "GreedyVert": (GreedyLocal, {"variant": "vertices", "data": nodes}),
            "SteepestEdges": (SteepestLocal, {"variant": "edges", "data": nodes}),
            "SteepestVert": (SteepestLocal, {"variant": "vertices", "data": nodes}),
            "RandomEdges": (RandomLocal, {"variant": "edges", "data": nodes}),
            "RandomVert": (RandomLocal, {"variant": "vertices", "data": nodes}),
        }

        base_greedy_algorithm = GreedyNNAlgorithm(nodes)
        random_base = RandomAlgorithm(nodes)

        for base_alg, base_str in zip((base_greedy_algorithm, random_base), ("from heur", "from random")):
            res = {k: [] for k in algorithms.keys()}  # all results
            times = {k: [] for k in algorithms.keys()}  # all times
            best_results = {k: np.inf for k in algorithms.keys()}
            best_solutions = {k: None for k in algorithms.keys()}

            if base_str == "from heur":
                iter, time_limit = 50, 1.8
            else:
                iter, time_limit = 20, 9

            for i in range(iter):
                base_alg.run(2*i+1)

                for k, v in algorithms.items():
                    alg = v[0](**v[1],
                               data_l=base_alg.solution.left_i,
                               data_r=base_alg.solution.right_i)
                    alg.set_time_limit(time_limit)
                    t1 = perf_counter()
                    alg.run()
                    times[k].append(perf_counter() - t1)
                    res[k].append(l := sum(alg.solution.length()))
                    if l < best_results[k]:
                        best_results[k], best_solutions[k] = l, alg.solution

                # get results
            print(f"\n\n{base_str.upper()}")
            for k, v in best_solutions.items():
                v.plot(problem.points, f"{k} - {problem_file} ({base_str})", show=False, save=True)

            print("RESULTS\nalgorithm\tbest\tworst\tavg")
            for k, v in res.items():
                print(f"{k}\t{min(v)}\t{max(v)}\t{sum(v) / len(v)}")

            print("TIME\nalgorithm\tbest\tworst\tavg")
            for k, v in times.items():
                print(f"{k}\t{min(v):.5f}\t{max(v):.5f}\t{(sum(v) / len(v)):.5f}")

    print(f"\nTIME: {perf_counter() - t0}")
