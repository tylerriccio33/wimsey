from abc import ABC, abstractmethod

class CoreDataFrame(ABC):
    """
    Abstract baseclass for datatesting.

    Idea is that a dataframe can be wrapped into this,
    and will execute the same methods differently based on
    engine. (i.e. spark, polars, pandas, dask)

    Goal of this is to reduce complexity and allow development
    of tests to  be seperated from compatability concerns.
    """
    def __init__(self, df):
        self.df = df

    def column_names(self):
        return list(self.df.columns)

    @abstractmethod
    def column_datatype(self, column):
        """
        Get datatype of specified column
        """

    @abstractmethod
    def column_mean(self, column):
        """
        Get mean of column
        """

