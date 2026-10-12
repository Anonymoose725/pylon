from rules.base import Finding
import ast

def find_improper_compares(filepath: str) -> list[Finding]:
    """given a python file path, return a list of Findings for improper comparisons using '==' rather than 'is' with keyword constants"""
    with open(filepath) as f:
        src = f.read()
    tree = ast.parse(src)

    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            compare_node_left = node.left
            compare_node_ops = node.ops[0]
            compare_node_right = node.comparators[0]
            if isValidConst(compare_node_right) or isValidConst(compare_node_left):
                if isinstance(compare_node_ops, (ast.Eq, ast.NotEq)):
                    result.append(Finding(
                        rule_id="improper-compares",
                        message=f"Improper comparison using operator '{'!=' if isinstance(compare_node_ops, ast.NotEq) else '=='}' with keyword constant in line {node.lineno}",
                        line=node.lineno
                    ))

    return result

def isValidConst(node):
    if isinstance(node, ast.Constant):
        val = node.value
        if isinstance(val, bool) or val is None:
            return True
    else:
        return False