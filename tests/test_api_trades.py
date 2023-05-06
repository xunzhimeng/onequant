"""Module to test the OqTrades object."""

import pytest


@pytest.fixture(scope='module')
def test_init():
    """Initializes OqTrades object with valid credentials."""
    from config import settings
    from onequant.api.request import ApiWrapper
    from onequant.api.trades import OqTrades

    return OqTrades(ApiWrapper(settings.api_url, settings.username, settings.password))


@pytest.fixture(scope='module')
def test_failed_init():
    """Initializes OqTrades object with invalid credentials."""
    from config import settings
    from onequant.api.request import ApiWrapper
    from onequant.api.trades import OqTrades

    return OqTrades(ApiWrapper(settings.api_url, 'test', '123456'))


def test_query_func(test_init):
    """Tests the query function of OqTrades object."""
    params = {'acc_type': 0}
    results = test_init.api.request(method='get', router='/trade/account/query', params=params)
    assert results['code'] == 200, 'Account return code not euqal 200!'
    assert results['data'] and len(results['data']) > 0, 'Account return data empty!'
    assert isinstance(results['data'], dict), 'Account return is not a JSON object!'
    assert results['data']['acc_type'] == 0, 'Account return type is virtual!'
    assert results['data']['user'] == test_init.username, 'Account return user not equal to request data!'


def test_real_accounts(test_init):
    """Tests the account function of OqTrades object with real accounts."""
    data, code = test_init.account()
    assert code == 200, 'Account response http error!'
    assert data and len(data) > 0, 'Account return data empty!'
    assert isinstance(data, dict), 'Account return is not a JSON object!'
    assert data['acc_type'] == 0, 'Account return type is virtual!'
    assert data['user'] == test_init.username, 'Account return user not equal to request data!'


def test_virtual_accounts(test_init):
    """Tests the account function of OqTrades object with virtual accounts."""
    data, code = test_init.account_virtual()
    assert code == 200, 'Virtual Account response http error!'
    assert data and len(data) > 0, 'Virtual Account return data empty!'
    assert isinstance(data, dict), 'Virtual Account return is not a JSON object!'
    assert data['acc_type'] == 1, 'Virtual Account return type is real!'
    assert data['user'] == test_init.username, 'Virtual Account return user not equal to request data!'


def test_err_real_accounts(test_failed_init):
    """Tests the account function of OqTrades object with invalid credentials for real accounts."""
    data, code = test_failed_init.account()
    assert code == 401, 'Account incorrect login got success code!'
    assert data is None, 'ErrAccount return data not empty!'


def test_err_virtual_accounts(test_failed_init):
    """Tests the account function of OqTrades object with invalid credentials for virtual accounts."""
    data, code = test_failed_init.account_virtual()
    assert code == 401, 'Virtual Account login got success code!'
    assert data is None, 'ErrAccount return data not empty!'


if __name__ == '__main__':
    pytest.main()
