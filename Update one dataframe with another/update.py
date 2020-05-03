"""
Parameters

1.  otherDataFrame, or object coercible into a DataFrame
    Should have at least one matching index/column label with the original DataFrame. If a Series is passed, its name attribute must be set, and that will be used as the column name to align with the original DataFrame.

2.  join{‘left’}, default ‘left’
    Only left join is implemented, keeping the index and columns of the original object.

3.  overwritebool, default True
    How to handle non-NA values for overlapping keys:

        True: overwrite original DataFrame’s values with values from other.

        False: only update values that are NA in the original DataFrame.

4.  filter_funccallable(1d-array) -> bool 1d-array, optional
    Can choose to replace values other than NA. Return True for values that should be updated.

5.  errors{‘raise’, ‘ignore’}, default ‘ignore’
    If ‘raise’, will raise a ValueError if the DataFrame and other both contain non-NA data in the same place.

    Changed in version 0.24.0: Changed from raise_conflict=False|True to errors=’ignore’|’raise’.

Returns
Nonemethod directly changes calling object
"""
import pandas as pd
import numpy as np


np.random.seed(12345)
a = pd.DataFrame({"stkcd": [1, 1, 1, 2, 2, 2], "year": [2010, 2011, 2012, 2010, 2011, 2012], "value": np.random.randn(6)})
b = pd.DataFrame({"stkcd": [1, 1, 1, 2, 2, 2], "year": [2010, 2011, 2012, 2010, 2011, 2012], "value": np.random.randn(6)})
a.loc[2:4, "value"] = np.nan

a = a.set_index(["stkcd", "year"])
b = b.set_index(["stkcd", "year"])
tmp = a.copy()
tmp.update(b, overwrite=False)

tmp = a.copy()
tmp.update(b, filter_func=lambda x: x >= 0)

tmp = a.copy()
tmp.update(b, filter_func=lambda x: np.array(list(pd.isna(x)) or list(x >= 0)))

tmp = a.copy()
tmp.update(b, filter_func=lambda x: pd.isna(x) | (x >= 0))