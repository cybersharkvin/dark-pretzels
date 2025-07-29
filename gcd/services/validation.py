from inspect import signature
from typing import Any, get_type_hints

from pydantic import BaseModel

from ..tools.registry import registry
from .parser import ParsedCall


def validate_call(call: ParsedCall) -> Any:
    if call.name not in registry.all_tools():
        raise ValueError("unknown tool")
    tool_meta = registry.get(call.name)
    func = tool_meta.function
    sig = signature(func)
    hints = get_type_hints(func)
    if len(call.args) != len(sig.parameters):
        raise ValueError("argument count mismatch")
    validated_args = []
    for arg, (name, param) in zip(call.args, sig.parameters.items()):
        expected = hints.get(name, str)
        try:
            if isinstance(expected, type) and issubclass(expected, BaseModel):
                validated_args.append(expected.parse_obj(arg))
            else:
                validated_args.append(expected(arg))
        except Exception as e:
            raise ValueError(f"type error for {name}") from e
    return func(*validated_args)
