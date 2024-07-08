import unittest
from plotly.graph_objs import Figure
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

import affectlog as alx
import time
import numpy as np
import pandas as pd
from affectlog.al360.static import get_free_port, try_port
from affectlog.al360.plots import *

class AL360Test(unittest.TestCase):
    def setUp(self):
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/ds_salaries.csv")
        data.loc[:, 'experience_level'] = LabelEncoder().fit_transform(data.experience_level)

        self.X = data.drop(columns='experience_level')
        self.y = data.experience_level
        self.john = pd.DataFrame({'work_year': [2022], 'employment_type': ['FT'], 'job_title': ['Data Scientist'], 
                                  'salary_currency': ['USD'], 'salary_in_usd': [150000], 'employee_residence': ['US'], 
                                  'remote_ratio': [100], 'company_location': ['US'], 'company_size': ['L']}, 
                                  index = ['John'])

        numeric_features = ['salary_in_usd']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_features = ['work_year', 'employment_type', 'job_title', 'salary_currency', 'employee_residence', 'remote_ratio', 'company_location', 'company_size']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', MLPClassifier(hidden_layer_sizes=(20, 20),
                                                           max_iter=400, random_state=0))])
        clf2 = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', MLPClassifier(hidden_layer_sizes=(50, 100, 50),
                                                            max_iter=400, random_state=0))])

        clf.fit(self.X, self.y)
        clf2.fit(self.X, self.y)

        self.exp = alx.Explainer(clf, self.X, self.y, label="model1", verbose=False)
        self.exp2 = alx.Explainer(clf2, self.X, self.y, label="model2", verbose=False)

        # These plots should be supported
        self.reference_plots = [ROCContainer, ShapleyValuesContainer, BreakDownContainer, CeterisParibusContainer,
                                FeatureImportanceContainer, PartialDependenceContainer, AccumulatedDependenceContainer, 
                                MetricsContainer, FairnessCheckContainer, ShapleyValuesDependenceContainer, 
                                ShapleyValuesVariableImportanceContainer, VariableAgainstAnotherContainer, 
                                VariableDistributionContainer]

    def test_supported_plots(self):
        al360 = alx.AL360()
        al360.push_model(self.exp)
        al360.push_model(self.exp2)
        plots = al360.get_supported_plots()
        sorting = lambda x: x.__name__
        self.assertEqual(sorted(plots, key=sorting), sorted(self.reference_plots, key=sorting))

        try:
            al360.stop_server()
        except Exception:
            pass

    def test_server(self):
        al360 = alx.AL360()
        al360.push_model(self.exp)
        al360.push_model(self.exp2)
        port = get_free_port()
        try:
            al360.run_server(port=port)
            time.sleep(2)
            self.assertFalse(try_port(port))
            al360.stop_server()
        except AssertionError as e:
            al360.stop_server()

        try:
            al360.stop_server()
        except Exception:
            pass

    def test_plots(self):
        al360 = alx.AL360()
        al360.push_model(self.exp)
        al360.push_observations(self.X.iloc[[1],])
        al360.set_option('DatasetShapleyValues', 'N', 10)
        al360.plots_manager.fill_cache()
        for p in self.reference_plots:
            ref_counts = list(map(lambda param_type: len(al360.list_params(param_type)), p.info.get('requiredParams')))
            count = np.sum([1 for plot in al360.plots_manager.cache if plot.__class__ == p])
            self.assertEqual(np.prod(ref_counts), count, msg="Count of " + str(p))

        try:
            al360.stop_server()
        except Exception:
            pass

    def test_observation_attributes(self):
        al360 = alx.AL360()
        al360.push_model(self.exp)
        ds_salaries = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/ds_salaries.csv").iloc[1:20]
        al360.push_observations(ds_salaries) # with observations
        al360.push_observations(self.john) # custom observation
        attrs = al360.get_params_attributes('observation')
        attrs_name = list(map(lambda x: x.get('name'), attrs))
        self.assertEqual(sorted(attrs_name), sorted(ds_salaries.columns))
        for attr in attrs:
            self.assertTrue(all(attr.get('values')[:-1] == ds_salaries[attr.get('name')]))

        try:
            al360.stop_server()
        except Exception:
            pass
        
    def test_variable_attributes(self):
        al360 = alx.AL360()
        al360.push_model(self.exp)
        ds_salaries = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/ds_salaries.csv").iloc[1:20]
        al360.push_observations(ds_salaries)
        attrs = { k: al360.get_param_attributes('variable', k) for k in self.X.columns }
        self.assertEqual(attrs, {
            'work_year': {'type': 'categorical', 'min': None, 'max': None, 'levels': [2020, 2021, 2022]},
            'employment_type': {'type': 'categorical', 'min': None, 'max': None, 'levels': ['FT', 'PT', 'CT', 'FL']},
            'job_title': {'type': 'categorical', 'min': None, 'max': None, 'levels': sorted(data['job_title'].unique().tolist())},
            'salary_currency': {'type': 'categorical', 'min': None, 'max': None, 'levels': sorted(data['salary_currency'].unique().tolist())},
            'salary_in_usd': {'type': 'numeric', 'min': data['salary_in_usd'].min(), 'max': data['salary_in_usd'].max(), 'levels': None},
            'employee_residence': {'type': 'categorical', 'min': None, 'max': None, 'levels': sorted(data['employee_residence'].unique().tolist())},
            'remote_ratio': {'type': 'categorical', 'min': None, 'max': None, 'levels': [0, 50, 100]},
            'company_location': {'type': 'categorical', 'min': None, 'max': None, 'levels': sorted(data['company_location'].unique().tolist())},
            'company_size': {'type': 'categorical', 'min': None, 'max': None, 'levels': ['S', 'M', 'L']}
        })

        try:
            al360.stop_server()
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()
