import unittest

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

import affectlog as alx

class PredictTestAttrition(unittest.TestCase):
    def setUp(self):
        # Load the HR Employee Attrition dataset
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/HR-Employee-Attrition.csv")
        data['Attrition'] = LabelEncoder().fit_transform(data['Attrition'])

        self.X = data.drop(columns='Attrition')
        self.y = data['Attrition']

        numeric_features = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_features = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('regressor', MLPRegressor(hidden_layer_sizes=(150, 100, 50),
                                                         max_iter=500, random_state=0))])

        clf.fit(self.X, self.y)

        self.exp = alx.Explainer(clf, self.X, self.y, verbose=False)

    def test(self):
        self.assertIsInstance(self.exp.predict(self.X.iloc[[0]]), np.ndarray)
        with self.assertRaises(TypeError):
            self.exp.predict(self.X.iloc[0])
        with self.assertRaises(ValueError):
            self.exp.predict(self.X.iloc[0].values)

        self.assertIsInstance(self.exp.predict(self.X.iloc[:100]), np.ndarray)


if __name__ == '__main__':
    unittest.main()
