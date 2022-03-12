import os.path

from instance_reader import InstanceReader
from random_algorithm import RandomAlgorithm
from solution import Solution

# TODOs:
#  algorithms
#    random - as baseline       DONE
#    greedy nearest neighbor algorithm
#    greedy cycle expansion algorithm
#    regret-based heuristic (2-regret)
#  other
#    solution visualization     DONE
#    solution statistics?

if __name__ == '__main__':
    problem = InstanceReader(os.path.join("data", "kroA100.tsp"))
    nodes = problem.matrix
    # print(nodes[0, :10])

    # random algorithm
    random_alg = RandomAlgorithm(nodes)
    random_alg.run()

    random_alg.solution.plot(problem.points, show=True)
    print(f"Random cycles lengths: {random_alg.solution.length()}")
