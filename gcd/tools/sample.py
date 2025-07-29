from .registry import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
