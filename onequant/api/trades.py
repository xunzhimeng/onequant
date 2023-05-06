"""Get trades information from server."""
from onequant.api.wrapper import _pd


class OqTrades:
    """Api for get trades information from server."""

    def __init__(self, wrapper=None):
        """Initializes the OqTrades class.

        Args:
            wrapper: An object that wraps the OneQuant API.

        Returns:
            None.
        """
        self.api = wrapper.api
        self.username = wrapper.username

    def _query(self, router=None, params=None):
        """Sends a GET request to the OneQuant API.

        Args:
            router: The router for the request.
            params: The parameters for the request.

        Returns:
            A tuple containing the data and code from the request.
        """
        result = self.api.request(method='get', router=router, params=params)
        return result['data'], result['code']

    @_pd
    def _query_pd(self, router=None, params=None):
        """Sends a GET request to the OneQuant API and returns the data as a pandas DataFrame.

        Args:
            router: The router for the request.
            params: The parameters for the request.

        Returns:
            A pandas DataFrame containing the data from the request.
        """
        result = self.api.request(method='get', router=router, params=params)
        return result['data'], result['code']

    def account(self):
        """Sends a GET request to the OneQuant API to retrieve account information.

        Args:
            None.

        Returns:
            A tuple containing the data and code from the request.
        """
        params = {'acc_type': 0}
        return self._query('/trade/account/query', params)

    def account_virtual(self):
        """Sends a GET request to the OneQuant API to retrieve virtual account information.

        Args:
            None.

        Returns:
            A tuple containing the data and code from the request.
        """
        params = {'acc_type': 1}
        return self._query('/trade/account/query', params)

    def position(self):
        """Sends a GET request to the OneQuant API to retrieve position information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the position data from the request.
        """
        params = {'acc_type': 0}
        return self._query_pd('/trade/position/query', params)

    def position_virtual(self):
        """Sends a GET request to the OneQuant API to retrieve virtual position information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the virtual position data from the request.
        """
        params = {'acc_type': 1}
        return self._query_pd('/trade/position/query', params)

    def orders(self):
        """Sends a GET request to the OneQuant API to retrieve order information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the order data from the request.
        """
        params = {'is_virtual': 0}
        return self._query_pd('/trade/order/query', params)

    def orders_virtual(self):
        """Sends a GET request to the OneQuant API to retrieve virtual order information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the virtual order data from the request.
        """
        params = {'is_virtual': 1}
        return self._query_pd('/trade/order/query', params)

    def unfill_orders(self):
        """Sends a GET request to the OneQuant API to retrieve unfulfilled order information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the unfulfilled order data from the request.
        """
        params = {'is_virtual': 0}
        return self._query_pd('/trade/order/restore/query', params)

    def unfill_orders_virtual(self):
        """Sends a GET request to the OneQuant API to retrieve virtual unfulfilled order information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the virtual unfulfilled order data from the request.
        """
        params = {'is_virtual': 1}
        return self._query_pd('/trade/order/restore/query', params)

    def rsptrades(self):
        """Sends a GET request to the OneQuant API to retrieve real-time settlement trade information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the real-time settlement trade data from the request.
        """
        params = {'is_virtual': 0}
        return self._query_pd('/trade/rsptrade/query', params)

    def rsptrades_virtual(self):
        """Sends a GET request to the OneQuant API to retrieve virtual real-time settlement trade information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the virtual real-time settlement trade data from the request.
        """
        params = {'is_virtual': 1}
        return self._query_pd('/trade/rsptrade/query', params)

    def workers(self):
        """Sends a GET request to the OneQuant API to retrieve worker information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the worker data from the request.
        """
        return self._query_pd('/trade/worker/query')

    def conditions(self):
        """Sends a GET request to the OneQuant API to retrieve condition information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the condition data from the request.
        """
        return self._query_pd('/trade/condition/query')

    def acc_follow(self):
        """Sends a GET request to the OneQuant API to retrieve account follow information.

        Args:
            None.

        Returns:
            A pandas DataFrame containing the account follow data from the request.
        """
        params = {'user': self.username}
        return self._query_pd('/trade/accFollow/query', params)
