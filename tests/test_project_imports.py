import unittest


class TestProjectImports(unittest.TestCase):

    def test_core_dependencies(self):
        import numpy
        import pandas
        import requests

        self.assertIsNotNone(numpy)
        self.assertIsNotNone(pandas)
        self.assertIsNotNone(requests)

    def test_ml_dependencies(self):
        import sklearn
        import joblib

        self.assertIsNotNone(sklearn)
        self.assertIsNotNone(joblib)


if __name__ == "__main__":
    unittest.main()