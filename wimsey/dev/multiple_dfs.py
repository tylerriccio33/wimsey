import pandas as pd
import polars as pl
import dask.dataframe as dd
from pyspark.sql import SparkSession


df = pd.DataFrame({'str': ['cat', 'bat', 'mat'], 'int': [4, 7, 2], 'float': [4.56, 0.09, 4.5]})

spark = SparkSession.builder.getOrCreate()
sdf = spark.createDataFrame(df)

pdf = pl.DataFrame(df)

ddf = dd.from_pandas(df, npartitions=1)
