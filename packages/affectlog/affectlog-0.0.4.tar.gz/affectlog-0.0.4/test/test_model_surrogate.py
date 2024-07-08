import unittest
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
import affectlog as alx
import pandas as pd


class ModelSurrogateTest(unittest.TestCase):
    def setUp(self):
        # Load the Skills dataset and preprocess it
        data = alx.datasets.load_skills()  # Assuming load_skills() is a generic function to load the dataset
        self.X = data.drop(columns=['target'])
        self.y = data['target']
        self.X.gender = LabelEncoder().fit_transform(self.X.gender)  # Example transformation

        # This checks for no feature_importances_ attribute
        model = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=400, random_state=0)
        model.fit(self.X, self.y)
        self.exp = alx.Explainer(model, self.X, self.y, verbose=False)

        # Load another sample of the Skills dataset for a regression task
        data2 = alx.datasets.load_skills()  # Reusing load_skills() function for another example
        self.X2 = data2.drop(columns=['target']).iloc[0:2000, :]
        self.y2 = data2['target'].iloc[0:2000]

        # This checks for feature_importances_ attribute
        model2 = RandomForestRegressor(random_state=0)
        model2.fit(self.X2, self.y2)
        self.exp2 = alx.Explainer(model2, self.X2, self.y2, verbose=False)

    def test(self):
        # Testing various model surrogates
        case1 = self.exp.model_surrogate()
        case2 = self.exp2.model_surrogate()
        case3 = self.exp.model_surrogate(max_vars=3, max_depth=2)
        case4 = self.exp2.model_surrogate(max_vars=3, max_depth=2)

        case5 = self.exp.model_surrogate(type='linear')
        case6 = self.exp2.model_surrogate(type='linear')
        case7 = self.exp.model_surrogate(type='linear', max_vars=3)
        case8 = self.exp2.model_surrogate(type='linear', max_vars=3)

        # Assertions to ensure proper types and attributes
        self.assertIsInstance(case1, DecisionTreeClassifier)
        self.assertIsInstance(case1.performance, pd.DataFrame)
        self.assertTrue(hasattr(case1, 'plot'))
        self.assertIsInstance(case2, DecisionTreeRegressor)
        self.assertIsInstance(case2.performance, pd.DataFrame)
        self.assertTrue(hasattr(case2, 'plot'))
        self.assertIsInstance(case3, DecisionTreeClassifier)
        self.assertIsInstance(case3.performance, pd.DataFrame)
        self.assertTrue(hasattr(case3, 'plot'))
        self.assertIsInstance(case4, DecisionTreeRegressor)
        self.assertIsInstance(case4.performance, pd.DataFrame)
        self.assertTrue(hasattr(case4, 'plot'))

        self.assertIsInstance(case5, LogisticRegression)
        self.assertIsInstance(case5.performance, pd.DataFrame)
        self.assertIsInstance(case6, LinearRegression)
        self.assertIsInstance(case6.performance, pd.DataFrame)
        self.assertIsInstance(case7, LogisticRegression)
        self.assertIsInstance(case7.performance, pd.DataFrame)
        self.assertIsInstance(case8, LinearRegression)
        self.assertIsInstance(case8.performance, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
