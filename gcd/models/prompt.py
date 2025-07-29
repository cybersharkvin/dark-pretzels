from typing import List
from ..tools.metadata import ToolMetadata

SYSTEM_TEMPLATE = "Available tools:\n{tools}\nRespond with a tool call."


def tool_description(meta: ToolMetadata) -> str:
    params = meta.signature
    return f"- {meta.name}{params}: {meta.description}"


def build_system_prompt(metas: List[ToolMetadata]) -> str:
    desc = "\n".join(tool_description(m) for m in metas)
    return SYSTEM_TEMPLATE.format(tools=desc)
