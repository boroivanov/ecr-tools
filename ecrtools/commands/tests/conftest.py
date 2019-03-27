import pytest
from click.testing import CliRunner


@pytest.yield_fixture(scope='session')
def runner():
    '''
    Setup a Python Click cli runner, this gets executed for each test function.
    '''
    yield CliRunner()
