from abc import ABC, abstractmethod


class GeometryBuilder(ABC):

    @abstractmethod
    def build(self):
        #return: list[GeometryPrimitive]
        pass
