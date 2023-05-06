"""Module to test the OqStrategies object."""
import pytest


# Fixture for testing initialization of OqStrategies object
@pytest.fixture(scope='module')
def test_init():
    """Test initialization of OqStrategies object."""
    from config import settings
    from onequant.api.request import ApiWrapper
    from onequant.api.strategies import OqStrategies

    return OqStrategies(ApiWrapper(settings.api_url, settings.username, settings.password))


# Fixture for testing initialization of OqStrategies object with incorrect credentials
@pytest.fixture(scope='module')
def test_failed_init():
    """Test initialization of OqStrategies object with incorrect credentials."""
    from config import settings
    from onequant.api.request import ApiWrapper
    from onequant.api.strategies import OqStrategies

    return OqStrategies(ApiWrapper(settings.api_url, 'test', '123456'))


# Test strategy_list method of OqStrategies object
def test_strategy_list(test_init):
    """Test strategy_list method of OqStrategies object."""
    data, code = test_init.strategy_list()
    assert code == 200, 'Response of http error!'
    assert len(data) > 0, 'Strategy list return data empty!'


# Test strategy_netvalue method of OqStrategies object
def test_strategy_netequity(test_init):
    """Test strategy_netvalue method of OqStrategies object."""
    data, code = test_init.strategy_netvalue(strategy_id='MA_gold_ema_M9_back_6_8')
    assert code == 200, 'Response of http error!'
    assert len(data) > 0, 'Strategy return data empty!'


# Test strategy_netvalue method of OqStrategies object with incorrect strategy_id
def test_err_strategy_netequity(test_init):
    """Test strategy_netvalue method of OqStrategies object with incorrect strategy_id."""
    data, code = test_init.strategy_netvalue(strategy_id='test')
    assert code == 200, 'Response of http unexpected correct!'
    assert len(data) == 0, 'Strategy return data not empty!'


# Test strategy_base method of OqStrategies object with incorrect credentials
def test_err_strategy_base(test_failed_init):
    """Test strategy_base method of OqStrategies object with incorrect credentials."""
    data, code = test_failed_init.strategy_base()
    assert code != 200, 'Response of http unexpected correct!'
    assert len(data) == 0, 'ErrAccount return data not empty!'


if __name__ == '__main__':
    pytest.main()
