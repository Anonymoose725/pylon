from rules.bare_excepts import find_bare_excepts
from rules.base import Finding
from test_util import create_test_file

def test_find_bare_except(tmp_path):
    code = """
try:
    val = 100
    result = 10 / val
except:
    print("This catches all exceptions!")    
"""
    file = create_test_file(tmp_path, code)
    
    result = find_bare_excepts(str(file))
    
    assert result == [Finding(rule_id="bare-except", message="Bare except clause found in try block", line=5)]
    
def test_find_all_bare_excepts(tmp_path):
    code = """
try:
    val = 100
    result = 10 / val
except:
    print("This catches all exceptions!")  
try:
    name = ethan
    age = 20
except ValueError:
    print("This is an appropriate use of exception handling")
except:
    print("This is not!")
"""
    file = create_test_file(tmp_path, code)
    
    result = find_bare_excepts(str(file))
    
    assert result == [Finding(rule_id="bare-except", message="Bare except clause found in try block", line=5),
                      Finding(rule_id="bare-except", message="Bare except clause found in try block", line=12)]