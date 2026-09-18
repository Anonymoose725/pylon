# testing/test_wildcard_imports.py
from rules.base import Finding
from rules.wildcard_imports import find_wildcard_imports


def test_detects_wildcard_import(tmp_path):
    code = """
from os import *
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_wildcard_imports(str(file))

    assert result == [Finding(rule_id="wildcard-import", message="Wildcard import from 'os'", line=2)]


def test_no_wildcard_import_not_flagged(tmp_path):
    code = """
from os import path
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_wildcard_imports(str(file))

    assert result == []


def test_multiple_wildcard_imports(tmp_path):
    code = """
from os import *
from sys import *
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_wildcard_imports(str(file))

    assert result == [Finding(rule_id="wildcard-import", message="Wildcard import from 'os'", line=2), 
                      Finding(rule_id="wildcard-import", message="Wildcard import from 'sys'", line=3)]


def test_regular_import_not_flagged(tmp_path):
    code = """
import os
"""
    file = tmp_path / "sample.py"
    file.write_text(code)

    result = find_wildcard_imports(str(file))

    assert result == []