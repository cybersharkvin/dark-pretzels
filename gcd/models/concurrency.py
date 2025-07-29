import asyncio

_model_lock = asyncio.Lock()

async def run_with_lock(coro, timeout: float | None = None):
    async with _model_lock:
        if timeout:
            return await asyncio.wait_for(coro, timeout)
        return await coro
