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

    @property
    def required(self):
        return False

    @property
    def injectable(self):
        return False

    # This can be overridden if the parameter value needs validating.
    def validate(self, value):
        return True
