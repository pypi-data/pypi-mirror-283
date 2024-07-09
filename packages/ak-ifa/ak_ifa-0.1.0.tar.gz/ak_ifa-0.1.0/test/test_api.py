from typing import Union

from unittest import TestCase

from scipy.optimize import minimize
import numpy as np
from numpy.random import RandomState

from ifa.api import *
from ifa.math import sigmoid

def model_samples(n: int, beta: Union[int, np.ndarray], seed: Union[int, RandomState]=556342):
    """creates n random instances based on beta"""
    assert n > 0

    # resolve beta
    if isinstance(beta, int):
        beta = np.random.uniform(-1, 1, size=beta)
    elif isinstance(beta, np.ndarray):
        assert beta.size == beta.shape[0]
    else:
        raise TypeError()
    
    # resolve random state
    if isinstance(seed, int):
        rs = RandomState(seed)
    elif isinstance(seed, RandomState):
        rs = seed
    else:
        raise TypeError()
        
    p = beta.size

    x = rs.uniform(low=-1, high=1, size=(n, p))
    
    xb = x.dot(beta)
    p = sigmoid(xb)
    y = rs.binomial(1, p)
    
    return x, y, beta

def crossentropy_loss(x, X, y):
    mu = X.dot(x)
    y_hat = sigmoid(mu)
    return -(y*np.log(y_hat) + (1-y)*np.log(1-y_hat)).mean()

def fit_logistic_regression(X, y):
    opt = minimize(crossentropy_loss, np.zeros(X.shape[1]), (X, y))
    return opt['x']


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

        