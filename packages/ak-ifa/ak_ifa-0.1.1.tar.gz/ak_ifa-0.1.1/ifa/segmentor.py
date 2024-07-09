from abc import ABC, abstractmethod
from typing import Optional
from collections import Counter

import numpy as np

class AbstractSegmentor(ABC):
    """
    IFA segments the data into groups in order to assess the potential improvement in CE in that area
    The AbstractSegmentor is the abstract segmentor class, any concrete class needs to 
    implement the _fit and _segment_implementation methods.
    """

    def __init__(self):
        self.state = None
    
    def segment(self, v: np.ndarray, _i: int) -> np.ndarray:
        """
        Args:
            v - is a k dimensional array.
            _i - is the index that we want to segment by.
        Returns:
            a k+1 dimensional array with:
                - original v in the first k columns
                - a mapping of x to segments in the k+1 column
                Values of np.nans will be mapped into -1"""
        assert 0 <= _i <= v.shape[1] - 1
        n, k = v.shape
        mask = ~np.isnan(v[:,_i])
        xnn = v[mask, :]
        if self.state is None:
            self._fit(xnn, _i)
        
        no_nan_result = self._segment_implementation(xnn, _i)
        assert no_nan_result.shape[1] == k + 1, f'num of cols in no_nan_result={no_nan_result.shape[1]}, ' \
                                                f'expecting {k+1}'
        assert no_nan_result.shape[0] == mask.sum()
        nan_result = v[~mask, :]
        nan_result = np.column_stack([nan_result, -np.ones(n-mask.sum())])
        result = np.row_stack([no_nan_result, nan_result])

        return result

    @abstractmethod
    def _fit(self, x: np.ndarray, i: int):
        pass

    @abstractmethod
    def _segment_implementation(self, x: np.ndarray, i: int) -> np.ndarray:
        pass


class CategoricalSegmentor(AbstractSegmentor):

    def __init__(self, top_k: Optional[int]=None, other_category_name: str='_other_'):
        super().__init__()
        if top_k is not None:
            assert top_k > 0, f'`top_k` must be greater than 0 or None, got {top_k=}'
        self.top_k = top_k
        self.other_category_name = other_category_name

    @staticmethod
    def is_nan(v):
        if v is None:
            return True
        elif isinstance(v, (str,)):
            return v == 'nan'
        elif isinstance(v, (float, int)):
            return np.isnan(v)
        else:
            raise ValueError(f'unrecognized type: {v=}, {type(v)=}')

    def segment(self, v: np.ndarray, _i: int) -> np.ndarray:
        nan_mask = np.array([self.is_nan(v_i) for v_i in v[:, _i].tolist()])
        v_nan = v[nan_mask,:]
        n_nan = v_nan.shape[0]
        v_no_nan = v[~nan_mask,:]
        if self.state is None:
            self._fit(v_no_nan, _i)
        
        def _class(x_i):
            if x_i in self.state:
                return self.state[x_i]
            elif x_i is None:
                return -1
            else:
                return 0 # other
            
        s = v_no_nan[:, _i].tolist()
        ss = np.array(list(map(_class, s)))
        ret = np.column_stack([v_no_nan, ss])
        ret_nan = np.column_stack([v_nan, [-1]*n_nan])
        result = np.row_stack([ret, ret_nan])
        result[result[:,-1] == 0, 0] = self.other_category_name
        return result

    def _segment_implementation(self, x: np.ndarray, i: int) -> np.ndarray:
        pass

    def _fit(self, x: np.ndarray, i: int):
        c = Counter(x[:, i])
        c = sorted(c.items(), key=lambda t: -t[1])
        if self.top_k is not None:    
            c = c[:self.top_k]
            c = list(map(lambda t: t[0], c))
        else:
            c = [k for k,v in c]

        self.state = {k: j+1 for j, k in enumerate(c)}
        

class NtileSegmentor(AbstractSegmentor):

    def __init__(self, tiles: int = 10):
        super().__init__()
        assert tiles > 0
        self.tiles = tiles

    def _fit(self, array: np.ndarray, i: int):
        percentiles = np.linspace(0, 100, self.tiles + 1)
        self.state = np.percentile(array[:, i], percentiles)

    def _segment_implementation(self, array: np.ndarray, i: int):
        tile_values = self.state
        mapped_array = np.zeros((array.shape[0], array.shape[1]+1))
        mapped_array[:, :array.shape[1]] = array

        for j in range(1, self.tiles + 1):
            indices = np.logical_and(array[:, i] >= tile_values[j - 1], array[:, i] <= tile_values[j])
            mapped_array[indices, array.shape[1]] = j

        return mapped_array