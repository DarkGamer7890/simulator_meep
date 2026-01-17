from abc import ABC, abstractmethod

class CADPrimitive(ABC):

    @abstractmethod
    def __init__(self, center=(0,0,0)):
        self.center = center
    
    @abstractmethod
    def to_geometry(self):
        pass

    @abstractmethod
    def get_properties(self) -> dict:
        return {}
    
    # @abstractmethod
    def set_property(self, name, value):
        if not hasattr(self, name):
            raise AttributeError(f"No property {name}")
        setattr(self, name, value)

    

