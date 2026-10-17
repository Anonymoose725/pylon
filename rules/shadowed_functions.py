from rules.base import Finding
import ast

KIND = {
    ast.FunctionDef: "function",
    ast.AsyncFunctionDef: "async function",
    ast.ClassDef: "class"
}
DEFS = tuple(KIND)

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

def _scan_statements(stmts: list[ast.stmt], result: list[Finding]) -> None:
    seen: dict[str, ast.AST] = {}
    for stmt in stmts:
        if isinstance(stmt, DEFS):
            first_seen = seen.get(stmt.name)
            if first_seen is not None and not _exempt(first_seen, stmt):
                result.append(Finding(
                    rule_id="shadowed-function",
                    message=(f"'{stmt.name}' redefined; the {KIND[type(first_seen)]} "
                             f"on line {first_seen.lineno} is shadowed"), # "myFunc redefined; the function on line 2 is shadowed"
                    line=stmt.lineno
                ))
            seen[stmt.name] = stmt

def _exempt(first, second) -> bool:
    # overload stubs, exempt if either first or second is marked as overloaded
    if _has_decorator(first, "overload") or _has_decorator(second, "overload"):
        return True
    # single dispatch: 'singledispatch' creates a generic function and '@x.register' registers special variants of it
    # property accessors (getters, setters) and @x.register on function named x
    if _is_attribute_of_self(second):
        return True
    # singledispatch convention matching repeated 'def _'s
    return second.name == "_"
    
def _has_decorator(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, name: str) -> bool:
    """Is true for @name, @mod.name, @name(...), @mod.name(...), false otherwise"""
    for deco in node.decorator_list:
        deco = deco.func if isinstance(deco, ast.Call) else deco # unwrap it if its a function call
        
        # ast.Name matching name
        if isinstance(deco, ast.Name) and deco.id == name:
            return True 
        # ast.Attribute matching name
        if isinstance(deco, ast.Attribute) and deco.attr == name:
            return True
        
    return False

def _is_attribute_of_self(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> bool:
    """Is true for @x.setter, @x.getter, @x.deleter, @x.register on 'def x' or any 'def foo'"""
    for deco in node.decorator_list:
        deco = deco.func if isinstance(deco, ast.Call) else deco # unwrap it if its a function call
        
        # if its an attribute, it has a Name label and the name matches the function def x / foo
        if isinstance(deco, ast.Attribute) and isinstance(deco.value, ast.Name) and deco.value.id == node.name:
            return True
        
    return False