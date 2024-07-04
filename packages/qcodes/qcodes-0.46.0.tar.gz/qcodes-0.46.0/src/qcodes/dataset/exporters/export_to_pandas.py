from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping

    import pandas as pd

    from qcodes.dataset.data_set_protocol import ParameterData


def load_to_dataframe_dict(datadict: ParameterData) -> dict[str, pd.DataFrame]:
    dfs = {}
    for name, subdict in datadict.items():
        index = _generate_pandas_index(subdict)
        dfs[name] = _data_to_dataframe(subdict, index)
    return dfs


def load_to_concatenated_dataframe(datadict: ParameterData) -> pd.DataFrame:
    import pandas as pd

    if not _same_setpoints(datadict):
        warnings.warn(
            "Independent parameter setpoints are not equal. "
            "Check concatenated output carefully. Please "
            "consider using `to_pandas_dataframe_dict` to export each "
            "independent parameter to its own dataframe."
        )

    dfs_dict = load_to_dataframe_dict(datadict)
    df = pd.concat(list(dfs_dict.values()), axis=1)

    return df


def _data_to_dataframe(
    data: Mapping[str, np.ndarray], index: pd.Index | pd.MultiIndex | None
) -> pd.DataFrame:
    import pandas as pd
    if len(data) == 0:
        return pd.DataFrame()
    dependent_col_name = list(data.keys())[0]
    dependent_data = data[dependent_col_name]
    if dependent_data.dtype == np.dtype('O'):
        # ravel will not fully unpack a numpy array of arrays
        # which are of "object" dtype. This can happen if a variable
        # length array is stored in the db. We use concatenate to
        # flatten these
        mydata = np.concatenate(dependent_data)
    else:
        mydata = dependent_data.ravel()
    df = pd.DataFrame(mydata, index=index,
                      columns=[dependent_col_name])
    return df


def _generate_pandas_index(
    data: Mapping[str, np.ndarray]
) -> pd.Index | pd.MultiIndex | None:
    # the first element in the dict given by parameter_tree is always the dependent
    # parameter and the index is therefore formed from the rest
    import pandas as pd
    keys = list(data.keys())
    if len(data) <= 1:
        index = None
    elif len(data) == 2:
        index = pd.Index(data[keys[1]].ravel(), name=keys[1])
    else:
        index_data = []
        for key in keys[1:]:
            if data[key].dtype == np.dtype("O"):
                # if we have a numpy array of dtype object,
                # it could either be a variable length array
                # in which case we concatenate it, or it could
                # be a numpy array of scalar objects.
                # In the latter case concatenate will fail
                # with a value error but ravel will produce the
                # correct result
                try:
                    index_data.append(np.concatenate(data[key]))
                except ValueError:
                    index_data.append(data[key].ravel())
            else:
                index_data.append(data[key].ravel())

        index = pd.MultiIndex.from_arrays(
            index_data,
            names=keys[1:])
    return index


def _parameter_data_identical(
    param_dict_a: Mapping[str, np.ndarray], param_dict_b: Mapping[str, np.ndarray]
) -> bool:

    try:
        np.testing.assert_equal(param_dict_a, param_dict_b)
    except AssertionError:
        return False

    return True


def _same_setpoints(datadict: ParameterData) -> bool:

    def _get_setpoints(dd: ParameterData) -> Iterator[dict[str, np.ndarray]]:

        for dep_name, param_dict in dd.items():
            out = {
                name: vals for name, vals in param_dict.items() if name != dep_name
            }
            yield out

    sp_iterator = _get_setpoints(datadict)

    try:
        first = next(sp_iterator)
    except StopIteration:
        return True

    return all(_parameter_data_identical(first, rest) for rest in sp_iterator)
