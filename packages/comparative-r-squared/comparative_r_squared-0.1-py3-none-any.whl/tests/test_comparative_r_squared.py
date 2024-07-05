import unittest
import pandas as pd
import numpy as np
from comparative_r_squared import comparative_r_squared, comparative_r_squared_non_nested, comparative_analysis

class TestComparativeRSquared(unittest.TestCase):
    def test_comparative_r_squared(self):
        R20 = 0.397
        R21 = 0.5
        sample_size = 100
        num_vars_new = 3
        result = comparative_r_squared(R20, R21, sample_size, num_vars_new)
        self.assertIsNotNone(result)
        self.assertTrue('Comparative R Squared' in result.columns)

    def test_comparative_r_squared_non_nested(self):
        R2_combined = 0.8
        R2_a = 0.5
        R2_b = 0.6
        sample_size = 100
        num_vars_new_a = 2
        num_vars_new_b = 3
        result = comparative_r_squared_non_nested(R2_combined, R2_a, R2_b, sample_size, num_vars_new_a, num_vars_new_b)
        self.assertIsNotNone(result)
        self.assertTrue('Model' in result.columns)

    def test_comparative_analysis(self):
        np.random.seed(1)
        Y = np.random.randn(100)
        Xa = pd.DataFrame(np.random.randn(100, 2), columns=['X1', 'X2'])
        Xb = pd.DataFrame(np.random.randn(100, 2), columns=['X2', 'X3'])
        result = comparative_analysis(Y, Xa, Xb)
        self.assertIsNotNone(result)
        self.assertTrue('Model' in result.columns or 'Model Type' in result.columns)

if __name__ == '__main__':
    unittest.main()
