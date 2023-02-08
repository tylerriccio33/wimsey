from dataframe import core

class SparkDataFrame(core.CoreDataFrame):
    def column_datatype(self, column):
        return self.df.schema['int'].dataType
    
    def column_mean(self, column):
        mean_row = self.df.agg({column: 'mean'}).collect()
        return mean_row[0][0]
