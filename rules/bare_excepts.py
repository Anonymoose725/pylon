from rules.base import Finding
import ast

def find_bare_excepts(filepath: str) -> list[Finding]:
    """given a python file path, return a list of Findings where try-catch uses a bare except"""
    with open(filepath) as f:
        src = f.read()
    tree = ast.parse(src)
    
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            result.append(Finding(
                rule_id="bare-except",
                message="Bare except clause found in try block",
                line=node.lineno
            ))
    
    # notice: i dont want through and find tries and then match tries with exception handlers
    # the tree walk finds ALL nodes, recursively, so it will find exception handlers anyway.
    return result