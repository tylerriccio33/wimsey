from dataframe import dynamic

class TestSuite():
    """
    Class with methods for adding tests to stack,
    and executing those tests, recording the results.
    """
    def __init__(self):
        self.test_stack = []

    def add(self, *test):
        self.test_stack += (test)

    def test(self, df):
        test_df = dynamic.dynamic_dataframe(df)
        results = []
        for test in self.test_stack:
            results.append({
                'test': test[0],
                'args': test[1],
                'pass': test[2](test_df)
            })
        return results

    def validate(self, df):
        test_results = self.test(df)
        if any(i for i in test_results if not i['pass']):
            newline = '\n'
            raise Exception(
                f"Data not validated, the following tests failed:{newline}     "
                f"{newline+'    '.join([str(i) for i in test_results if not i['pass']])}"
            )
        print('All tests passed')
