"""This module provides methods for interacting with OneQuant strategies."""
from onequant.api.wrapper import _pagination, _pd, tddata_2_list


class OqStrategies:
    """A class for interacting with OneQuant strategies."""

    def __init__(self, wrapper=None):
        """Initializes an OqStrategies object.

        Args:
            wrapper (object, optional): An object containing the API and username. Defaults to None.
        """
        self.api = wrapper.api
        self.username = wrapper.username

    def _query(self, router, params=None):
        """Sends a GET request to the specified router with the given parameters.

        Args:
            router (str): The router to send the request to.
            params (dict, optional): The parameters to include in the request. Defaults to None.

        Returns:
            tuple: A tuple containing the data and code from the response.
        """
        result = self.api.request(method='get', router=router, params=params)
        if result['code'] != 200:
            raise Exception(f'An error occurred while retrieving tdegine data! code is {result["code"]}')
        return result['data']

    @_pd
    def _query_pd(self, params=None, router=None):
        """Sends a GET request and returns the data as a pandas DataFrame.

        Args:
            params (dict, optional): The parameters to include in the request. Defaults to None.
            router (str, optional): The router to send the request to. Defaults to None.

        Returns:
            pandas.DataFrame: The data from the response as a pandas DataFrame.
        """
        result = self.api.request(method='get', router=router, params=params)
        return result['data'], result['code']

    @_pd
    @_pagination
    def _query_pd_pg(self, params=None, router=None):
        """Sends a GET request and returns the data as a paginated pandas DataFrame.

        Args:
            params (dict, optional): The parameters to include in the request. Defaults to None.
            router (str, optional): The router to send the request to. Defaults to None.

        Returns:
            dict: A dictionary containing the paginated data and metadata from the response.
        """
        result = self.api.request(method='get', router=router, params=params)
        return result

    @_pd
    @tddata_2_list
    def _querytd_pd(self, router, params=None):
        """Sends a GET request and returns the data as a pandas DataFrame.

        Args:
            router (str): The router to send the request to.
            params (dict, optional): The parameters to include in the request. Defaults to None.

        Returns:
            pandas.DataFrame: The data from the response as a pandas DataFrame.
        """
        result = self.api.request(method='get', router=router, params=params)
        return result

    def strategy_base(self):
        """Returns the base information for all strategies.

        Returns:
            pandas.DataFrame: The base information for all strategies.
        """
        return self._query_pd(router='/strategy/info/base/query')

    def strategy_list(self, base_ea=None, base_tf=None, is_running=None, mark=None, min_tf=None):
        """Returns a paginated list of strategies that match the specified criteria.

        Args:
            base_ea (str, optional): The base EA to filter by. Defaults to None.
            base_tf (str, optional): The base time frame to filter by. Defaults to None.
            is_running (bool, optional): Whether the strategy is currently running. Defaults to None.
            mark (int, optional): The mark index to filter by. Defaults to None.

        Returns:
            dict: A dictionary containing the paginated list of strategies and metadata.
        """
        params = {
            'base_ea': base_ea,
            'base_tf': base_tf,
            'is_running': is_running,
            'mark_index': mark,
            'min_tf': min_tf,
        }
        return self._query_pd(router='/strategy/info/querypro', params=params)

    def strategy_report(
        self,
        strategy=None,
        base_ea=None,
        test_codes=None,
        base_tf=None,
        min_tf=None,
        min_netvalue=None,
        min_sharpe=None,
        min_annual_returns=None,
        min_calmar=None,
        min_sortino=None,
        max_margin=None,
        min_tradetimes=None,
        is_running=None,
    ):
        """Returns a paginated report of the specified strategy.

        Args:
            strategy (str, optional): The strategy to retrieve the report for. Defaults to None.
            base_ea (str, optional): The base EA to filter by. Defaults to None.
            test_codes (str, optional): The test codes to filter by. Defaults to None.
            base_tf (str, optional): The base time frame to filter by. Defaults to None.

        Returns:
            dict: A dictionary containing the paginated report and metadata.
        """
        params = {
            'strategy': strategy,
            'base_ea': base_ea,
            'base_tf': base_tf,
            'test_codes': test_codes,
            'min_tf': min_tf,
            'min_netvalue': min_netvalue,
            'min_sharpe': min_sharpe,
            'min_annual_returns': min_annual_returns,
            'min_calmar': min_calmar,
            'min_sortino': min_sortino,
            'max_margin': max_margin,
            'min_tradetimes': min_tradetimes,
            'status': -1 if is_running is None else (1 if is_running else 0),
        }
        return self._query_pd(router='/strategy/analyse/report/querypro', params=params)

    def strategy_netvalue(self, strategy_id=None):
        """Returns the net value for the specified strategy.

        Args:
            strategy_id (str, optional): The ID of the strategy to retrieve the net value for. Defaults to None.

        Returns:
            pandas.DataFrame: The net value for the specified strategy.
        """
        params = {'strategy_id': strategy_id}
        return self._querytd_pd(router='/strategy/analyse/netequity/query', params=params)

    def strategy_record(self, strategy_id=None):
        """Returns the record for the specified strategy.

        Args:
            strategy_id (str, optional): The ID of the strategy to retrieve the record for. Defaults to None.

        Returns:
            pandas.DataFrame: The record for the specified strategy.
        """
        params = {'strategy_id': strategy_id}
        return self._querytd_pd(router='/strateg/analyse/record/query', params=params)
