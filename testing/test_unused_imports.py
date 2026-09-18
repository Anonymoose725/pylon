# run from project root
from rules.base import Finding
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
    
    assert result == [Finding(rule_id="unused-import", message="Unused import from 'sys'", line=3),
                      Finding(rule_id="unused-import", message="Unused import from 'Counter'", line=4)]

def test_all_imports_used(tmp_path):
    code = """
import os
print(os.getcwd())
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == []
    
def test_no_imports(tmp_path):
    code = "print('hello')"
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == []

def test_aliased_unused_imports(tmp_path):
    code = """
import os
import numpy as lumpy

print(os.getcwd())
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_unused_imports(str(file))
    
    assert result == [Finding(rule_id="unused-import", message="Unused import from 'lumpy'", line=3)]
