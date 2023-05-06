"""Decorator to convert the data returned by the API to a list."""


def tddata_2_list(func):
    """Decorator to convert the data returned by the API to a list.

    Args:
        func: The function to be decorated

    Returns:
        A wrapper function that converts the data to a list
    """

    def wrapper(self, *args, **kwargs):
        data = func(self, *args, **kwargs)
        if data is None or data['data'] is None:
            return None, 400
        if data['data']['code'] != 0:
            return None, data['code']
        column_meta = data['data']['column_meta']
        data_list = data['data']['data']
        result = list(map(lambda row: {column_meta[i][0]: row[i] for i in range(len(column_meta))}, data_list))
        return result, data['code']

    return wrapper


# Decorator to convert the data returned by the API to a pandas DataFrame
def _pd(func):
    """Decorator to convert the data returned by the API to a pandas DataFrame.

    Args:
        func: The function to be decorated

    Returns:
        A wrapper function that converts the data to a pandas DataFrame
    """

    def convert(self, *args, **kwargs):
        import pandas as pd

        data, code = func(self, *args, **kwargs)
        return pd.DataFrame(data), code

    return convert


def _pagination(func):
    """Decorator to handle pagination of API data.

    Args:
        func: The function to be decorated

    Returns:
        A wrapper function that handles pagination of API data
    """

    def wrapper(self, *args, **kwargs):
        kwargs['params']['current'] = 1
        kwargs['params']['pageSize'] = 10000
        data = func(self, *args, **kwargs)

        if 'total' in data and 'pageSize' in data:
            total = data['total']
            page_size = data['pageSize']

            num_pages = (total + page_size - 1) // page_size

            for page in range(2, num_pages + 1):
                if 'params' in kwargs:
                    kwargs['params']['current'] = page
                    kwargs['params']['pageSize'] = page_size
                page_data = func(self, *args, **kwargs)
                if page_data['code'] != 200:
                    print(f'Error: {page}')
                    continue
                data['data'].extend(page_data['data'])

        return data['data'], data['code']

    return wrapper
