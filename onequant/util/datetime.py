"""Module for datetime utility functions."""

import datetime


class OqDateTime:
    """This class provides methods to convert timestamps to strings and vice versa."""

    @staticmethod
    def timestamp_to_string(timestamp):
        """Converts a timestamp to a string in the format 'YYYY-MM-DD HH:MM:SS'.

        Args:
            timestamp (int): The timestamp to convert.

        Returns:
            str: The formatted date and time string.
        """
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def string_to_timestamp(date_string):
        """Converts a date and time string in the format 'YYYY-MM-DD HH:MM:SS' to a timestamp.

        Args:
            date_string (str): The date and time string to convert.

        Returns:
            int: The timestamp.
        """
        if len(date_string) == 10:
            date_string += ' 00:00:00'
        elif len(date_string) == 8:
            date_string = date_string[:4] + '-' + date_string[4:6] + '-' + date_string[6:] + ' 00:00:00'
        return int(datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').timestamp())

    @staticmethod
    def string_to_ms_timestamp(date_string):
        """Converts a date and time string in the format 'YYYY-MM-DD HH:MM:SS' to a timestamp in milliseconds.

        Args:
            date_string (str): The date and time string to convert.

        Returns:
            int: The timestamp in milliseconds.
        """
        if len(date_string) == 10:
            date_string += ' 00:00:00'
        elif len(date_string) == 8:
            date_string = date_string[:4] + '-' + date_string[4:6] + '-' + date_string[6:] + ' 00:00:00'
        return int(datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
