from dataframe import core

class DaskDataFrame(core.CoreDataFrame):
    def column_datatype(self, column):
        return type(self.df[column].dtype)
    
    def column_mean(self, column):
        return self.df[column].mean().compute()
