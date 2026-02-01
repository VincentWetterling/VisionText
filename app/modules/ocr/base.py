from abc import ABC, abstractmethod

class OCRBase(ABC):
    @abstractmethod
    def run(self, image):
        pass
