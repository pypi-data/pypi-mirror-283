import pandas as pd
from scipy.stats import chi2
import numpy as np
import statsmodels.api as sm

def validate_inputs(R20, R21, sample_size, num_vars_new):
    if not (0 <= R20 <= 1):
        raise ValueError("R20 must be between 0 and 1.")
    if not (0 <= R21 <= 1):
        raise ValueError("R21 must be between 0 and 1.")
    if sample_size <= 0:
        raise ValueError("Sample size must be a positive integer.")
    if num_vars_new <= 0:
        raise ValueError("Number of new variables must be a positive integer.")
    if R21 < R20:
        raise ValueError("R21 must be greater than or equal to R20.")

def comparative_r_squared(R20, R21, sample_size, num_vars_new):
    validate_inputs(R20, R21, sample_size, num_vars_new)
    R2C = (R21 - R20) / (1 - R20)
    chi_square_stat = sample_size * R2C
    p_value = 1 - chi2.cdf(chi_square_stat, df=num_vars_new)
    results = pd.DataFrame({
        'Comparative R Squared': [R2C],
        'Chi-Square Statistic': [chi_square_stat],
        'p-value': [p_value],
        'Number of new variables': [num_vars_new]
    })
    return results

def comparative_r_squared_non_nested(R2_combined, R2_a, R2_b, sample_size, num_vars_new_a, num_vars_new_b):
    validate_inputs(R2_b, R2_combined, sample_size, num_vars_new_a)
    validate_inputs(R2_a, R2_combined, sample_size, num_vars_new_b)
    R2_unique_a = R2_combined - R2_b
    R2_unique_b = R2_combined - R2_a
    R2_shared = R2_a + R2_b - R2_combined
    R2C_a = (R2_combined - R2_b) / (1 - R2_b)
    R2C_b = (R2_combined - R2_a) / (1 - R2_a)
    chi_square_stat_a = sample_size * R2C_a
    chi_square_stat_b = sample_size * R2C_b
    p_value_a = 1 - chi2.cdf(chi_square_stat_a, df=num_vars_new_a)
    p_value_b = 1 - chi2.cdf(chi_square_stat_b, df=num_vars_new_b)
    results = pd.DataFrame({
        'Model': ['a', 'b'],
        'R Squared': [R2_a, R2_b],
        'Combined and shared R squared': [R2_combined, R2_shared],
        'Unique R Squared': [R2_unique_a, R2_unique_b],
        'Comparative R Squared': [R2C_a, R2C_b],
        'Chi-Square Statistic': [chi_square_stat_a, chi_square_stat_b],
        'p-value': [p_value_a, p_value_b],
        'Number of new variables': [num_vars_new_a, num_vars_new_b]
    })
    return results

def run_regression(Y, X):
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    return model.rsquared

def determine_nested(Xa, Xb):
    return set(Xa.columns).issubset(set(Xb.columns)) or set(Xb.columns).issubset(set(Xa.columns))

def comparative_analysis(Y, Xa, Xb):
    nested = determine_nested(Xa, Xb)
    R2_a = run_regression(Y, Xa)
    R2_b = run_regression(Y, Xb)
    if nested:
        R2_combined = max(R2_a, R2_b)
        num_vars_new = abs(len(Xa.columns) - len(Xb.columns))
        R2C = (R2_combined - min(R2_a, R2_b)) / (1 - min(R2_a, R2_b))
        sample_size = len(Y)
        chi_square_stat = sample_size * R2C
        p_value = 1 - chi2.cdf(chi_square_stat, df=num_vars_new)
        results = pd.DataFrame({
            'Model Type': ['Nested'],
            'R2 Model a': [R2_a],
            'R2 Model b': [R2_b],
            'Comparative R Squared': [R2C],
            'Chi-Square Statistic': [chi_square_stat],
            'p-value': [p_value],
            'Number of new variables': [num_vars_new]
        })
    else:
        combined_cols = pd.concat([Xa, Xb], axis=1).loc[:,~pd.concat([Xa, Xb], axis=1).columns.duplicated()]
        R2_combined = run_regression(Y, combined_cols)
        num_vars_new_a = len(combined_cols.columns) - len(Xb.columns)
        num_vars_new_b = len(combined_cols.columns) - len(Xa.columns)
        R2_unique_a = R2_combined - R2_b
        R2_unique_b = R2_combined - R2_a
        R2_shared = R2_a + R2_b - R2_combined
        R2C_a = (R2_combined - R2_b) / (1 - R2_b)
        R2C_b = (R2_combined - R2_a) / (1 - R2_a)
        sample_size = len(Y)
        chi_square_stat_a = sample_size * R2C_a
        p_value_a = 1 - chi2.cdf(chi_square_stat_a, df=num_vars_new_a)
        chi_square_stat_b = sample_size * R2C_b
        p_value_b = 1 - chi2.cdf(chi_square_stat_b, df=num_vars_new_b)
        results = pd.DataFrame({
            'Model': ['a', 'b'],
            'R Squared': [R2_a, R2_b],
            'Combined and shared R squared': [R2_combined, R2_shared],
            'Unique R Squared': [R2_unique_a, R2_unique_b],
            'Comparative R Squared': [R2C_a, R2C_b],
            'Chi-Square Statistic': [chi_square_stat_a, chi_square_stat_b],
            'p-value': [p_value_a, p_value_b],
            'Number of new variables': [num_vars_new_a, num_vars_new_b]
        })
    return results
