from typing import Callable, Dict
from inspect import signature

from .metadata import ToolMetadata, extract_tool_metadata

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolMetadata] = {}

    def register(self, func: Callable) -> Callable:
        meta = extract_tool_metadata(func)
        # Validate function has type hints for all parameters
        sig = signature(func)
        for name, param in sig.parameters.items():
            if param.annotation is param.empty:
                raise TypeError(f"Parameter '{name}' missing type annotation")
        self._tools[meta.name] = meta
        return func

    def get(self, name: str) -> ToolMetadata:
        return self._tools[name]

    def all_tools(self) -> Dict[str, ToolMetadata]:
        return dict(self._tools)
registry = ToolRegistry()

def tool(func: Callable) -> Callable:
    registry.register(func)
    return func

def register_tool(func: Callable) -> Callable:
    return registry.register(func)

def regenerate_grammar() -> str:
    from ..grammar.generator import combine_grammar
    metas = list(registry.all_tools().values())
    return combine_grammar(metas)
