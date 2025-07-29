from typing import Optional

from ..tools.registry import registry
from .loader import load_model
from .prompt import build_system_prompt
from .concurrency import run_with_lock
from .performance import increment_requests

async def generate(question: str, max_tokens: int = 64, timeout: Optional[float] = None) -> str:
    model = load_model()
    increment_requests()
    if model is None:
        return ""
    metas = list(registry.all_tools().values())
    system_prompt = build_system_prompt(metas)
    prompt = system_prompt + "\n" + question

    async def _call():
        return await model(prompt, max_tokens=max_tokens, temperature=0.0)

    return await run_with_lock(_call(), timeout=timeout)
