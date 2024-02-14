from typing import Any
import importlib

import pandas as pd
import ibis
from ibis.expr.types.relations import Table
from ufo.wrappers import coerce_into

@coerce_into(False, ImportError)
def is_lib_df(df: Any, import_route: str, object_name: str):
    to_match = getattr(
        importlib.import_module(import_route),
        object_name,
    )
    return isinstance(df, to_match)

def dataframe_to_ibis(df) -> Table:
    if is_lib_df(df, "pandas", "DataFrame"):
        return ibis.pandas.connect({"df": df}).table("df")
    if is_lib_df(df,  "dask.dataframe", "DataFrame"):
        return ibis.dask.connect({"df": df}).table("df")
    if is_lib_df(df, "polars.dataframe.frame", "DataFrame"):
        return ibis.polars.connect({"df": df}).table("df")
    if is_lib_df(df, "pyarrow", "Table"):
        return ibis.connect("duckdb://testing").create_table("df", df, overwrite=True)
    raise NotImplementedError("The given dataframe is not currently supported")


