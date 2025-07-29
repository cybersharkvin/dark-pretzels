BASE_TYPES = {
    "string": r'<string> ::= "(?:\\\\.|[^\\\\"])*"',
    "int": r"<int> ::= -?[0-9]+",
    "float": r"<float> ::= -?[0-9]+(?:\\.[0-9]+)?",
    "bool": r"<bool> ::= \"True\" | \"False\"",
}

def base_grammar() -> str:
    return "\n".join(BASE_TYPES.values())
