import unittest
import pandas as pd
import statsmodels.api as sm
from OLS_pipeline.pipeline import preprocess_data, fit_models, calculate_vif, pipeline


class TestPipeline(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        data = {
            'Country': ['A', 'A', 'B', 'B'],
            'Year': [2020, 2021, 2020, 2021],
            'Stringency Index': [50, 60, 70, 80],
            'Covid Cases': [1000, 1500, 2000, 2500],
            'Covid Death': [50, 60, 70, 80],
            'Financial Development': [0.5, 0.6, 0.7, 0.8],
            'Green Bond Issuance': [10, 20, 30, 40],
            'GDP Growth': [2, 3, 4, 5],
            'Conventional Bond Issuance': [100, 200, 300, 400]
        }
        self.df = pd.DataFrame(data)

    def test_preprocess_data(self):
        X_scaled = preprocess_data(self.df)
        self.assertEqual(X_scaled.shape[1], len(self.df.columns))  # Check if all columns are present

    def test_fit_models(self):
        X_scaled = preprocess_data(self.df)
        fixed_effects_results, random_effects_model = fit_models(X_scaled)
        self.assertIsNotNone(fixed_effects_results)  # Check if the model is fitted
        self.assertIsNotNone(random_effects_model)  # Check if the model is fitted

    def test_calculate_vif(self):
        X_scaled = preprocess_data(self.df)
        vif_data = calculate_vif(sm.add_constant(X_scaled[['COVID_Impact_Measure', 'GDP Growth', 'Financial Development', 'Conventional Bond Issuance']]))
        self.assertGreater(len(vif_data), 0)  # Check if VIF data is calculated

    def test_pipeline(self):
        self.df.to_csv("test_data.csv", index=False)
        fixed_effects_results, random_effects_model, vif_data, X_scaled = pipeline("test_data.csv")
        self.assertIsNotNone(fixed_effects_results)  # Check if the model is fitted
        self.assertIsNotNone(random_effects_model)  # Check if the model is fitted
        self.assertGreater(len(vif_data), 0)  # Check if VIF data is calculated

if __name__ == '__main__':
    unittest.main()
