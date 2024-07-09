from abc import ABC, abstractmethod
from typing import Optional, Tuple, Callable, Union

import scipy
import numpy as np
from numpy.random import RandomState

from ifa.math import objective, minimize_ce_with_1param

class ConfidenceIntervalMethod(ABC):

    def __init__(self, alpha: float = 0.05):
        assert 0 < alpha < 1
        self.alpha = alpha

    def ci(self, p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> \
            Tuple[float, float, float, float, int]:
        """returns a tuple (lower, upper, avg, stddev, n)"""
        assert p.reshape(-1).size == p.shape[0]
        assert p.shape == y.shape
        if w is None:
            w = np.ones(p.size)
        else:
            assert w.shape == y.shape
        assert ~np.isnan(p).any(), f"""no nans allowed in p"""
        assert ~np.isnan(w).any(), f"""no nans allowed in w"""
        assert ~np.isnan(y).any(), f"""no nans allowed in y"""

        return self._ci_implementation(p, y, w)

    @abstractmethod
    def _ci_implementation(self, p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> \
            Tuple[float, float, float, float, int]:
        pass


class PointEstimateMethod(ConfidenceIntervalMethod):

    def _ci_implementation(self, p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> \
            Tuple[float, float, float, float, int]:
        n = p.size
        a = minimize_ce_with_1param(p, y, w)
        return a, a, a, np.nan, n


class LikelihoodRatioConfidenceIntervalMethod(ConfidenceIntervalMethod):

    def __init__(self, alpha: float = 0.05,
                 tol: float = 1e-10,
                 max_iter: Optional[int] = None,
                 verbose: bool = False):
        super().__init__(alpha)
        assert 0 < tol < 0.1
        self.tol = tol
        self.max_iter = max_iter
        self.verbose = verbose

    @staticmethod
    def log_likelihood_ratio(a_opt: float, p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None):
        def f(a: float):
            ratio = objective(a, y, p, w) / objective(a_opt, y, p, w)
            llr = -2*np.log(ratio)
            return -llr if a >= a_opt else llr
        return f

    @staticmethod
    def bisection(target: float, f: Callable[[float], float],
                  x_lo: float, x_hi: float, tol: float = 1e-10,
                  max_iter: Optional[int] = 100,
                  verbose: bool = False):
        i = 0
        while abs(x_lo - x_hi) > tol and (True if max_iter is None else i <= max_iter):
            if verbose:
                print(f'bisection {i=}, {x_lo=}, {x_hi=}, diff={abs(x_lo - x_hi)}')
            ad = abs(x_lo - x_hi)
            f_lo = f(x_lo)
            f_hi = f(x_hi)
            if target <= f_lo:
                x_hi = x_lo
                x_lo = x_lo - ad
            elif f_lo < target < f_hi:
                x_lo = (x_lo + x_hi)*0.5
            else:
                x_lo = x_hi
                x_hi = x_lo + ad
            i += 1
        return (x_lo + x_hi)*0.5

    def _ci_implementation(self, p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> \
            Tuple[float, float, float, float, int]:
        a_opt = minimize_ce_with_1param(p, y, w)
        chi2 = scipy.stats.chi2(1)
        chi2_q = chi2.ppf(1-self.alpha)
        llr = self.log_likelihood_ratio(a_opt, p, y, w)

        upper = self.bisection(chi2_q, llr, a_opt, a_opt+4, self.tol, max_iter=self.max_iter, verbose=self.verbose)
        lower = self.bisection(-chi2_q, llr, a_opt, a_opt+4, self.tol, max_iter=self.max_iter, verbose=self.verbose)

        return lower, upper, a_opt, np.nan, p.size


class BootstrapConfidenceIntervalMethod(ConfidenceIntervalMethod):

    def __init__(self, alpha: float = 0.05, n_samples: int = 10, seed: Union[int, RandomState] = 4242):
        super().__init__(alpha)
        assert isinstance(n_samples, int)
        assert n_samples > 0
        self.n_samples = n_samples
        self.rs = self._resolve_random_state(seed)

    @staticmethod
    def _resolve_random_state(seed: int = Union[int, RandomState]) -> RandomState:
        if isinstance(seed, int):
            return RandomState(seed)
        elif isinstance(seed, RandomState):
            return seed
        else:
            raise TypeError(f'seed needs to be either [int, RandomState], got {str(type(seed))}')

    def bootstrap_indices(self, n: int):
        return self.rs.choice(range(n), size=(n, self.n_samples), replace=True)

    def bootstrap_results(self, p: np.ndarray, y: np.ndarray, w: np.ndarray):
        pyw = np.column_stack([p, y, w])
        n = pyw.shape[0]
        results = []

        indices = self.bootstrap_indices(n)

        for i in range(self.n_samples):
            sample_i = pyw[indices[:, i], :]
            _p, _y, _w = sample_i[:, 0], sample_i[:, 1], sample_i[:, 2]
            a = minimize_ce_with_1param(_p, _y, _w)
            results.append(a)

        return np.array([results])

    def _ci_implementation(self, p: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> \
            Tuple[float, float, float, float, int]:

        results = self.bootstrap_results(p, y, w)
        lower = np.percentile(results, 100*self.alpha/2)
        upper = np.percentile(results, 100*(1-self.alpha/2))
        avg = results.mean()
        std = results.std()
        return lower, upper, avg, std, p.size