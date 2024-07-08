import unittest
import pandas as pd

class DatasetsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        case1 = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/ds_salaries.csv")
        case2 = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/HR-Employee-Attrition.csv")

        self.assertIsInstance(case1, pd.DataFrame)
        self.assertIsInstance(case2, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
