"""Reports module"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Report(ABC):
    """
    Base Report interface with methods to be implemented by concrete reports
    """

    # @property
    # @abstractmethod
    # def product(self) -> None:
    #     pass

    @abstractmethod
    def read_report_input(self) -> None:
        pass

    @abstractmethod
    def processs_report_input(self) -> None:
        pass

    @abstractmethod
    def processs_queries_output(self) -> None:
        pass

    @abstractmethod
    def report(self) -> None:
        pass


class StandardRDSReport(Report):
    """
    Standard RDS Report
    """
