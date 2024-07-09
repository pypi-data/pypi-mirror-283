from typing import Union
import numpy as np
from numpy.random import RandomState

from ifa.math import sigmoid, ce
from scipy.optimize import minimize

def model_samples(n: int, beta: Union[int, np.ndarray], seed: Union[int, RandomState]=556342):
    """creates n random instances based on beta
    
    Args:
        n - number of samples
        beta - 1-d array, predetermined feature vector
        seed - RandomState or int to control the randomness

    Returns:
        if beta is of size k, returns a tuple of 3 elements:
         - 2-d array of shape (n,k) denoting the feature
         - 1-d array of labels, size n
         - the beta vector used to create the data
    """
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

    X = rs.uniform(low=-1, high=1, size=(n, p))
    
    mu = X.dot(beta)
    p = sigmoid(mu)
    y = rs.binomial(1, p)
    
    return X, y, beta

def ce_loss(x, X, y):
    """calls afi.math's ce method, but uses x as the coefficients
    
    Args:
        x - 1-d array, of size k denoting the model coefficients
        X - 2-d array of features, shape should be (n,k)
        y - 1-d array of labels, size should be n
    """
    k = x.size
    n = X.shape[0]
    
    assert len(X.shape) == 2
    assert X.shape[1] == k
    assert y.size == n

    mu = X.dot(x)
    y_hat = sigmoid(mu)
    return ce(y, y_hat, np.ones(y_hat.size))
    

def fit_logistic_regression(X, y):
    """using straight forward minimization to solve for logistic regression - only for demos
    Args:
        X - 2-d array of features, shape should be (n,k)
        y - 1-d array of labels, size should be n

    Returns:
        1-d array of weights of size k
    """
    opt = minimize(ce_loss, np.zeros(X.shape[1]), (X, y))
    return opt['x']