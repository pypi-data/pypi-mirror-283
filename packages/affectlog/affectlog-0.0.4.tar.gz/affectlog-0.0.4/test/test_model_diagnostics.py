import unittest

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

import affectlog as alx
from plotly.graph_objs import Figure
import time


class ModelDiagnosticsTestGerman(unittest.TestCase):
    def setUp(self):
        # Load the German dataset and preprocess it
        data = alx.datasets.load_german()
        data.loc[:, 'risk'] = LabelEncoder().fit_transform(data.risk)

        self.X = data.drop(columns='risk')
        self.y = data.risk

        numeric_features = ['age', 'credit_amount', 'duration']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_features = ['sex', 'job', 'housing', 'saving_accounts', 'checking_account', 'purpose']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', MLPClassifier(hidden_layer_sizes=(50, 100, 50),
                                                           max_iter=400, random_state=0))])

        clf.fit(self.X, self.y)

        self.exp = alx.Explainer(clf, self.X, self.y, verbose=False)
        self.exp2 = alx.Explainer(clf, self.X, self.y, label="model2", verbose=False)
        self.exp_performance = alx.Explainer(clf,
                                            pd.concat([self.X for _ in range(10)]).reset_index(drop=True),
                                            pd.concat([self.y for _ in range(10)]).reset_index(drop=True),
                                            verbose=False)

    def test_constructor(self):
        # Test model diagnostics constructor
        case1 = self.exp.model_diagnostics()
        self.assertIsInstance(case1, (alx.model_explanations.ResidualDiagnostics,))
        self.assertIsInstance(case1.result, (pd.DataFrame,))
        self.assertEqual(case1.result.shape[0], self.exp.data.shape[0])
        self.assertTrue(np.isin(['y', 'y_hat', 'residuals', 'abs_residuals', 'label', 'ids'],
                                case1.result.columns).all())

        # Test model diagnostics with specified variables
        case2 = self.exp.model_diagnostics(variables=['age', 'job'])
        self.assertIsInstance(case2, (alx.model_explanations.ResidualDiagnostics,))
        self.assertIsInstance(case2.result, (pd.DataFrame,))
        self.assertEqual(case2.result.shape[0], self.exp.data.shape[0])
        self.assertTrue(np.isin(['y', 'y_hat', 'residuals', 'abs_residuals', 'label', 'ids', 'age', 'job'],
                                case2.result.columns).all())
        self.assertFalse(np.isin(['credit_amount', 'duration', 'sex', 'housing'], case2.result.columns).any())

    def test_plot(self):
        # Test plotting of model diagnostics
        case1 = self.exp.model_diagnostics(variables=['credit_amount', 'housing'])
        case2 = self.exp.model_diagnostics()
        case3 = self.exp2.model_diagnostics()

        self.assertIsInstance(case1, alx.model_explanations.ResidualDiagnostics)
        self.assertIsInstance(case2, alx.model_explanations.ResidualDiagnostics)
        self.assertIsInstance(case3, alx.model_explanations.ResidualDiagnostics)

        fig1 = case1.plot(title="test1", variable="credit_amount", N=1000, show=False)
        fig2 = case2.plot(case3, variable="age", yvariable="abs_residuals",  N=None, show=False)
        fig3 = case2.plot(smooth=False, line_width=6, marker_size=1, variable="duration", show=False)

        self.assertIsInstance(fig1, Figure)
        self.assertIsInstance(fig2, Figure)
        self.assertIsInstance(fig3, Figure)

    def test_performance(self):
        # Test model diagnostics performance
        case = self.exp_performance.model_diagnostics()
        start_time = time.time()
        fig = case.plot(show=False)
        end_time = time.time()
        self.assertTrue((end_time - start_time) < 160)


if __name__ == '__main__':
    unittest.main()
