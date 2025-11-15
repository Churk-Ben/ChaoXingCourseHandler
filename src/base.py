from abc import ABC, abstractmethod


class PluginBase(ABC):
    @abstractmethod
    def run(self):
        pass
