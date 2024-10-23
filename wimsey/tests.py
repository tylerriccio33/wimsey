from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class result:
    name: str
    success: bool
    unexpected: Any = None


def _range_check(metric: str) -> Callable:
    """
    Factory function for generated tests of the form "x should be within range"
    """

    def should_be(
        describe: dict[str, Any],
        column: str,
        exactly: float | int | None = None,
        less_than: float | int | None = None,
        less_than_or_equal_to: float | int | None = None,
        greater_than: float | int | None = None,
        greater_than_or_equal_to: float | int | None = None,
        **kwargs,
    ) -> result:
        """
        Test that column mean is within designated range
        """
        checks: list[bool] = []
        value: Any = describe[f"{metric}_{column}"]
        if exactly is not None:
            checks.append(value == exactly)
        if less_than is not None:
            checks.append(value < less_than)
        if greater_than is not None:
            checks.append(value > greater_than)
        if less_than_or_equal_to is not None:
            checks.append(value <= less_than_or_equal_to)
        if greater_than_or_equal_to is not None:
            checks.append(value >= greater_than_or_equal_to)
        return result(
            name=f"{metric}-of-{column}-should-be",
            success=all(checks),
            unexpected=value if not all(checks) else None,
        )

    return should_be


possible_tests: dict[str, Callable] = {
    "mean_should_be": _range_check("mean"),
    "min_should_be": _range_check("min"),
    "max_should_be": _range_check("max"),
    "null_count_should_be": _range_check("null_count"),
    "count_should_be": _range_check("count"),
}
