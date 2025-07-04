
from abc import ABC, abstractmethod

class Tracker(ABC):
    @abstractmethod
    def log_entry(self, data):
        pass

    @abstractmethod
    def view_entries(self):
        pass
