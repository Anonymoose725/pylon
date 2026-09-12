from rules.bare_excepts import find_bare_excepts

def test_find_bare_except(tmp_path):
    code = """
try:
    val = 100
    result = 10 / val
except:
    print("This catches all exceptions!")    
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_bare_excepts(str(file))
    
    assert result == [5]
    
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
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_bare_excepts(str(file))
    
    assert result == [5,12]