from gcd.tools.metadata import extract_tool_metadata
from gcd.tools.registry import registry, tool

@tool
def sample(a: int, b: str = "x") -> str:
    """Example tool.

    Grammar:
        <call> ::= "sample(" <int> ", " <string> ")"
    """
    return b * a


def test_extract_tool_metadata():
    meta = extract_tool_metadata(sample)
    assert meta.name == "sample"
    assert "Example tool" in meta.description
    assert "a" in meta.signature
    assert meta.custom_grammar is not None


def test_registry():
    reg_meta = registry.get("sample")
    assert reg_meta.name == "sample"
