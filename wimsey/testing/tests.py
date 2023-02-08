def should_have_column_named(column):
    def should_have_column_named(df):
        return column in df.column_names()
    args = {'column': column}
    return ('should_have_column_named', args, should_have_column_named)

def column_mean_should_be_in_range(column, lower, upper):
    def column_mean_should_be_in_range(df):
        mean = df.column_mean(column)
        return lower <= mean <= upper
    args = {'column': column, 'lower': lower, 'upper': upper}
    return ('column_mean_should_be_in_range', args, column_mean_should_be_in_range)
