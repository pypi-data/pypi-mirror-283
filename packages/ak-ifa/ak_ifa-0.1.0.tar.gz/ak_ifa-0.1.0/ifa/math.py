from typing import Union, Optional

import numpy as np
from scipy.optimize import minimize

def sigmoid(x: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    """the sigmoid function f(x)=\frac{1}{1+e^-x}
    
    Args:
        x - either a float or a numpy array of numeric values

    Returns:
        float or array, depending on the input
    """
    return 1/(1+np.exp(-x))


def clipped_probs(p: Union[np.ndarray, float], tau: float = 1e-6) -> Union[np.ndarray, float]:
    """
    Symmetrical clipping of probability vectors - 
    used to avoid numerical problems with logs of probablities close to 0,1
    
    Usage:
        >>> p = np.array([0, 1, 0.3])
        >>> clipped_probs(p, tau=0.1)
        returns: array([0.1, 0.9, 0.3])

    Args:
        p - vector with all values within [0,1] or a float within that range
        tau - the symmetric clipping value, must be a float in the range (0,0.5)

    Returns:
        either a vector or float depending on the input
    """
    assert 0 < tau < 0.5
    p = np.clip(p, a_min=tau, a_max=1-tau)
    return p


def logit(p: Union[np.ndarray, float], tau: float = 1e-6) -> Union[np.ndarray, float]:
    """
    The logit function

    Args:
        p - vector with all values within [0,1] or a float within that range
        tau - the symmetric clipping value, must be a float in the range (0,0.5)

    Returns:
        logit value as a float or vector, depending on the input

    """
    p_clipped = clipped_probs(p, tau)
    return np.log(p_clipped/(1-p_clipped))


def ce(y: np.ndarray, p: np.ndarray, w: np.ndarray, tau: float = 1e-6) -> float:
    """"(weighted) cross entropy
    
    Args:
        y - 1-d vector of {0,1} of size n, can also be within the range [0,1]
        p - 1-d vector of probabilities [0,1] of size n
        w - 1-d vector of weights, each w_i > 0 of size n
        tau - the symmetric clipping value, must be a float in the range (0,0.5)
    
    Returns:
        A float denoting the weighted cross entropy

    Raises:
        AssertionError:
          - if vectors are not 1-d
          - weights are not strictly positive
          - any p_i is not within [0,1]
          - any y_i is not within [0,1]    
    """
    assert y.shape[0] == y.reshape(-1).size, f'y needs to be 1 dimensional, got {y.shape=}'
    assert p.shape[0] == p.reshape(-1).size, f'p needs to be 1 dimensional, got {p.shape=}'
    assert w.shape[0] == w.reshape(-1).size, f'w needs to be 1 dimensional, got {w.shape=}'
    w_cond = w > 0
    assert w_cond.all(), f"""weights must be strictly positive, got values: {w[~w_cond]}"""
    p_cond = np.logical_and((0 <= p), (p <= 1))
    y_cond = np.logical_and((0 <= y), (y <= 1))
    assert p_cond.all(), f"""p must be within (0,1), got values: {p[~p_cond]}"""
    assert y_cond.all(), f"""y must be within [0,1], got values: {y[~y_cond]}"""

    p = clipped_probs(p, tau)
    loss = y*np.log(p) + (1-y)*np.log(1-p)
    loss *= w
    return -loss.sum() / w.sum()


def objective(a: float, y: np.ndarray, p: np.ndarray, 
              w: Optional[np.ndarray] = None, tau: float = 1e-6) -> float:
    """IFA's classification objective
     This is parameterized CE with 1 global additive scalar on the logit scale
     
     See documentation for the mathematical details

     Args:
        a - float, the global additive scalar to the CE loss
        y - 1-d vector of {0,1} of size n, can also be within the range [0,1]
        p - 1-d vector of probabilities [0,1] of size n
        w - 1-d vector of weights, each w_i > 0 of size n
        tau - the symmetric clipping value, must be a float in the range (0,0.5)

    Returns:
        a float denoting the CE adjusted by a

    Raises:
        see the documentation for the ifa.math.ce method
     
     """
    if w is None:
        w = np.ones(y.size)
    p_a = sigmoid(logit(p) + a)
    return ce(y, p_a, w, tau)


def minimize_ce_with_1param(p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None, 
                            verbose: bool = False) -> float:
    """given a structure (p,y,w) finds the constant a that will minimize CE
    for a given observation i, the unweighted CE is defined as:
        y_i * log(\sigma(\sigma^{-1}(p_i)+a)) + (1-y_i) * log(1-\sigma(\sigma^{-1}(p_i)+a)))

    Args:
        y - 1-d vector of {0,1} of size n, can also be within the range [0,1]
        p - 1-d vector of probabilities [0,1] of size n
        w - 1-d vector of weights, each w_i > 0 of size n
        verbose - bool, will print the scipy.optimize.OptimizeResult object returned from calling scipy.optimize.mininize
    
    Returns:
        a float denoting the arg that will minimize CE as an added constant in logit scale
    """
    assert p.shape == y.shape

    opt = minimize(fun=objective, x0=np.array([0.0]), args=(y, p, w))
    if verbose:
        print(opt)
    return opt['x'][0]