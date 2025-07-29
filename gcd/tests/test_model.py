from pathlib import Path
from unittest.mock import patch

from gcd.models.loader import load_model, load_grammar
from gcd.tools.registry import tool

@tool
def dummy(a: int) -> int:
    """Dummy tool"""
    return a


def test_load_grammar():
    gram = load_grammar()
    assert '<root>' in gram


def test_load_model(tmp_path):
    model_file = tmp_path / "model.bin"
    model_file.write_text("dummy")
    with patch('gcd.models.loader.Llama') as MockLlama, patch('gcd.models.loader.LlamaGrammar') as MockGrammar:
        load_model(model_file)
        assert MockLlama.called
