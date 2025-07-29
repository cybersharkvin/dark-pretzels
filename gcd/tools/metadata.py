from dataclasses import dataclass
from inspect import signature
from typing import Callable, Dict, Optional

from docstring_parser import parse

@dataclass
class ToolMetadata:
    name: str
    description: str
    function: Callable
    signature: str
    custom_grammar: Optional[str]

def extract_tool_metadata(func: Callable) -> ToolMetadata:
    sig = signature(func)
    doc = func.__doc__ or ""
    parsed = parse(doc)
    description = parsed.short_description or ""
    custom_grammar = None
    if parsed.long_description:
        lines = [line.rstrip() for line in parsed.long_description.splitlines()]
        grammar_lines = []
        in_grammar = False
        for line in lines:
            if line.strip().lower().startswith("grammar:"):
                in_grammar = True
                continue
            if in_grammar:
                grammar_lines.append(line)
        if grammar_lines:
            custom_grammar = "\n".join(grammar_lines).strip() or None
    return ToolMetadata(
        name=func.__name__,
        description=description,
        function=func,
        signature=str(sig),
        custom_grammar=custom_grammar,
    )
