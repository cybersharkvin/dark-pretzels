import ast
from typing import Any, List

from pydantic import BaseModel, ValidationError

from ..tools.registry import registry

class ParsedCall(BaseModel):
    name: str
    args: List[Any]


def parse_output(text: str) -> ParsedCall:
    try:
        node = ast.parse(text.strip(), mode="eval")
    except SyntaxError as e:
        raise ValueError("invalid syntax") from e
    if not isinstance(node.body, ast.Call):
        raise ValueError("expected single function call")
    func_name = getattr(node.body.func, 'id', None)
    if func_name is None:
        raise ValueError("invalid function name")
    args = [ast.literal_eval(arg) for arg in node.body.args]
    return ParsedCall(name=func_name, args=args)
