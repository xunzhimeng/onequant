"""Wash data for portfolio analyze."""

import numpy as np
import pandas as pd


def fill_date(
    strategy_id=None,
    data=None,
    need_start=pd.Timestamp('2015-01-01', tz='UTC'),
    need_end=pd.Timestamp('2023-04-15', tz='UTC'),
    time_column='ts',
    netvalue_column='net_value',
):
    """Fills missing dates in a pandas DataFrame with specified values.

    Args:
        strategy_id (int): The ID of the strategy.
        data (pandas.DataFrame): The DataFrame to fill missing dates in.
        need_start (pandas.Timestamp): The start date to fill missing dates from.
        need_end (pandas.Timestamp): The end date to fill missing dates to.
        time_column (str): The name of the column containing the timestamps.
        netvalue_column (str): The name of the column containing the net values.

    Returns:
        pandas.DataFrame: The DataFrame with missing dates filled in.
    """

    def _fill_date(data, start, end, fill_data, is_pre=False):
        """Fills missing dates in a pandas DataFrame with specified values.

        Args:
            data (pandas.DataFrame): The DataFrame to fill missing dates in.
            start (pandas.Timestamp): The start date to fill missing dates from.
            end (pandas.Timestamp): The end date to fill missing dates to.
            fill_data (int): The value to fill missing data with.
            is_pre (bool): Whether the missing dates are before the start date.

        Returns:
            pandas.DataFrame: The DataFrame with missing dates filled in.
        """
        missing_dates = pd.date_range(start=start, end=end, freq='D')
        missing_data = pd.DataFrame()
        missing_data[time_column] = missing_dates
        missing_data[netvalue_column] = fill_data
        missing_data.set_index(time_column, inplace=True)
        missing_data.index = missing_data.index.tz_localize(None).floor('D')
        data = pd.concat([missing_data, data] if is_pre else [data, missing_data], ignore_index=False)
        data.ffill()
        return data

    data_start = data.index[0].tz_localize('UTC')
    data_end = data.index[-1].tz_localize('UTC')
    if data_start > need_start:
        data_start = data_start - pd.Timedelta('1 days')
        data = _fill_date(data, need_start, data_start, 1, True)
    if data_end < need_end:
        data_end = data_end + pd.Timedelta('1 days')
        data = _fill_date(data, data_end, need_end, data[netvalue_column].iloc[-1], False)
    return data


def filter_returns_by_weights(returns, weights, min_weights=0.005):
    """This function filters the returns by weights.

    Parameters:
    -----------
    returns: pandas dataframe.
        A dataframe containing the returns.
    weights: pandas dataframe.
        A dataframe containing the weights.
    min_weights: float, default: 0.005.
        The minimum weight.

    Returns:
    --------
    cumulative_return: pandas dataframe.
        A dataframe containing the cumulative return.
    """
    selected_weights = weights.loc[weights['weights'] > min_weights]
    selected_returns = returns[selected_weights.index]
    weighted_return = selected_returns.mul(selected_weights['weights'])
    portfolio_return = weighted_return.sum(axis=1)
    cumulative_return = (1 + portfolio_return).cumprod() - 1
    return cumulative_return


def filter_returns_by_corr(corr, cutoff=0.9, exact=None):
    """This function is the Python implementation of the R function `findCorrelation()`.

    Relies on numpy and pandas, so must have them pre-installed.
    It searches through a correlation matrix and returns a list of column names
    to remove to reduce pairwise correlations.
    For the documentation of the R function, see
    https://www.rdocumentation.org/packages/caret/topics/findCorrelation
    and for the source code of `findCorrelation()`, see
    https://github.com/topepo/caret/blob/master/pkg/caret/R/findCorrelation.R
    -----------------------------------------------------------------------------

    Parameters:
    -----------
    corr: pandas dataframe.
        A correlation matrix as a pandas dataframe.
    cutoff: float, default: 0.9.
        A numeric value for the pairwise absolute correlation cutoff
    exact: bool, default: None
        A boolean value that determines whether the average correlations be
        recomputed at each step
    -----------------------------------------------------------------------------

    Returns:
    --------
    list of column names
    -----------------------------------------------------------------------------

    Example:
    --------
    R1 = pd.DataFrame({
        'x1': [1.0, 0.86, 0.56, 0.32, 0.85],
        'x2': [0.86, 1.0, 0.01, 0.74, 0.32],
        'x3': [0.56, 0.01, 1.0, 0.65, 0.91],
        'x4': [0.32, 0.74, 0.65, 1.0, 0.36],
        'x5': [0.85, 0.32, 0.91, 0.36, 1.0]
    }, index=['x1', 'x2', 'x3', 'x4', 'x5'])
    findCorrelation(R1, cutoff=0.6, exact=False)  # ['x4', 'x5', 'x1', 'x3']
    findCorrelation(R1, cutoff=0.6, exact=True)   # ['x1', 'x5', 'x4']
    """

    def _findCorrelation_fast(corr, avg, cutoff):

        combsAboveCutoff = corr.where(lambda x: (np.tril(x) == 0) & (x > cutoff)).stack().index

        rowsToCheck = combsAboveCutoff.get_level_values(0)
        colsToCheck = combsAboveCutoff.get_level_values(1)

        msk = avg[colsToCheck] > avg[rowsToCheck].values
        deletecol = pd.unique(np.r_[colsToCheck[msk], rowsToCheck[~msk]]).tolist()

        return deletecol

    def _findCorrelation_exact(corr, avg, cutoff):

        x = corr.loc[(*[avg.sort_values(ascending=False).index] * 2,)]

        if (x.dtypes.values[:, None] == ['int64', 'int32', 'int16', 'int8']).any():
            x = x.astype(float)

        x.values[(*[np.arange(len(x))] * 2,)] = np.nan

        deletecol = []
        for ix, i in enumerate(x.columns[:-1]):
            for j in x.columns[ix + 1 :]:
                if x.loc[i, j] > cutoff:
                    if x[i].mean() > np.nanmean(x.drop(j)):
                        deletecol.append(i)
                        x.loc[i] = x[i] = np.nan
                    else:
                        deletecol.append(j)
                        x.loc[j] = x[j] = np.nan
        return deletecol

    if not np.allclose(corr, corr.T) or any(corr.columns != corr.index):
        raise ValueError("correlation matrix is not symmetric.")

    acorr = corr.abs()
    avg = acorr.mean()

    if exact or exact is None and corr.shape[1] < 100:
        return _findCorrelation_exact(acorr, avg, cutoff)
    else:
        return _findCorrelation_fast(acorr, avg, cutoff)
