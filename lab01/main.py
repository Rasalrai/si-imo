import os.path

from instance_reader import InstanceReader
from lab01.algorithms.greedy_nn import GreedyNNAlgorithm
from lab01.algorithms.random import RandomAlgorithm

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

    # random algorithm
    random_alg = RandomAlgorithm(nodes)
    random_alg.run()
    # random_alg.solution.plot(problem.points, show=False)
    print(f"Random cycles lengths: {random_alg.solution.length()}")

    # greedy NN
    greedy_nn_alg = GreedyNNAlgorithm(nodes)

    for start_node in range(10):
        greedy_nn_alg.run(start_node)
        greedy_nn_alg.solution.plot(problem.points, show=False)
        print(f"Greedy NN cycles lengths: {greedy_nn_alg.solution.length()}")
