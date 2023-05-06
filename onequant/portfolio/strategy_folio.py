"""Fetch reports and returns for strategies."""
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from onequant.api.request import ApiWrapper
from onequant.api.strategies import OqStrategies
from onequant.data_wash.preprocess_returns import fill_date, filter_returns_by_corr


def get_filter_reports(
    wrapper=None,
    strategy=None,
    base_ea=None,
    test_codes=None,
    base_tf=None,
    min_tf=None,
    min_netvalue=None,
    min_sharpe=None,
    min_profit_year_ratio=None,
    min_calmar=None,
    min_sortino=None,
    max_margin=None,
    min_tradetimes=None,
):
    """This function retrieves the reports and OqStrategies object for a given set of parameters.

    Parameters:
    -----------
    wrapper: ApiWrapper object, default: None.
        An object of the ApiWrapper class.
    strategy: str, default: None.
        The strategy ID.
    base_ea: str, default: None.
        The base EA.
    test_codes: list, default: None.
        A list of test codes.
    base_tf: int, default: None.
        The base time frame.
    min_tf: int, default: None.
        The minimum time frame.
    min_netvalue: float, default: None.
        The minimum net value.
    min_sharpe: float, default: None.
        The minimum Sharpe ratio.
    min_profit_year_ratio: float, default: None.
        The minimum profit year ratio.
    min_calmar: float, default: None.
        The minimum Calmar ratio.
    min_sortino: float, default: None.
        The minimum Sortino ratio.
    max_margin: float, default: None.
        The maximum margin.
    min_tradetimes: int, default: None.
        The minimum number of trades.

    Returns:
    --------
    reports: pandas dataframe.
        A dataframe containing the reports.
    oqs: OqStrategies object.
        An object of the OqStrategies class.
    """
    oqs = OqStrategies(wrapper=wrapper)
    reports, _ = oqs.strategy_report(
        strategy,
        base_ea,
        test_codes,
        base_tf,
        min_tf,
        min_netvalue,
        min_sharpe,
        min_profit_year_ratio,
        min_calmar,
        min_sortino,
        max_margin,
        min_tradetimes,
    )
    return reports, oqs


def get_strategy_returns(oqs, strategy_list):
    """This function retrieves the returns for a given strategy ID.

    Parameters:
    -----------
    oqs: OqStrategies object.
        An object of the OqStrategies class.
    strategy_list: list.
        A list of strategy IDs.

    Returns:
    --------
    returns_df: pandas dataframe.
        A dataframe containing the returns.
    """

    def get_returns(id):
        try:
            data, _ = oqs.strategy_netvalue(id)
            data['ts'] = pd.to_datetime(data['ts'])
            data.set_index('ts', inplace=True)

            # Set hours and minutes to zero
            data.index = data.index.tz_localize(None).floor('D')

            data = data[~data.index.duplicated()]
            data = data.resample('D').ffill()

            data = fill_date(
                strategy_id=id,
                data=data,
                need_start=pd.Timestamp('2015-01-01', tz='UTC'),
                need_end=pd.Timestamp('2023-04-15', tz='UTC'),
            )

            data = data.rename(columns={'net_value': id})
            data[id] = data[id].pct_change()
            data = data.dropna()

            return data
        except Exception as e:
            print(f'{id} get returns error {e}')
            return None

    dfs = []
    pool = ThreadPoolExecutor()
    for res in pool.map(get_returns, strategy_list):
        if res is not None:
            dfs.append(res)
    returns_df = pd.concat(dfs, axis=1)
    return returns_df


def get_strategy_filter_corr(returns=None, max_corr=0.9):
    """This function filters the returns dataframe by correlation.

    Parameters:
    -----------
    returns: pandas dataframe, default: None.
        A dataframe containing the returns.
    max_corr: float, default: 0.9.
        The maximum correlation value.

    Returns:
    --------
    trimmed_df: pandas dataframe.
        A dataframe containing the filtered returns.
    """
    corr_matrix = returns.corr()
    returns_by_corr = filter_returns_by_corr(corr_matrix, cutoff=max_corr)
    trimmed_df = returns.drop(columns=returns_by_corr)
    trimmed_df = trimmed_df.fillna(0)
    return trimmed_df


if __name__ == '__main__':
    from dynaconf import Dynaconf

    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['../settings.toml', '../.secrets.toml'],
    )
    wrapper = ApiWrapper(settings.api_url, settings.username, settings.password)

    reports, oqs = get_filter_reports(
        wrapper=wrapper, min_tf=240, min_profit_year_ratio=0.2, min_sharpe=0.4, max_margin=60000, min_tradetimes=100
    )
    returns = get_strategy_returns(oqs, reports['strategy'])

    get_strategy_filter_corr(returns=returns, max_corr=0.85)
