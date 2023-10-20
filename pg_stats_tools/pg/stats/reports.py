"""Base reports module"""


from abc import ABC, abstractmethod


class Report(ABC):
    """
    Interface for all reports
    """

    # @property
    # @abstractmethod
    # def product(self) -> None:
    #     pass
    @classmethod
    @abstractmethod
    def get_help(cls) -> str:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
