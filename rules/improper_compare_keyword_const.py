""" 
- Comparing statements using `==` instead of `is` for None, True, False, etc. Check for `ast.Compare` nodes where one side is
`ast.Constant` with value None, True, etc. and check the operator is `Eq` or `NotEq` 

"""

import ast

code = "x == True"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
print("SPACE")
code = "x is True"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
print("SPACE")
code = "x == 5"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
print("SPACE")
code = "5 == x"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
print("SPACE")
code = "x == True"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))

import ast

def find_improper_compares(filepath: str):
    """given a python file path, return a list (module, lineno) of wilcard imports"""
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
                if isinstance(compare_node_ops, ast.Eq):
                    result.append(("Improper Use of \"==\"", node.lineno))
      
    return result

def isValidConst(node):
    if isinstance(node, ast.Constant):
        val = node.value
        if isinstance(val, bool) or val is None:
            return True
    else:
        return False