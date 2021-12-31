from abc import ABCMeta, abstractmethod


class Module(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def summary(self):
        pass

    @abstractmethod
    def show(self):
        pass
