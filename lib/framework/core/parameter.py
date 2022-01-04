from abc import ABCMeta, abstractmethod


class Parameter(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def types(self):
        pass
