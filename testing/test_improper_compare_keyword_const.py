# testing/improper_compare_keyword_const.py
from rules.improper_compare_keyword_const import find_improper_compares


def test_improper_expr_with_eq(tmp_path):
    code = """
x == True
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_improper_compares(str(file))

    assert result == [("Improper Use of \"==\"", 2)]

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

    assert result == [("Improper Use of \"==\"", 2)]

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
