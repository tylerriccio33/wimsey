import narwhals as nw
from narwhals.typing import FrameT


@nw.narwhalify
def describe(df: FrameT) -> dict[str, float]:
    """
    Outputs a dictionary for use in testing, mimicking polars 'describe' method.

    Note this code is adapted from polars own descrip function.
    """
    if not df.columns:
        return {}

    # Determine which columns should get std/mean/percentile statistics
    stat_cols = {c for c, dt in df.schema.items() if dt.is_numeric()}

    mean_exprs = [
        (nw.col(c).mean() if c in stat_cols else nw.lit(None)).alias(f"mean_{c}")
        for c in df.columns
    ]
    std_exprs = [
        (nw.col(c).std() if c in stat_cols else nw.lit(None)).alias(f"std_{c}")
        for c in df.columns
    ]
    min_exprs = [
        (nw.col(c).min() if c in stat_cols else nw.lit(None)).alias(f"min_{c}")
        for c in df.columns
    ]
    max_exprs = [
        (nw.col(c).max() if c in stat_cols else nw.lit(None)).alias(f"max_{c}")
        for c in df.columns
    ]
    df_metrics = df.select(
        nw.col(*df.columns).count().name.prefix("count_"),
        nw.col(*df.columns).null_count().name.prefix("null_count_"),
        *mean_exprs,
        *std_exprs,
        *min_exprs,
        *max_exprs,
    )
    return {k: v[0] for k, v in df_metrics.to_dict(as_series=False).items()}
