import json
from typing import Callable
from functools import partial

import fsspec

from wimsey.tests import possible_tests


def collect_tests(config: list[dict]) -> list[Callable]:
    """
    Take a configuration, and build out tests
    """
    tests: list[callable] = []
    for item in config:
        test: callable | None = possible_tests.get(item.get("test"))
        if test is None:
            msg = (
                "Issue reading configuration, for at least one test, either no "
                "test is named, or a mispelt/unimplemented test is given"
            )
            raise ValueError(msg)
        tests.append(partial(test, **item))
    return tests


def read_config(path: str, storage_options: dict | None = None) -> list[Callable]:
    """
    Read a json or yaml configuration, and return list of test callables
    """
    storage_options_dict: dict = storage_options or {}
    config: dict
    with fsspec.open(path, "rt", **storage_options_dict) as file:
        contents = file.read()
    if path.endswith(".yaml"):
        try:
            import yaml

            config = yaml.safe_load(contents)
            return collect_tests(config)
        except ImportError as exception:
            msg = (
                "It looks like you're trying to import a yaml configured "
                "test suite. This is supported but requires an additional "
                "install of pyyaml (`pip install pyyaml`)"
            )
            raise ImportError(msg) from exception
    config = json.loads(contents)
    return collect_tests(config)
