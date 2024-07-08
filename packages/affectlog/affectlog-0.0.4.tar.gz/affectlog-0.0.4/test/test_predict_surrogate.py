import unittest

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

import affectlog as alx
import lime
import pandas as pd

class PredictSurrogateTestAttrition(unittest.TestCase):
    def setUp(self):
        # Load the HR Employee Attrition dataset
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/HR-Employee-Attrition.csv")
        self.X = data.drop(columns=['Attrition', 'JobRole', 'Over18'])
        self.y = data['Attrition']
        self.X['Gender'] = LabelEncoder().fit_transform(self.X['Gender'])

        # this checks for no feature_importances_ attribute
        model = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=400, random_state=0)
        model.fit(self.X, self.y)
        self.exp = alx.Explainer(model, self.X, self.y, verbose=False)

        # Using the same dataset but fitting a regression model for testing
        self.X2 = data.drop(columns=['Attrition', 'JobRole', 'Over18', 'EmployeeNumber'])
        self.y2 = data['DailyRate']  # Using a numerical target for regression

        model2 = RandomForestRegressor(random_state=0)
        model2.fit(self.X2, self.y2)
        self.exp2 = alx.Explainer(model2, self.X2, self.y2, verbose=False)

    def test(self):
        case1 = self.exp.predict_surrogate(new_observation=self.X.iloc[1, :],
                                           feature_names=self.X.columns)
        case2 = self.exp.predict_surrogate(new_observation=self.X.iloc[1:2, :],
                                           mode='classification',
                                           feature_names=self.X.columns,
                                           discretize_continuous=True,
                                           num_features=4)
        case3 = self.exp.predict_surrogate(new_observation=self.X.iloc[1:2, :].to_numpy(),
                                           feature_names=self.X.columns,
                                           kernel_width=2,
                                           num_samples=50)
        case4 = self.exp2.predict_surrogate(new_observation=self.X2.iloc[1, :],
                                            feature_names=self.X2.columns)
        case5 = self.exp2.predict_surrogate(new_observation=self.X2.iloc[1:2, :],
                                            mode='regression',
                                            feature_names=self.X2.columns,
                                            discretize_continuous=True,
                                            num_features=4)
        case6 = self.exp2.predict_surrogate(new_observation=self.X2.iloc[1:2, :].to_numpy(),
                                            feature_names=self.X2.columns,
                                            kernel_width=2,
                                            num_samples=50)

        self.assertIsInstance(case1, lime.explanation.Explanation)
        self.assertIsInstance(case2, lime.explanation.Explanation)
        self.assertIsInstance(case3, lime.explanation.Explanation)
        self.assertIsInstance(case4, lime.explanation.Explanation)
        self.assertIsInstance(case5, lime.explanation.Explanation)
        self.assertIsInstance(case6, lime.explanation.Explanation)


if __name__ == '__main__':
    unittest.main()
