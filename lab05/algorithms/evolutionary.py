import random
from copy import deepcopy
from time import perf_counter

import numpy as np

from lab02.algorithms.algorithm import Algorithm
from lab02.algorithms.greedy_nn import GreedyNNAlgorithm
from lab02.solution import Solution


########################################################################################################################
# better regret

def delta_insert(cities, path, i, city):
    a, b = path[i - 1], path[i]
    return cities[a, city] + cities[city, b] - cities[a, b]


def solve_regret_init(cities, paths, remaining):
    t0 = perf_counter()
    while remaining:
        for path in paths:
            if not remaining:
                break
            scores = np.array([[delta_insert(cities, path, i, v) for i in range(len(path))] for v in remaining])
            if scores.shape[1] == 1:
                best_city_idx = np.argmin(scores)
            else:
                regret = np.diff(np.partition(scores, 1)[:, :2]).reshape(-1)
                weight = regret - 0.37 * np.min(scores, axis=1)
                best_city_idx = np.argmax(weight)

            best_city = remaining[best_city_idx]
            best_insert = np.argmin(scores[best_city_idx])
            path.insert(best_insert, best_city)
            remaining.remove(best_city)
    return perf_counter() - t0, paths

########################################################################################################################


class EvolutionaryAlgorithm(Algorithm):
    def __init__(self, data, time_limit=30, do_local_search=False):
        super().__init__(data)
        self.population_size = 15
        self.time_limit = time_limit
        self.do_local_search = do_local_search

        self.mutation_probability = 0.1

    def run(self):
        t0 = perf_counter()

        population = self.pop_gen(50)
        population_results = np.array([sum(Solution(self.data, p.left_i, p.right_i).length()) for p in population],
                                      dtype=float)

        best_id = np.argmin(population_results)

        while perf_counter() - t0 < self.time_limit:
            # generate a new offspring
            parents_ids = random.sample(range(self.population_size), 2)
            parents = [population[i] for i in parents_ids]

            # generate a new child
            child = Solution(self.data, *self.crossover(parents))

            # evaluate the offspring
            child_length = sum(child.length())
            worst_id = np.argmax(population_results)
            if child_length < population_results[worst_id]:
                population[worst_id] = child
                population_results[worst_id] = child_length
            if child_length < population_results[best_id]:
                best_id = best_id

        self.solution = population[best_id]
        return population[best_id]

    # def generate_individual(self):
    #     rnd = RandomAlgorithm(self.data).run()
    #     # g = GreedyNNAlgorithm(self.data)

    def pop_gen(self, n=None):
        g = GreedyNNAlgorithm(self.data)
        pop = [g.run(x) for x in random.sample(range(200), n or self.population_size)]
        if n > self.population_size:
            lengths = np.array([sum(Solution(self.data, p.left_i, p.right_i).length()) for p in pop])
            results = np.array(lengths, dtype=float).argsort()
            ids = results[results < self.population_size]

            return [pop[x] for x in ids]

        return pop

    def crossover(self, parents):
        s1, s2 = deepcopy(parents[0]), deepcopy(parents[1])
        sol1, sol2 = [[s.left_i, s.right_i] for s in [s1, s2]]

        remaining = []
        for cyc1 in sol1:
            n = len(cyc1)
            if n == 1:
                continue
            for i in range(n):
                p, q = cyc1[i], cyc1[(i + 1) % n]
                if p == -1 or q == -1 or p == q:
                    continue
                found = False
                for cyc2 in sol2:
                    m = len(cyc2)
                    for j in range(m):
                        u, v = cyc2[j], cyc2[(j + 1) % m]
                        if (p == u and q == v) or (p == v and q == u):
                            found = True
                            break
                    if found:
                        break

                if not found:
                    remaining.append(cyc1[i])
                    remaining.append(cyc1[(i + 1) % n])
                    cyc1[i] = -1
                    cyc1[(i + 1) % n] = -1

            for i in range(1, n):
                x, y, z = cyc1[(i - 1) % n], cyc1[i], cyc1[(i + 1) % n]
                if x == z == -1 and y != -1:
                    remaining.append(y)
                    cyc1[i] = -1

            for i in range(1, n):
                x = cyc1[i]
                if x != -1 and np.random.rand() < 0.2:
                    remaining.append(x)
                    cyc1[i] = -1

        a = [x for x in sol1[0] if x != -1]
        b = [x for x in sol1[1] if x != -1]
        assert len(a) + len(b) + len(remaining) == 200
        return solve_regret_init(self.data, (a, b), remaining)[1]
