"""Pytest setup"""


def pytest_configure(config):
    # NB this causes `onequant/__init__.py` to run
    import onequant  # noqa
