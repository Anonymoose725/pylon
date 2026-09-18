# testing/improper_compare_keyword_const.py
from rules.improper_compare_keyword_const import find_improper_compares


def test_improper_expr_with_eq(tmp_path):
    code = """
x == True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == [2]

def test_proper_expr_with_is(tmp_path):
    code = """
x is True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == []

def test_improper_if_with_eq(tmp_path):
    code = """
if x == True: True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == [2]

def test_proper_if_with_is(tmp_path):
    code = """
if x is True: True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == []

def test_proper_if_without_is(tmp_path):
    code = """
if x == 5: True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == []

def test_proper_expr_without_is(tmp_path):
    code = """
x == 5
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == []

def test_proper_expr_is_none(tmp_path):
    code = """
x is None
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == []

def test_improper_if_eq_none(tmp_path):
    code = """
if x == None: True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == [2]

def test_improper_compare_multiple(tmp_path):
    code = """
def func1(x):
    if x == None: 
        return 1
    else:
        return 2

def func2(y):
    if y == None:
        return 2
    else:
        return 1
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_improper_compares(str(file))
    
    assert result == [3, 9]
    