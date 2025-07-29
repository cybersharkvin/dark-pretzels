from gcd.tools.registry import registry, tool
from gcd.grammar.generator import combine_grammar

@tool
def add(x: int, y: int) -> int:
    """Add numbers"""
    return x + y


def test_combine_grammar():
    metas = list(registry.all_tools().values())
    grammar = combine_grammar(metas)
    assert '<root>' in grammar
    assert '<add>' in grammar
    assert '<int>' in grammar
