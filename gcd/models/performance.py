import psutil

_request_count = 0

def increment_requests() -> None:
    global _request_count
    _request_count += 1

def metrics() -> dict:
    return {
        "requests": _request_count,
        "memory": psutil.Process().memory_info().rss,
    }
