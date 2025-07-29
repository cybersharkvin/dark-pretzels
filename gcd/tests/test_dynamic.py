from gcd.tools.registry import register_tool, regenerate_grammar


def sample_tool(x: int) -> int:
    """A sample"""
    return x


def test_dynamic_registration():
    register_tool(sample_tool)
    grammar = regenerate_grammar()
    assert '<sample_tool>' in grammar
