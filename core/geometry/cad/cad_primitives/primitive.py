from abc import ABC, abstractmethod

class CADPrimitive(ABC):

    @abstractmethod
    def __init__(self, center=(0,0,0)):
        self.center = center
    
    @abstractmethod
    def to_geometry(self):
        pass
