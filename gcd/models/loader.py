from pathlib import Path
from typing import Optional

try:
    from llama_cpp import Llama, LlamaGrammar
except ImportError:  # pragma: no cover - allow running without package
    Llama = None
    LlamaGrammar = None

from ..logging_config import logger
from ..grammar.generator import combine_grammar
from ..tools.registry import registry
from ..config import settings

_model = None
_grammar = None

def load_grammar() -> Optional[str]:
    global _grammar
    if _grammar is None:
        metas = list(registry.all_tools().values())
        _grammar = combine_grammar(metas)
    return _grammar


def load_model(model_path: Optional[Path] = None):
    global _model
    if _model is not None:
        return _model
    model_path = model_path or settings.model_path
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    if Llama is None:
        logger.warning("llama_cpp not installed; using mock")
        _model = None
    else:
        grammar_text = load_grammar()
        llm_kwargs = {"model_path": str(model_path), "n_ctx": settings.n_ctx, "n_threads": settings.n_threads}
        if grammar_text:
            grammar = LlamaGrammar.from_string(grammar_text)
            llm_kwargs["grammar"] = grammar
        _model = Llama(**llm_kwargs)
    return _model
