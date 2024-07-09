from typing import Union

from unittest import TestCase

from scipy.optimize import minimize
import numpy as np
from numpy.random import RandomState

from ifa.api import *
from ifa.math import sigmoid
from ifa.demo import model_samples, fit_logistic_regression


class TestApi(TestCase):
   
    def test_example(self):
        k = 5
        rs = RandomState(333)
        beta = rs.uniform(-5,5,k)
        X, y, beta = model_samples(50000, beta) # missing 1 feature

        beta_hat = fit_logistic_regression(X, y)
        error = np.pow(beta - beta_hat,2).mean()
        print(f"beta error: {error}")

        X_partial = X[:,:(k-1)]
        beta_hat_partial = fit_logistic_regression(X_partial, y)
        p = sigmoid(X_partial.dot(beta_hat_partial))
        df = pd.DataFrame({'x':X[:,k-1], 'y': y, 'p': p})
        result, _ = analyze_feature(df, x_col='x', p_col='p', y_col='y', plot=False)
        result = result['bias']
        expected = np.array([ 1.114955,0.801960,0.627544,0.315205,0.136839,
                             -0.115860,-0.329878,-0.578883,-0.884712,-1.074554])
        np.testing.assert_allclose(result, expected, atol=1e-6, rtol=1e-6)

        