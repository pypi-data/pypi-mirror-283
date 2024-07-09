from typing import Optional, Tuple

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from ifa.math import sigmoid, logit
from ifa.segmentor import *
from ifa.ci import *


def plot_result(result: pd.DataFrame, x_col: Optional[str]=None,
                y_axis: str='bias',
                figsize: Tuple[int, int]=(10, 4),
                width_ratios: Tuple[int, int]=(1, 10),
                color = 'blue',
                ax: Optional[np.ndarray]=None):
    if ax is None:
        _, ax = plt.subplots(1,2, figsize=figsize, gridspec_kw={'width_ratios': [*width_ratios]}, sharey=True)
    ax = ax.ravel()

    _y_axis = result['bias']
    ymin = result['bias_lower']
    ymax = result['bias_upper']
    if y_axis == 'bias':
        pass
    elif y_axis == 'mape':
        def _mape(key):
            s = np.abs(result['p_q50'] - sigmoid(logit(result['p_q50']) + result[key]))
            s /= result['p_q50']
            s = s.mean()
            return s
        _y_axis = _mape('bias')
        ymin = _mape('bias_lower')
        ymax = _mape('bias_upper')     
    else:
        raise Exception(f'unrecognized option {y_axis=}')

    null_msk = result['i'] == -1
    _n_null = _y_axis[null_msk].size

    # x null bias plot
    ax[0].axhline(0, linestyle='--', color='gray')
    if np.any(null_msk):
        ax[0].scatter([0]*_n_null, _y_axis[null_msk], color=color, s=8)
        ax[0].vlines([0]*_n_null, ymin=ymin[null_msk], ymax=ymax[null_msk], color=color)
    ax[0].set_ylabel('bias')
    ax[0].get_xaxis().set_ticks([])
    ax[0].set_xlabel('Nulls')

    # x defined bias plot
    ax[1].axhline(0, linestyle='--', color='gray')
    ax[1].scatter(result.loc[~null_msk, 'x_mid'], _y_axis[~null_msk], color=color, s=8)
    ax[1].vlines(result.loc[~null_msk, 'x_mid'], ymin=ymin[~null_msk], ymax=ymax[~null_msk], color=color)
    ax[1].set_xlabel(x_col if x_col is not None else 'x')

    # categorical values
    if 'x_cat' in result.columns:
        ax[1].set_xticks(result.loc[~null_msk, 'x_mid'])
        ax[1].set_xticklabels(result.loc[~null_msk, 'x_cat'])

    plt.show()
    return ax


def analyze_feature(df: pd.DataFrame, x_col: str, p_col: str, y_col: str, w_col: Optional[str] = None,
                    segmentor: AbstractSegmentor = NtileSegmentor(),
                    ci_method: Optional[ConfidenceIntervalMethod] = BootstrapConfidenceIntervalMethod(),
                    plot: bool = True,
                    **plot_args) -> Tuple[pd.DataFrame, Optional[Axes]]:
    """
    Graphical test for the incremental predictive power of a feature over an existing probability model
    :param df: a pandas dataframe that contains columns that are (at least) the feature of interest,
        the prediction from a probabilistic model
        and the labels for analysis
    :param x_col: the name of the column with the feature (may contain Nans)
    :param p_col: the name of the column with the model predictions (no Nans allowed)
    :param y_col: the name of the column with the labels (no Nans allowed)
    :param w_col: an optional weight column, weights must be strictly positive
    :param segmentor: any AbstractSegmentor that will segment the feature, default is NtileSegmentor
    :param ci_method: any ConfidenceIntervalMethod, uses BootstrapConfidenceIntervalMethod by default
    :return: a dataframe with columns:
        i - denoting the segment's identifier, this would go from 0 to [num segments - 1], it will include a -1 for Nans
        x_min/x_max - the lowest/highest value of x in the segment
        bias_lower/bias_upper - according to the ci_method, these will be lower and upper confidence bounds of the bias (a)
        bias - the point estimate of the bias
        bis_std - only relevant for certain ci_methods
        n - the number of samples in the segment
        w - the sum of weights in the segments

    """
    x = df[x_col].values
    p = df[p_col].values
    y = df[y_col].values
    w = df[w_col] if w_col is not None else np.ones(df.shape[0])
    assert x.reshape(-1).size == x.shape[0]
    assert x.shape == y.shape
    assert p.shape == y.shape
    if w is None:
        w = np.ones(p.size)
    else:
        assert w.shape == y.shape
    assert ~np.isnan(p).any(), f"""no nans allowed in p"""
    assert ~np.isnan(w).any(), f"""no nans allowed in w"""
    assert ~np.isnan(y).any(), f"""no nans allowed in y"""

    xpyw = np.column_stack([x, p, y, w])
    s = segmentor.segment(xpyw, 0) # s has the the structure (x,p,y,w,segment)
    result = []

    for i in np.unique(s[:, -1]):
        s_i = s[s[:, -1] == i, :4] 
        r_i = {'i': i}
        lower, upper, avg, std, n = ci_method.ci(s_i[:, 1].astype(np.float64), 
                                                 s_i[:, 2].astype(np.float64), 
                                                 s_i[:, 3].astype(np.float64))
        if isinstance(segmentor, CategoricalSegmentor):
            r_i['x_cat'] = s_i[0, 0]
            r_i['x_mid'] = i
        else:
            r_i['x_min'] = s_i[:, 0].min()
            r_i['x_max'] = s_i[:, 0].max()
            r_i['x_mid'] = (r_i['x_min'] + r_i['x_max'])*0.5        

        r_i['bias_lower'] = lower
        r_i['bias_upper'] = upper
        r_i['bias'] = avg
        r_i['bias_std'] = std
        r_i['n'] = n
        r_i['w'] = s_i[:, 3].sum()
        r_i['p_q10'] = np.percentile(s_i[:, 1], 10)
        r_i['p_q25'] = np.percentile(s_i[:, 1], 25)
        r_i['p_q50'] = np.percentile(s_i[:, 1], 50)
        r_i['p_q75'] = np.percentile(s_i[:, 1], 75)
        r_i['p_q90'] = np.percentile(s_i[:, 1], 90)
           
        result.append(pd.Series(r_i))
    
    result = pd.DataFrame(result)
    if plot:
        ax = plot_result(result, **plot_args)

    return result, ax if plot else None