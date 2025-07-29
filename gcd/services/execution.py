from .errors import ErrorResponse
import json
import time
from typing import Any

from ..logging_config import logger
from .validation import validate_call
from .parser import parse_output


def execute(text: str) -> str:
    start = time.time()
    try:
        call = parse_output(text)
    except Exception as e:
        logger.error("parse fail", exc_info=e)
        return json.dumps(ErrorResponse(error="parse_error").dict())
    try:
        result = validate_call(call)
        duration = time.time() - start
        response = {"result": result, "time": duration}
    except Exception as e:
        logger.error("execution error", exc_info=e)
        response = ErrorResponse(error=str(e)).dict()
    return json.dumps(response)
