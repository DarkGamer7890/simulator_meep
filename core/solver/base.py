from abc import ABC, abstractmethod

class BaseSolver(ABC):

    @abstractmethod
    def run(self):
        pass


# WHY: abstracting solver allows backend swap without touching UI/plotter
