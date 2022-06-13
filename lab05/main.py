import os
from time import perf_counter

import numpy as np

from lab01.algorithms.random import RandomAlgorithm
from lab01.instance_reader import InstanceReader
from lab05.algorithms.evolutionary import EvolutionaryAlgorithm


def get_random_solution(nodes):
    return RandomAlgorithm(nodes).run()


if __name__ == '__main__':
    problem_files = [
        # "kroA200.tsp",
        "kroB200.tsp",
    ]
    # Każdy z czterech algorytmów na każdej instancji uruchamiany 100 razy startując (lokalne
    # przeszukiwanie) z rozwiązań losowych

    for file in problem_files:
        print(f"\n\n--- {file} ---")
        problem = InstanceReader(os.path.join("data", file))
        nodes = problem.matrix

        # name: (class, run_params)
        algorithms = {

            "Custom": (EvolutionaryAlgorithm, {"time_limit": 150}),
        }

        res = {k: [] for k in algorithms.keys()}  # all results
        times = {k: [] for k in algorithms.keys()}  # all times
        best_results = {k: np.inf for k in algorithms.keys()}
        best_solutions = {k: None for k in algorithms.keys()}

        for start_node in range(10):
            # random_solution = get_random_solution(nodes)
            # print(f"start result: {sum(random_solution.length())}")

            for k, v in algorithms.items():
                # v[1]["left"] = deepcopy(random_solution.left_i)
                # v[1]["right"] = deepcopy(random_solution.right_i)

                alg = v[0](data=nodes, **v[1])

                t1 = perf_counter()
                alg.run()  # **v[1])  # start1=start_node*2)
                times[k].append(perf_counter() - t1)
                res[k].append(l := sum(alg.solution.length()))
                if l < best_results[k] and 90 < len(alg.solution.left_i) < 110:
                    best_results[k], best_solutions[k] = l, alg.solution
            print(".", end="")

        for k, v in best_solutions.items():
            v.plot(problem.points, f"{k} - {file}", show=False, save=True)

        print("\nRESULTS\nalgorithm\tbest\tworst\tavg")
        for k, v in res.items():
            print(f"{k}\t{min(v)}\t{max(v)}\t{sum(v) / len(v)}")

        print("TIME\nalgorithm\tbest\tworst\tavg")
        for k, v in times.items():
            print(f"{k}\t{min(v):.5f}\t{max(v):.5f}\t{(sum(v) / len(v)):.5f}")
