from rules.base import Finding
import ast

def find_wildcard_imports(filepath: str) -> list[Finding]:
    """given a python file path, return a list (module, lineno) of wilcard imports"""
    with open(filepath) as f:
        src = f.read()
    tree = ast.parse(src)
    
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for name in node.names:
                if name.name == "*":
                    result.append(Finding(
                        rule_id="wildcard-import",
                        message=f"Wildcard import from '{node.module}'",
                        line=node.lineno
                    ))
                # deliberately not using aliased names as these will always be '*'
    
    return result