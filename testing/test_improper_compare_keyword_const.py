from rules.improper_compare_keyword_const import find_improper_compares
from rules.base import Finding
from test_util import create_test_file


def test_improper_expr_with_eq(tmp_path):
    """Test detection of improper comparison: x == True"""
    code = """x == True"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == [Finding(
        rule_id="improper-compares",
        message=f"Improper comparison using operator '==' with keyword constant in line 1",
        line=1
    )]


def test_proper_expr_with_is(tmp_path):
    """Test that proper comparison: x is True, is not flagged"""
    code = """x is True"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == []


def test_improper_if_with_eq(tmp_path):
    """Test detection of improper comparison in if statement: if x == True:"""
    code = """if x == True: True"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == [Finding(
        rule_id="improper-compares",
        message=f"Improper comparison using operator '==' with keyword constant in line 1",
        line=1
    )]


def test_proper_if_with_is(tmp_path):
    """Test that proper if statement: if x is True: is not flagged"""
    code = """if x is True: True"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == []


def test_proper_if_without_is(tmp_path):
    """Test that comparison with non-boolean constant is not flagged"""
    code = """if x == 5: True"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == []


def test_proper_expr_without_is(tmp_path):
    """Test that expression with non-boolean constant is not flagged"""
    code = """x == 5"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == []


def test_proper_expr_is_none(tmp_path):
    """Test that proper None comparison: x is None is not flagged"""
    code = """x is None"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == []


def test_improper_if_eq_none(tmp_path):
    """Test detection of improper comparison: if x == None:"""
    code = """if x == None: True"""
    file = create_test_file(tmp_path, code)

    result = find_improper_compares(str(file))

    assert result == [Finding(
        rule_id="improper-compares",
        message=f"Improper comparison using operator '==' with keyword constant in line 1",
        line=1
    )]