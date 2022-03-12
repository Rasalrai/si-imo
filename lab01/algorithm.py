from abc import ABC, abstractmethod

import numpy as np


class Algorithm(ABC):
    def __init__(self, data: np.ndarray):
        self.data = data
        self.solution = None
        # super().__init__()

    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")
