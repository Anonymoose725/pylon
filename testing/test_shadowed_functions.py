from rules.base import Finding
from rules.shadowed_functions import find_shadowed_functions
from test_util import create_test_file

def test_find_shadowed_functions(tmp_path):
    code = """
def myFunc():
    print("Hello!")
def myFunc():
    print("Hello again!")
"""
    file = create_test_file(tmp_path, code)
    
    result = find_shadowed_functions(str(file))
    
    assert result == [Finding(rule_id="shadowed-function", message="'myFunc' redefined; function definition is shadowed", line=4)]

def test_find_shadowed_functions_not_flagged(tmp_path):
    code = """
def myFunct():
    print("Hello!")
"""
    file = create_test_file(tmp_path, code)
    
    result = find_shadowed_functions(str(file))
    
    assert result == []
    
def test_multiple_shadowed_functions_detected(tmp_path):
    code = """
def myFunc():
    print("Hello!")
def myFunc():
    print("Hello again!")
def myFuncFalse():
    print("shhh")
def myFuncToo():
    print("Hello!")
def myFuncToo():
    print("Hello again!")

"""
    file = create_test_file(tmp_path, code)
    
    result = find_shadowed_functions(str(file))
    
    assert result == [Finding(rule_id="shadowed-function", message="'myFunc' redefined; function definition is shadowed", line=4),
                      Finding(rule_id="shadowed-function", message="'myFuncToo' redefined; function definition is shadowed", line=10)]
    