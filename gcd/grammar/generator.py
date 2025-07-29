from inspect import signature, Parameter
from typing import List

from ..tools.metadata import ToolMetadata
from .base import base_grammar, BASE_TYPES

TYPE_MAP = {
    str: "<string>",
    int: "<int>",
    float: "<float>",
    bool: "<bool>",
}


def rule_from_signature(meta: ToolMetadata) -> str:
    sig = signature(meta.function)
    parts: List[str] = []
    for i, param in enumerate(sig.parameters.values()):
        type_rule = TYPE_MAP.get(param.annotation, "<string>")
        if param.default is not Parameter.empty:
            part = f"[ {type_rule} ]"
        else:
            part = type_rule
        if i > 0:
            parts.append('", "')
        parts.append(part)
    args = " ".join(parts)
    return f"<{meta.name}> ::= \"{meta.name}(\" {args} \")\""


def generate_tool_rules(metas: List[ToolMetadata]) -> List[str]:
    rules = []
    for meta in metas:
        if meta.custom_grammar:
            rules.append(meta.custom_grammar)
        else:
            rules.append(rule_from_signature(meta))
    return rules


def combine_grammar(metas: List[ToolMetadata]) -> str:
    rules = generate_tool_rules(metas)
    root_alts = [f"<{m.name}>" for m in metas]
    rules.append(f"<root> ::= {' | '.join(root_alts)}")
    rules.append(base_grammar())
    return "\n".join(rules)
