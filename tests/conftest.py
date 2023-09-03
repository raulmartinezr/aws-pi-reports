# -*- coding: utf-8 -*-
"""
The aim of this configuration is to avoid running certain tests
https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
"""

from typing import Any, Dict, List

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--runslow", action="store_true", default=False, help="run slow tests")


# pylint: disable=C0201
def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]) -> None:
    """Modify test description at runtime"""

    skippable: Dict[str, Any] = {}
    if not config.getoption("--runslow"):
        skippable["slow"] = pytest.mark.skip(reason="need --runslow option to run")

    for item in items:
        for s, skip in skippable.items():
            if s in item.keywords:
                item.add_marker(skip)
