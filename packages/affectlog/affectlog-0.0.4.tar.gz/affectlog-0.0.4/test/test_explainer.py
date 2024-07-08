import unittest

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

import numpy as np
import pandas as pd
import warnings


class ExplainerTest(unittest.TestCase):
    def setUp(self):
        # Load dataset
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/ds_salaries.csv")
        data.loc[:, 'salary'] = LabelEncoder().fit_transform(data.salary_in_usd)

        self.X = data.drop(columns='salary')
        self.y = data.salary

        # Define numeric features and preprocessing steps
        numeric_features = ['work_year', 'experience_level', 'employment_type', 'remote_ratio', 'company_size']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        # Define categorical features and preprocessing steps
        categorical_features = ['job_title', 'salary_currency', 'employee_residence', 'company_location']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        # Combine preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        # Define and fit the model
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', MLPRegressor(hidden_layer_sizes=(150, 100, 50),
                                                          max_iter=500, random_state=0))])

        clf.fit(self.X, self.y)
        self.model = clf

    def test(self):
        # Create explainers with different combinations of X and y
        case1 = alx.Explainer(self.model, self.X, self.y, verbose=False)
        case2 = alx.Explainer(self.model, self.X, None, verbose=False)
        case3 = alx.Explainer(self.model, None, self.y, verbose=False)
        case4 = alx.Explainer(self.model, None, None, verbose=False)

        # Assert that the explainers are instances of alx.Explainer
        self.assertIsInstance(case1, alx.Explainer)
        self.assertIsInstance(case2, alx.Explainer)
        self.assertIsInstance(case3, alx.Explainer)
        self.assertIsInstance(case4, alx.Explainer)

        # Test model_performance, model_parts, and model_profile with missing data
        with self.assertRaises(ValueError):
            case2.model_performance()
        with self.assertRaises(ValueError):
            case3.model_parts()
        with self.assertRaises(ValueError):
            case4.model_profile()

        # Test predict_parts and predict_profile methods
        case5 = case2.predict_parts(self.X.iloc[[0]])
        case6 = case2.predict_profile(self.X.iloc[[0]])

        self.assertIsInstance(case5, alx.predict_explanations.BreakDown)
        self.assertIsInstance(case6, alx.predict_explanations.CeterisParibus)

        # Test warning for incorrect predict_function
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            case5 = alx.Explainer(self.model, self.X, self.y, predict_function=1, verbose=False)
            assert issubclass(w[-1].category, UserWarning)

        self.assertIsInstance(case5, alx.Explainer)

    def test_errors(self):
        from sklearn.ensemble import RandomForestRegressor

        # Load dataset
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/HR-Employee-Attrition.csv")
        X = data.drop(columns=['Attrition', 'MonthlyIncome']).iloc[1:100, :]
        y = data['MonthlyIncome'][1:100]

        model = RandomForestRegressor()
        model.fit(X, y)

        def predict_function_return_2d(m, d):
            n_rows = d.shape[0]
            prediction = m.predict(d)
            return prediction.reshape((n_rows, 1))

        def predict_function_return_3d(m, d):
            n_rows = d.shape[0]
            prediction = m.predict(d)
            return prediction.reshape((n_rows, 1, 1))

        def predict_function_return_one_element_array(m, d):
            return np.array(0.2)

        warnings.simplefilter("always")
        with warnings.catch_warnings(record=True) as w:
            alx.Explainer(model, X, y, verbose=False, model_type='regression',
                          predict_function=predict_function_return_2d)
            assert issubclass(w[-1].category, UserWarning)

        with warnings.catch_warnings(record=True) as w:
            alx.Explainer(model, X, y, verbose=False, model_type='regression',
                          predict_function=predict_function_return_3d)
            assert issubclass(w[-1].category, UserWarning)

        with warnings.catch_warnings(record=True) as w:
            alx.Explainer(model, X, y, verbose=False, model_type='regression',
                          predict_function=predict_function_return_one_element_array)
            assert issubclass(w[-1].category, UserWarning)


if __name__ == '__main__':
    unittest.main()
