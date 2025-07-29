from gcd.services.execution import execute
from gcd.services.errors import ErrorResponse


def test_parse_fail():
    out = execute("not a call")
    data = ErrorResponse.parse_raw(out)
    assert data.error == "parse_error"


def test_error_response():
    out = execute('bad(')
    data = ErrorResponse.parse_raw(out)
    assert data.error
