import unittest
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

import affectlog as alx
from plotly.graph_objs import Figure


class PredictPartsTestAttrition(unittest.TestCase):
    def setUp(self):
        # Load the HR Employee Attrition dataset
        data = pd.read_csv("affectlog-0.0.3/affectlog/datasets/data/HR-Employee-Attrition.csv")
        data.loc[:, 'Attrition'] = LabelEncoder().fit_transform(data['Attrition'])

        self.X = data.drop(columns='Attrition')
        self.y = data['Attrition']

        numeric_features = self.X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = self.X.select_dtypes(include=['object']).columns.tolist()

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

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

    def test_bd(self):
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down'), alx.predict_explanations.BreakDown)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[0], type='break_down'), alx.predict_explanations.BreakDown)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[0].values, type='break_down'),
                              alx.predict_explanations.BreakDown)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down'),
                              alx.predict_explanations.BreakDown)

        with self.assertRaises(ValueError):
            self.exp.predict_parts(self.X.iloc[:2], type='break_down')

        with self.assertRaises(ValueError):
            self.exp.predict_parts(self.X.iloc[:2].values, type='break_down')

        self.assertTrue((self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down',
                                                order=numeric_features + categorical_features).result.variable_name.values == ['intercept'] + numeric_features + categorical_features + ['']).all())

        self.assertTrue((self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down',
                                                order=categorical_features + numeric_features).result.variable_name.values == ['intercept'] + categorical_features + numeric_features + ['']).all())

        self.assertTrue((self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down',
                                                order=list(range(len(self.X.columns)))).result.variable_name.values == ['intercept'] + self.X.columns.tolist() + ['']).all())

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down', path=list(range(len(self.X.columns)))),
                              alx.predict_explanations.BreakDown)
        
        _row_count = self.exp.data.shape[0]
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down', B=1),
                              alx.predict_explanations.BreakDown)
        self.assertEqual(_row_count, self.exp.data.shape[0])
        _row_count = self.exp.data.shape[0]
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down', N=100),
                              alx.predict_explanations.BreakDown)
        self.assertEqual(_row_count, self.exp.data.shape[0])

        self.assertTrue(hasattr(self.exp.predict_parts(self.X.iloc[[0]], type='break_down', keep_distributions=True),
                                'yhats_distributions'))

        self.assertIsInstance(
            self.exp.predict_parts(self.X.iloc[[0]], type='break_down', keep_distributions=True).yhats_distributions,
            pd.DataFrame)

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down', interaction_preference=2),
                              alx.predict_explanations.BreakDown)

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down', interaction_preference=0.5),
                              alx.predict_explanations.BreakDown)

    def test_ibd(self):
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions'),
                              alx.predict_explanations.BreakDown)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[0], type='break_down_interactions'),
                              alx.predict_explanations.BreakDown)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[0].values, type='break_down_interactions'),
                              alx.predict_explanations.BreakDown)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down_interactions'),
                              alx.predict_explanations.BreakDown)

        with self.assertRaises(ValueError):
            self.exp.predict_parts(self.X.iloc[:2], type='break_down_interactions')

        with self.assertRaises(ValueError):
            self.exp.predict_parts(self.X.iloc[:2].values, type='break_down_interactions')

        self.assertTrue((self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down_interactions',
                                                order=numeric_features + categorical_features).result.variable_name.values == ['intercept'] + numeric_features + categorical_features + ['']).all())

        self.assertTrue((self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down_interactions',
                                                order=categorical_features + numeric_features).result.variable_name.values == ['intercept'] + categorical_features + numeric_features + ['']).all())

        self.assertTrue((self.exp.predict_parts(self.X.iloc[[0]].values, type='break_down_interactions',
                                                order=list(range(len(self.X.columns)))).result.variable_name.values == ['intercept'] + self.X.columns.tolist() + ['']).all())

        self.assertIsInstance(
            self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions', path=list(range(len(self.X.columns)))),
            alx.predict_explanations.BreakDown)

        _row_count = self.exp.data.shape[0]
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions', B=1),
                              alx.predict_explanations.BreakDown)
        self.assertEqual(_row_count, self.exp.data.shape[0])
        _row_count = self.exp.data.shape[0]
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions', N=100),
                              alx.predict_explanations.BreakDown)
        self.assertEqual(_row_count, self.exp.data.shape[0])
        
        self.assertTrue(
            hasattr(self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions', keep_distributions=True),
                    'yhats_distributions'))

        self.assertIsInstance(
            self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions',
                                   keep_distributions=True).yhats_distributions,
            pd.DataFrame)

        self.assertIsInstance(
            self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions', interaction_preference=2),
            alx.predict_explanations.BreakDown)

        self.assertIsInstance(
            self.exp.predict_parts(self.X.iloc[[0]], type='break_down_interactions', interaction_preference=0.5),
            alx.predict_explanations.BreakDown)

    def test_shap(self):
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='shap'), alx.predict_explanations.Shap)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[0], type='shap'), alx.predict_explanations.Shap)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[0].values, type='shap'), alx.predict_explanations.Shap)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]].values, type='shap'), alx.predict_explanations.Shap)
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]].values, type='shap', processes=2),
                              alx.predict_explanations.Shap)

        with self.assertRaises(ValueError):
            self.exp.predict_parts(self.X.iloc[:2], type='shap')

        with self.assertRaises(ValueError):
            self.exp.predict_parts(self.X.iloc[:2].values, type='shap')

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]].values, type='shap',
                                                     order=numeric_features + categorical_features), alx.predict_explanations.Shap)

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='shap', path=list(range(len(self.X.columns)))),
                              alx.predict_explanations.Shap)

        with self.assertRaises(TypeError):
            self.exp.predict_parts(self.X.iloc[[0]], type='shap',
                                   path=categorical_features + numeric_features)

        tmp = self.exp.predict_parts(self.X.iloc[[0]].values, type='shap',
                                     path=list(range(len(self.X.columns)))).result
        self.assertTrue((tmp.loc[tmp.B == 0, 'variable_name'].values == list(self.X.columns)).all())

        _row_count = self.exp.data.shape[0]
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='shap', B=1), alx.predict_explanations.Shap)
        self.assertEqual(_row_count, self.exp.data.shape[0])
        _row_count = self.exp.data.shape[0]
        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='shap', N=100), alx.predict_explanations.Shap)
        self.assertEqual(_row_count, self.exp.data.shape[0])

        self.assertTrue(hasattr(self.exp.predict_parts(self.X.iloc[[0]], type='shap', keep_distributions=True),
                                'yhats_distributions'))

        self.assertIsInstance(
            self.exp.predict_parts(self.X.iloc[[0]], type='shap', keep_distributions=True).yhats_distributions,
            pd.DataFrame)

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='shap', interaction_preference=2),
                              alx.predict_explanations.Shap)

        self.assertIsInstance(self.exp.predict_parts(self.X.iloc[[0]], type='shap', interaction_preference=0.5),
                              alx.predict_explanations.Shap)

    def test_plot(self):
        case1 = self.exp.predict_parts(self.X.iloc[0, :])
        case2 = self.exp2.predict_parts(self.X.iloc[1, :])
        case3 = self.exp.predict_parts(self.X.iloc[2, :], B=10, N=100, type="shap")

        self.assertIsInstance(case1, alx.predict_explanations.BreakDown)
        self.assertIsInstance(case2, alx.predict_explanations.BreakDown)
        self.assertIsInstance(case3, alx.predict_explanations.Shap)

        fig1 = case1.plot(case2, min_max=[0, 1], show=False)
        fig2 = case2.plot((case2, ), max_vars=3, baseline=0.5, show=False)
        fig3 = case3.plot(baseline=0.5, max_vars=3, digits=2, bar_width=12, min_max=[0, 1], show=False)
        fig4 = case3.plot(title="title1", vertical_spacing=0.1, vcolors=("green", "red", "blue"), show=False)
        fig5 = case1.plot(case2, rounding_function=np.ceil, digits=None, max_vars=1, min_max=[0.1, 0.9], show=False)

        self.assertIsInstance(fig1, Figure)
        self.assertIsInstance(fig2, Figure)
        self.assertIsInstance(fig3, Figure)
        self.assertIsInstance(fig4, Figure)
        self.assertIsInstance(fig5, Figure)


if __name__ == '__main__':
    unittest.main()
