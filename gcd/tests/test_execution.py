from gcd.services.execution import execute
from gcd.tests.test_parsing import multiply


def test_execute_success():
    output = execute('multiply(2, 5)')
    assert 'result' in output


def test_execute_error():
    out = execute('unknown(1)')
    assert 'error' in out
