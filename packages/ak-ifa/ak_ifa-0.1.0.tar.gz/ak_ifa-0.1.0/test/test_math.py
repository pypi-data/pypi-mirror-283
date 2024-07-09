from unittest import TestCase

from ifa.math import *
import numpy as np

class TestMath(TestCase):

    def assert_arrays_allclose(self,a,b,tol=1e-20):
        np.testing.assert_allclose(a,b,tol,tol)

    def test_math(self):
        self.assertEqual(sigmoid(0), 0.5)
        self.assertTrue(sigmoid(-1) < sigmoid(0))
        self.assertTrue(sigmoid(-100) < sigmoid(-1))
        self.assertTrue(sigmoid(-100) < 1e-10)

        self.assertEqual(clipped_probs(0.99, tau=0.1), 0.90)
        self.assertEqual(clipped_probs(0.01, tau=0.1), 0.1)

        self.assertEqual(logit(0.5), 0)
        self.assertTrue(logit(0.7) > logit(0.6) > logit(0.5))
        self.assertEqual(logit(0.8), logit(0.8, tau=0.2))

        with self.assertRaises(AssertionError) as cm:
            y = np.random.uniform(0,1,size=(10, 2))
            ce(y, y, y)
        self.assertTrue('y needs to be 1 dimensional, got y.shape=(10, 2)' in str(cm.exception))


    def test_sigmoid(self):
        result = sigmoid(0)
        self.assertEqual(result, 0.5)

        x = np.array([-100, -1, 1, 100])
        result = sigmoid(x)
        expected = [0, 1/(1+np.exp(1)), 1/(1+np.exp(-1)), 1]
        self.assert_arrays_allclose(result, expected, 1e-20)

    def test_clipped_probs(self):
        p = np.array([0, 1, 0.3])
        result = clipped_probs(p, tau=0.1)
        expected = np.array([0.1, 0.9, 0.3])
        self.assert_arrays_allclose(result, expected, 1e-20)

    def test_logit(self):
        p = np.array([0.2, 0.5, 0.6])
        result = logit(p)
        expected = np.array([-1.38629436, 0., 0.40546511])
        self.assert_arrays_allclose(result, expected, 1e-8)

    def test_ce_unweighted_single(self):
        y = np.array([0.2])
        p = np.array([0.2])
        w = np.ones(1)
        result = ce(y,p,w)
        expected = -(0.2*np.log(0.2) + 0.8*np.log(0.8))
        self.assert_arrays_allclose(result, expected)

    def test_ce_weighted_single(self):
        y = np.array([0.2])
        p = np.array([0.2])
        w = np.ones(1)*5
        result = ce(y,p,w)
        expected = -(0.2*np.log(0.2) + 0.8*np.log(0.8))
        self.assert_arrays_allclose(result, expected)

    def test_ce_unweighted_multiple(self):
        y = np.array([0.2, 0.8])
        ps = [np.array([0.2, _]) for _ in [0.7, 0.8, 0.9]]
        result = [ce(y, ps_i, np.ones(2)) for ps_i in ps]
        self.assertEqual(result[1], min(result))
    
    def test_objective_a_is_zero(self):
        y = np.array([0, 1, 1])
        p = np.array([0.1, 0.3, 0.3])
        result = objective(0, y, p, np.ones(3))
        expected = ce(y, p, np.ones(3))
        self.assertAlmostEqual(result, expected, 6)

    def test_objective(self):
        y = np.array([0, 1, 1])
        p = np.array([0.1, 0.3, 0.3])
        ce_result = ce(y, p, np.ones(3))
        self.assertTrue(objective(-0.1, y, p, np.ones(3)) > ce_result)
        self.assertTrue(objective(0.1, y, p, np.ones(3)) < ce_result)

    def test_minimizer(self):
        y = np.array([0, 1, 1])
        p = np.array([0.1, 0.3, 0.3])
        result = minimize_ce_with_1param(p, y, np.ones(3))
        orig = ce(p, y, np.ones(3))
        minima = objective(result, y, p, np.ones(3))
        self.assertTrue(minima < orig)



        


