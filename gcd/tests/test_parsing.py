from pydantic import BaseModel

from gcd.services.parser import parse_output
from gcd.services.validation import validate_call
from gcd.tools.registry import tool

@tool
def multiply(x: int, y: int) -> int:
    """Multiply"""
    return x * y

class Item(BaseModel):
    name: str

@tool
def echo(item: Item) -> str:
    """Echo"""
    return item.name


def test_parse_output():
    call = parse_output('multiply(2, 3)')
    assert call.name == 'multiply'
    assert call.args == [2, 3]


def test_validate_call_simple():
    call = parse_output('multiply(2, 4)')
    result = validate_call(call)
    assert result == 8


def test_validate_call_pydantic():
    call = parse_output("echo({'name': 'hi'})")
    result = validate_call(call)
    assert result == 'hi'
