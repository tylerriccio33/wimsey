from dataframe import core, dask, spark, polars, pandas

def dynamic_dataframe(df):
    frame_dict = {
        "<class 'pandas.core.frame.DataFrame'>": pandas.PandasDataFrame,
        "<class 'pyspark.sql.dataframe.DataFrame'>": spark.SparkDataFrame,
        "<class 'polars.internals.dataframe.frame.DataFrame'>": polars.PolarsDataFrame,
        "<class 'dask.dataframe.core.DataFrame'>": dask.DaskDataFrame,
    }
    df_type = str(type(df))
    df = frame_dict[df_type](df)
    return df

