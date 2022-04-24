import numpy as np


class Move:
    def __init__(self, type: str, nodes: tuple):
        self.type = type    # 'e' or 'v'
        self.nodes = nodes  # a pair of edges (tuples) or vertices (ints)
        self.delta = None   # the change in the graph
