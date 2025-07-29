import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from gcd.models.inference import generate
from gcd.models.concurrency import _model_lock

@pytest.mark.asyncio
async def test_run_with_lock():
    mock_model = AsyncMock(return_value='ok')
    with patch('gcd.models.inference.load_model', return_value=mock_model), \
         patch('gcd.models.inference.build_system_prompt', return_value='prompt'), \
         patch('gcd.models.inference.registry') as reg:
        reg.all_tools.return_value = {}
        result = await generate('hi')
        result = await generate("hi", timeout=0.1)
    assert _model_lock.locked() is False
