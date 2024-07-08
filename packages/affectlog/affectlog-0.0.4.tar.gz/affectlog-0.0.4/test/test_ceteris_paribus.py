import unittest

import numpy as np
import pandas as pd
from plotly.graph_objs import Figure
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

import affectlog as alx
from affectlog.predict_explanations._ceteris_paribus import utils


class CeterisParibusTestDsSalaries(unittest.TestCase):
    def setUp(self):
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/ds_salaries.csv")
        data.loc[:, 'salary_in_usd'] = data['salary_in_usd']

        self.X = data.drop(columns='salary_in_usd')
        self.y = data.salary_in_usd

        numeric_features = ['work_year', 'experience_level', 'employment_type', 'remote_ratio', 'company_size']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_features = ['job_title', 'salary_currency', 'employee_residence', 'company_location']
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

    def test_calculate_variable_split(self):
        splits = utils.calculate_variable_split(self.X, self.X.columns, 101)
        self.assertIsInstance(splits, dict)
        for key, value in splits.items():
            self.assertLessEqual(len(value), 101)

        splits = utils.calculate_variable_split(self.X, ['work_year', 'experience_level'], 121)
        self.assertIsInstance(splits, dict)
        for key, value in splits.items():
            self.assertLessEqual(len(value), 121)

        splits = utils.calculate_variable_split(self.X, ['job_title'], 5)
        self.assertIsInstance(splits, dict)
        for key, value in splits.items():
            self.assertLessEqual(len(value), np.unique(self.X.loc[:, 'job_title']).shape[0])

    def test_single_variable_profile(self):
        splits = utils.calculate_variable_split(self.X, self.X.columns, 101)
        new_data_work_year = utils.single_variable_profile(self.exp.predict_function,
                                                           self.exp.model,
                                                           self.X.iloc[[0], :],
                                                           'work_year',
                                                           splits['work_year'])

        new_data_job_title = utils.single_variable_profile(self.exp.predict_function,
                                                           self.exp.model,
                                                           self.X.iloc[[0], :],
                                                           'job_title',
                                                           splits['job_title'])

        self.assertIsInstance(new_data_work_year, pd.DataFrame)
        self.assertIsInstance(new_data_job_title, pd.DataFrame)

        self.assertLessEqual(new_data_work_year.shape[0], 101)
        self.assertLessEqual(new_data_job_title.shape[0], 101)

        self.assertTrue(np.isin(np.array(['_yhat_', '_vname_', '_ids_']),
                                new_data_work_year.columns).all())

        self.assertTrue(np.isin(np.array(['_yhat_', '_vname_', '_ids_']),
                                new_data_job_title.columns).all())

        self.assertTrue(pd.api.types.is_numeric_dtype(new_data_work_year.loc[:, 'work_year']))

    def test_calculate_variable_profile(self):
        splits = utils.calculate_variable_split(self.X, ['work_year', 'job_title'], 121)
        vp = utils.calculate_variable_profile(self.exp.predict_function, self.exp.model, self.X.iloc[[0], :], splits, 1, verbose=False)
        self.assertIsInstance(vp, pd.DataFrame)

        splits = utils.calculate_variable_split(self.X, ['job_title'], 5)
        vp = utils.calculate_variable_profile(self.exp.predict_function, self.exp.model, self.X.iloc[[0], :], splits, 1, verbose=False)
        self.assertIsInstance(vp, pd.DataFrame)

        splits = utils.calculate_variable_split(self.X, self.X.columns, 15)
        vp = utils.calculate_variable_profile(self.exp.predict_function, self.exp.model, self.X.iloc[[0], :], splits, 2, verbose=False)
        self.assertIsInstance(vp, pd.DataFrame)

    def test_calculate_ceteris_paribus(self):
        splits = utils.calculate_variable_split(self.X, ['work_year', 'job_title'], 121)

        cp = utils.calculate_ceteris_paribus(self.exp,
                                             self.X.iloc[[0], :].copy(),
                                             splits,
                                             self.y.iloc[0],
                                             processes=1,
                                             verbose=False)

        self.assertIsInstance(cp, tuple)
        self.assertIsInstance(cp[0], pd.DataFrame)
        self.assertIsInstance(cp[1], pd.DataFrame)

        splits = utils.calculate_variable_split(self.X, ['job_title'], 5)

        cp = utils.calculate_ceteris_paribus(self.exp,
                                             self.X.iloc[[0], :].copy(),
                                             splits,
                                             self.y.iloc[0],
                                             processes=1,
                                             verbose=False)

        self.assertIsInstance(cp, tuple)
        self.assertIsInstance(cp[0], pd.DataFrame)
        self.assertIsInstance(cp[1], pd.DataFrame)

        splits = utils.calculate_variable_split(self.X, self.X.columns, 15)

        cp = utils.calculate_ceteris_paribus(self.exp,
                                             self.X.iloc[[0], :].copy(),
                                             splits,
                                             self.y.iloc[0],
                                             processes=1,
                                             verbose=False)

        self.assertIsInstance(cp, tuple)
        self.assertIsInstance(cp[0], pd.DataFrame)
        self.assertIsInstance(cp[1], pd.DataFrame)

    def test_constructor(self):
        cp = self.exp.predict_profile(self.X.iloc[[0], :], verbose=False)
        self.assertIsInstance(cp, alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(cp.result, pd.DataFrame)
        self.assertIsInstance(cp.new_observation, pd.DataFrame)

        with self.assertRaises(ValueError):
            self.exp.predict_profile(self.X.iloc[[0], :], variables=['aaa'], verbose=False)

        with self.assertRaises(TypeError):
            self.exp.predict_profile(self.X.iloc[[0], :], y=3, verbose=False)

        self.assertIsInstance(self.exp.predict_profile(self.X.iloc[0, :], verbose=False),
                              alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(self.exp.predict_profile(self.X.iloc[0:10, :], verbose=False),
                              alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(self.exp.predict_profile(self.X.iloc[[0], :], variables=['work_year'], verbose=False),
                              alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(self.exp.predict_profile(self.X.iloc[0, :].values.reshape(-1, ), verbose=False),
                              alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(self.exp.predict_profile(self.X.iloc[0:10, :].values, verbose=False),
                              alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(self.exp.predict_profile(self.X.iloc[0:10, :].values, processes=2, verbose=False),
                              alx.predict_explanations.CeterisParibus)

    def test_plot(self):

        case1 = self.exp.predict_profile(self.X.iloc[2:10, :], verbose=False)
        case2 = self.exp.predict_profile(self.X.iloc[0, :], verbose=False)
        case3 = self.exp.predict_profile(self.X.iloc[1, :], verbose=False)

        self.assertIsInstance(case1, alx.predict_explanations.CeterisParibus)
        self.assertIsInstance(case2, alx.predict_explanations.CeterisParibus)

        fig1 = case1.plot((case2, case3), show=False)
        fig2 = case2.plot(variable_type="categorical", show=False)
        fig3 = case1.plot(case2, variables="work_year", show=False)
        fig4 = case2.plot(variables="job_title", show=False)
        fig5 = case1.plot(case3, size=1, color="job_title", facet_ncol=1, show_observations=False,
                          title="title", horizontal_spacing=0.2, vertical_spacing=0.15,
                          show=False)
        fig6 = case2.plot(variables=["job_title"], show=False)
        fig7 = case2.plot(variables=["job_title", 'company_location'], show=False)
        fig8 = case2.plot(variables=["job_title", 'company_location'], variable_type='categorical', show=False)

        self.assertIsInstance(fig1, Figure)
        self.assertIsInstance(fig2, Figure)
        self.assertIsInstance(fig3, Figure)
        self.assertIsInstance(fig4, Figure)
        self.assertIsInstance(fig5, Figure)
        self.assertIsInstance(fig6, Figure)
        self.assertIsInstance(fig7, Figure)
        self.assertIsInstance(fig8, Figure)


if __name__ == '__main__':
    unittest.main()
