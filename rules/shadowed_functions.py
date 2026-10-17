from rules.base import Finding
import ast

def find_shadowed_functions(filepath: str) -> list[Finding]:
    """Given a python file path, return a list of Findings where functions have been redefined, silently shadowing. This includes `def`, `async def`, and `class`"""
    with open(filepath) as f:
        src = f.read()
    tree = ast.parse(src)
    
    # return
    # 'test_create' redefined; the definition on line 12 is unreachable
    result = []
    seen = {} # dict[str, ast.AST]
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in seen: # must be exact matching
                typeOfNode = {
                    ast.FunctionDef: "function",
                    ast.AsyncFunctionDef: "async function",
                    ast.ClassDef: "class"
                }.get(type(node)) # a dict, cool!
                
                result.append(Finding(
                    rule_id="shadowed-function",
                    message=f"'{node.name}' redefined; {typeOfNode} definition is shadowed",
                    line=node.lineno # note this is where the shadowing occurs, not original def
                ))
            seen[node.name] = node
    return result
    
