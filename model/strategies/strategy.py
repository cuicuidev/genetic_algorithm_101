from abc import ABC, abstractmethod

class Strategy(ABC):

    @abstractmethod
    def apply(self):
        pass