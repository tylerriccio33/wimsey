from typing import Callable, Any
from dataclasses import dataclass

from narwhals.typing import FrameT

from wimsey.dataframe import describe
from wimsey.tests import result
from wimsey.config import read_config, collect_tests


@dataclass
class final_result:
    success: bool
    results: list[result]


class DataValidationException(Exception):
    ...


def run_all_tests(df: FrameT, tests: list[Callable[[...], result]]) -> result:
    description: dict[str, Any] = describe(df)
    results: list[result] = []
    for test in tests:
        results.append(test(description))
    return final_result(
        success=all(i.success for i in results),
        results=results,
    )


def test(
    df: FrameT, contract: str | dict, storage_options: dict | None = None
) -> final_result:
    """
    Carry out tests on dataframe and return results. This will *not* raise
    an exception on test failure, and will instead return a 'final_result'
    object, with a boolean 'success' field, and a detailed list of individual
    tests.

    If you want to halt processing in the event of a data contract failure,
    see `validate` function.
    """
    tests = (
        read_config(path=contract, storage_options=storage_options)
        if isinstance(contract, str)
        else collect_tests(contract)
    )
    return run_all_tests(df, tests)


def validate(
    df: FrameT, contract: str | dict, storage_options: dict | None = None
) -> FrameT:
    """
    Carry out tests on dataframe, returning original dataframe if tests are
    successful, and raising a DataValidationException in case of failure.
    """
    results = test(
        df=df,
        path=contract,
        storage_options=storage_options,
    )
    if not results.success:
        failures: str[list] = [
            f"{i.name} (unexpected: {i.unexpected})"
            for i in results.results
            if not i.success
        ]
        newline = "\n - "
        msg = f"At least one test failed:\n - {newline.join(failures)}"
        raise DataValidationException(msg)
    return df
