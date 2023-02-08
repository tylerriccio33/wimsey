import pandas as pd

from testing import suite, tests
from dataframe.dynamic import dynamic_dataframe


test = suite.TestSuite()
test.add(tests.column_mean_should_be_in_range('a', 0, 100))
test.add(tests.column_mean_should_be_in_range('b', 3, 5))
test.add(tests.should_have_column_named('b'))
test.add(tests.should_have_column_named('mystery'))

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

results = test.test(df)
print(results)

test.validate(df)
