from rules.base import Finding
import ast

KIND = {
    ast.FunctionDef: "function",
    ast.AsyncFunctionDef: "async function",
    ast.ClassDef: "class"
}
DEFS = tuple(KIND)

def _scan_statements(stmts: list[ast.stmt], result: list[Finding]) -> None:
    seen: dict[str, ast.AST] = {}
    for stmt in stmts:
        if isinstance(stmt, DEFS):
            first_seen = seen.get(stmt.name)
            if first_seen is not None:
                result.append(Finding(
                    rule_id="shadowed-function",
                    message=(f"'{stmt.name}' redefined; the {KIND[type(first_seen)]} "
                             f"on line {first_seen.lineno} is shadowed"), # "myFunc redefined; the function on line 2 is shadowed"
                    line=stmt.lineno
                ))
            seen[stmt.name] = stmt

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
        # per-scope
        for field in ("body", "orelse", "finalbody"):
            stmts = getattr(node, field, None) # get field if it has one, equiv to node.field
            if isinstance(stmts, list):
                # lambda / if exp have a non-list 'body' field
                _scan_statements(stmts, result)
                
    result.sort(key=lambda f: f.line) # sort by line since it wont match walk order
    return result
    
