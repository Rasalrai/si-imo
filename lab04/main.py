import os
from copy import deepcopy

import numpy as np

from time import perf_counter

from lab01.instance_reader import InstanceReader
from lab01.algorithms.random import RandomAlgorithm
from lab04.algorithms.ils_destroy_repair import ILSDestroyRepair
from lab04.algorithms.ils_perturbation import ILSWithPerturbation
from lab04.algorithms.msls import MultipleStartLocalSearch

if __name__ == '__main__':
    problem_files = [
        "kroA200.tsp",
        "kroB200.tsp",
    ]

    for file in problem_files:
        print(f"\n\n--- {file} ---")
        problem = InstanceReader(os.path.join("data", file))
        nodes = problem.matrix

        tl = 1
        algorithms = {
            # "MultipleStartLocalSearch": (MultipleStartLocalSearch, {"time_limit": tl}),
            "ILSWithPerturbation": (ILSWithPerturbation, {"time_limit": tl * 100}),
            "ILSDestroyRepair": (ILSDestroyRepair, {"time_limit": tl * 100}),
        }

        res = {k: [] for k in algorithms.keys()}  # all results
        times = {k: [] for k in algorithms.keys()}  # all times
        best_results = {k: np.inf for k in algorithms.keys()}
        best_solutions = {k: None for k in algorithms.keys()}

        for start_node in range(1):     # 10
            # print(".", end="")
            print(".")
            random_solution = RandomAlgorithm(nodes).run()
            print(f"start result: {sum(random_solution.length())}")

            for k, v in algorithms.items():
                # print(k, end="\t")
                v[1]["left"] = deepcopy(random_solution.left_i)
                v[1]["right"] = deepcopy(random_solution.right_i)

                alg = v[0](data=nodes, **v[1])

                t1 = perf_counter()
                alg.run()
                times[k].append(perf_counter() - t1)
                res[k].append(l := sum(alg.solution.length()))
                print(f"{k}: {l} ({times[k][-1]} s)")
                if l < best_results[k]:
                    best_results[k], best_solutions[k] = l, deepcopy(alg.solution)

        for k, v in best_solutions.items():
            v.plot(problem.points, f"{k} - {file}", show=False, save=True)

        print("\nRESULTS\nalgorithm\tbest\tworst\tavg")
        for k, v in res.items():
            print(f"{k}\t{min(v)}\t{max(v)}\t{sum(v) / len(v)}")

        print("TIME\nalgorithm\tbest\tworst\tavg")
        for k, v in times.items():
            print(f"{k}\t{min(v):.5f}\t{max(v):.5f}\t{(sum(v) / len(v)):.5f}")
