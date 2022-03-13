import os.path

from instance_reader import InstanceReader
from lab01.algorithms.greedy_nn import GreedyNNAlgorithm
from lab01.algorithms.greedy_cycle import GreedyCycleAlgorithm
# from lab01.algorithms.regret import RegretAlgorithm
from lab01.algorithms.random import RandomAlgorithm

# TODOs:
#  algorithms
#    random - as baseline       DONE
#    greedy nearest neighbor algorithm  DONE
#    greedy cycle expansion algorithm   DONE
#    regret-based heuristic (2-regret)
#  other
#    solution visualization     DONE
#    solution statistics?

if __name__ == '__main__':
    problem = InstanceReader(os.path.join("data", "kroA100.tsp"))
    nodes = problem.matrix

    # # random algorithm
    # random_alg = RandomAlgorithm(nodes)
    # random_alg.run()
    # # random_alg.solution.plot(problem.points, show=False)
    # print(f"Random cycles lengths: {random_alg.solution.length()}")

    algoritms = [
        # GreedyNNAlgorithm(nodes),
        GreedyCycleAlgorithm(nodes),
        # RegretAlgorithm(nodes),
    ]

    for algorithm in algoritms:
        for start_node in range(15):
            algorithm.run(start_node)
            algorithm.solution.plot(problem.points, show=True)
            print(f"Greedy NN cycles lengths: {algorithm.solution.length()}")
