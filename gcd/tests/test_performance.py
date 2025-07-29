from gcd.models.performance import metrics, increment_requests


def test_metrics():
    before = metrics()['requests']
    increment_requests()
    after = metrics()['requests']
    assert after == before + 1
    assert 'memory' in metrics()
