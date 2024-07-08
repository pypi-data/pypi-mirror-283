import unittest
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import affectlog as alx
from plotly.graph_objs import Figure


class ModelPerformanceTestSkills(unittest.TestCase):
    def setUp(self):
        # Load the Skills dataset and preprocess it
        data = alx.datasets.load_skills()  # Assuming load_skills() is a generic function to load the dataset
        data['target'] = pd.cut(data['target'], bins=2, labels=[0, 1])  # Simplify target variable for binary classification

        self.X = data.drop(columns='target')
        self.y = data['target']

        numeric_features = ['numerical_feature1', 'numerical_feature2', 'numerical_feature3']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_features = ['categorical_feature1', 'categorical_feature2']
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

    def test_constructor(self):
        # Test model performance for classification
        case1 = self.exp.model_performance('classification')
        self.assertIsInstance(case1, (alx.model_explanations.ModelPerformance,))
        self.assertIsInstance(case1.result, (pd.DataFrame,))
        self.assertEqual(case1.result.shape[0], 1)
        self.assertTrue(np.isin(['recall', 'precision', 'f1', 'accuracy', 'auc'], case1.result.columns).all())

    def test_plot(self):
        # Test plotting of model performance
        case1 = self.exp.model_performance('classification')
        case2 = self.exp2.model_performance('classification')

        self.assertIsInstance(case1, alx.model_explanations.ModelPerformance)
        self.assertIsInstance(case2, alx.model_explanations.ModelPerformance)

        fig1 = case1.plot(title="test1", show=False)
        fig2 = case2.plot(case1, show=False)
        fig3 = case1.plot(case2, geom="roc", show=False)
        fig4 = case2.plot(case1, geom="lift", show=False)

        self.assertIsInstance(fig1, Figure)
        self.assertIsInstance(fig2, Figure)
        self.assertIsInstance(fig3, Figure)
        self.assertIsInstance(fig4, Figure)


if __name__ == '__main__':
    unittest.main()
