"""This module provides methods for interacting with OneQuant quotedatas."""
from onequant.api.wrapper import _pagination, _pd, tddata_2_list
from onequant.util.datetime import OqDateTime


class OqQuotes:
    """A class for interacting with OneQuant quotedatas."""

    def __init__(self, wrapper=None):
        """Initializes an OqQuotes object.

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

    def realtime_quote(self):
        """Returns realtime quote data.

        Returns:
            pandas.DataFrame: The realtime quote data.
        """
        return self._query_pd(router='/quote/future/realTime/quote')

    def realtime_quotes(self):
        """Returns multiple realtime quote data.

        Returns:
            pandas.DataFrame: The multiple realtime quote data.
        """
        return self._query_pd(router='/quote/future/realTime/quotes')

    def future_bars(self, code=None, interval=None, start_time=None, end_time=None, limit=None):
        """Fetches K-line (candlestick) data for futures.

        Args:
            code (str, optional): The code of the future to fetch data for. Defaults to None.
            interval (str, optional): The time interval for each K-line data point. Defaults to None.
            start (uint or str, optional): The start time for the data fetch. Can be a timestamp or a date string.
            end (uint or str, optional): The end time for the data fetch. Can be a timestamp or a date string.
            limit (int, optional): The maximum number of data points to fetch. Defaults to None.If set limit value,then
            start will discarded.

        Returns:
            pandas.DataFrame: The K-line data as a pandas DataFrame.
        """
        if isinstance(start_time, int) and isinstance(end_time, int):
            params = {
                'symbol': code,
                'interval': interval,
                'start': start_time,
                'end': end_time,
                'limit': limit,
            }
            return self._querytd_pd(router='/tvquote/kline_ascend', params=params)
        else:
            params = {
                'symbol': code,
                'interval': interval,
                'start': OqDateTime.string_to_ms_timestamp(start_time),
                'end': OqDateTime.string_to_ms_timestamp(end_time),
                'limit': limit,
            }
            return self._querytd_pd(router='/tvquote/kline_ascend', params=params)

    def symbols(self):
        """Returns symbols data."""
        return self._query_pd_pg(router='/quote/futureBase/symbol', params={})

    def codeinfos(self):
        """Returns code information data."""
        return self._query_pd_pg(router='/quote/futureBase/allCode', params={})

    def indexes(self):
        """Returns indexes data."""
        return self._query_pd_pg(router='/quote/futureBase/indexCode', params={})

    def option_codes(self):
        """Returns option codes data."""
        return self._query_pd_pg(router='/quote/futureBase/optionCode', params={})

    def std_codes(self):
        """Returns standard codes data."""
        return self._query_pd_pg(router='/quote/futureBase/stdCode', params={})


if __name__ == '__main__':
    from dynaconf import Dynaconf

    from onequant.api.request import ApiWrapper

    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['./settings.toml', './.secrets.toml'],
    )

    wrapper = ApiWrapper(settings.api_url, settings.username, settings.password)

    quotes = OqQuotes(wrapper)

    # data = quotes.future_bars(code='rb000', start_time='20240101', end_time='20240201', interval='15m', limit=1000)
    # data
    data = quotes.std_codes()
    data
