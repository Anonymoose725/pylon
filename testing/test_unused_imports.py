# run from project root
from rules.unused_imports import find_unused_imports

def test_detects_unused_imports(tmp_path):
    code = """
import os
import sys
from collections import Counter

print(os.getcwd())
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == {"sys", "Counter"}

def test_all_imports_used(tmp_path):
    code = """
import os
print(os.getcwd())
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == set()
    
def test_no_imports(tmp_path):
    code = "print('hello')"
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == set()

def test_aliased_unused_imports(tmp_path):
    code = """
import os
import numpy as lumpy

print(os.getcwd())
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == {"lumpy"}    
