import os
import numpy as np

from time import perf_counter

from lab01.instance_reader import InstanceReader
from lab01.algorithms.greedy_nn import GreedyNNAlgorithm
from lab02.algorithms.steepest_local import SteepestLocal


if __name__ == '__main__':
    problem_files = ["kroA200", "kroB200"]
    algorithms = {
        "Improving Moves": (),
        "Candidate Moves": (),
    }

    # problem = InstanceReader(os.path.join("data", problem_file))
    # nodes = problem.matrix

    # get initial solution
    # greedy_nn_solution

    # get solution after local search
    # "SteepestEdges": (SteepestLocal, {"variant": "edges", "data": nodes}),

    # new algorithms
