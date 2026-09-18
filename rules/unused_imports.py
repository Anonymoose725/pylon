from rules.base import Finding
import ast

def find_unused_imports(filepath: str) -> list[Finding]:
    """Given a Python file path, return a list of import names that are never used"""
    # get tree
    with open(filepath) as f:
        source = f.read() # string
    tree = ast.parse(source)
    
    # get list of imports
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for name in node.names:
                # check if .name or .asname (import os || import os as opersys)
                imported[name.asname or name.name] = node.lineno
    
    # every time code references a name: os.path.join(), path.exists(),... parser creates ast.Name with .id attribute
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
    
    # compare
    result = []
    for name,lineno in imported.items():
        if name not in used_names:
            # unused import: create a Finding
            result.append(Finding(
                rule_id="unused-import",
                message=f"Unused import from '{name}'",
                line=lineno
            ))
    
    return result