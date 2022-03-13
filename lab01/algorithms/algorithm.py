from abc import ABC, abstractmethod

import numpy as np

from lab01.solution import Solution


class Algorithm(ABC):
    def __init__(self, data: np.ndarray):
        self.data = data
        self.solution = None
        # super().__init__()

    @abstractmethod
    def run(self, *args, **kwargs) -> Solution:
        raise NotImplementedError("Subclass must implement abstract method")
