from abc import ABC, abstractmethod


class Action(ABC):
    """
    Abstract base class for Action.
    """

    @abstractmethod
    def __init__(self):
        """
        Abstract method __init__
        Defines a method that should initialize the class
        """
        pass

    @abstractmethod
    def run(self):
        """
        Abstract method run
        Defines a method that should be used to execute the action
        """
        pass
