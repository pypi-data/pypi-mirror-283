import unittest

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from affectlog.wrappers import ShapWrapper

import affectlog as alx
import pandas as pd


class TestShapWrapperMLPRegressorAttrition(unittest.TestCase):
    def setUp(self):
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
        with self.assertRaises(TypeError):
            self.exp.predict_parts(self.X.iloc[[0]], type='shap_wrapper')


class TestShapWrapperRandomForestClassifierAttritionNumericalDataset(unittest.TestCase):
    def setUp(self):
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/HR-Employee-Attrition.csv")
        data['Attrition'] = LabelEncoder().fit_transform(data['Attrition'])

        self.X = data.loc[:, ["Age", "DailyRate", "DistanceFromHome", "HourlyRate", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "PercentSalaryHike", "TotalWorkingYears", "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager"]]
        self.y = data['Attrition']

        clf = RandomForestClassifier(n_estimators=100, random_state=123)
        clf.fit(self.X, self.y)

        self.exp = alx.Explainer(clf, self.X, self.y, verbose=False)

    def test_predict_parts(self):
        case1 = self.exp.predict_parts(self.X.iloc[[0]], type='shap_wrapper')
        case2 = self.exp.predict_parts(self.X.iloc[1:2, :], type='shap_wrapper', shap_explainer_type='KernelExplainer')
        case3 = self.exp.predict_parts(self.X.iloc[1, :], type='shap_wrapper')
        case4 = self.exp.predict_parts(self.X.iloc[[0]], N=500, type='shap_wrapper', shap_explainer_type='KernelExplainer')

        self.assertIsInstance(case1, ShapWrapper)
        self.assertEqual(case1.shap_explainer_type, 'TreeExplainer')

        self.assertIsInstance(case2, ShapWrapper)
        self.assertEqual(case2.shap_explainer_type, 'KernelExplainer')

        self.assertIsInstance(case3, ShapWrapper)
        self.assertIsInstance(case4, ShapWrapper)

        case1.plot(show=False)
        case2.plot(show=False)
        case3.plot(show=False)
        case4.plot(show=False)

    def test_model_parts(self):
        case1 = self.exp.model_parts(type='shap_wrapper', N=22)
        case2 = self.exp.model_parts(type='shap_wrapper', N=22, shap_explainer_type='KernelExplainer')

        self.assertIsInstance(case1, ShapWrapper)
        self.assertEqual(case1.shap_explainer_type, 'TreeExplainer')

        self.assertIsInstance(case2, ShapWrapper)
        self.assertEqual(case2.shap_explainer_type, "KernelExplainer")

        case1.plot(show=False)
        case2.plot(show=False)


if __name__ == '__main__':
    unittest.main()
