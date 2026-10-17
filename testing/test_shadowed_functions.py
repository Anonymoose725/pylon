from rules.base import Finding
from rules.shadowed_functions import find_shadowed_functions
from test_util import create_test_file

# test helpers ---------
def run(tmp_path, code):
    return find_shadowed_functions(str(create_test_file(tmp_path, code)))

# easier not to retype
def shadowed(name, kind, first_line, line):
    """Expected finding. `kind` and `first_line` describe the EARLIER definition;
    `line` is where the shadowing happens."""
    return Finding(
        rule_id="shadowed-function",
        message=f"'{name}' redefined; the {kind} on line {first_line} is shadowed",
        line=line,
    )


# tests!

def test_find_shadowed_functions(tmp_path):
    code = """
def myFunc():
    print("Hello!")
def myFunc():
    print("Hello again!")
"""
    assert run(tmp_path, code) == [shadowed("myFunc", "function", 2, 4)]


def test_find_shadowed_functions_not_flagged(tmp_path):
    code = """
def myFunct():
    print("Hello!")
"""
    assert run(tmp_path, code) == []


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
    assert run(tmp_path, code) == [
        shadowed("myFunc", "function", 2, 4),
        shadowed("myFuncToo", "function", 8, 10),
    ]

# scoping tests -------

def test_methods_in_different_classes_not_flagged(tmp_path):
    code = """
class A:
    def save(self): ...
class B:
    def save(self): ...
"""
    assert run(tmp_path, code) == []


def test_duplicate_method_in_same_class_flagged(tmp_path):
    code = """
class A:
    def save(self): ...
    def save(self): ...
"""
    assert run(tmp_path, code) == [shadowed("save", "function", 3, 4)]
    

def test_if_else_branches_not_flagged(tmp_path):
    code = """
import sys
if sys.version_info >= (3, 11):
    def f(): ...
else:
    def f(): ...
"""
    assert run(tmp_path, code) == []


def test_nested_helpers_in_different_functions_not_flagged(tmp_path):
    code = """
def outer1():
    def helper(): ...
def outer2():
    def helper(): ...
"""
    assert run(tmp_path, code) == []


def test_class_then_function_same_name_flagged(tmp_path):
    code = """
class Foo: ...
def Foo(): ...
"""
    assert run(tmp_path, code) == [shadowed("Foo", "class", 2, 3)]


def test_async_then_sync_same_name_flagged(tmp_path):
    code = """
async def run(): ...
def run(): ...
"""
    assert run(tmp_path, code) == [shadowed("run", "async function", 2, 3)]


def test_three_definitions_give_two_findings(tmp_path):
    code = """
def f(): ...
def f(): ...
def f(): ...
"""
    # each definition is compared against the one immediately before it
    assert run(tmp_path, code) == [
        shadowed("f", "function", 2, 3),
        shadowed("f", "function", 3, 4),
    ]
    
    
# exemption cases ---------

def test_overload_stubs_not_flagged(tmp_path):
    code = """
from typing import overload
@overload
def f(a: int) -> int: ...
@overload
def f(a: str) -> str: ...
def f(a): return a
"""
    assert run(tmp_path, code) == []


def test_property_setter_not_flagged(tmp_path):
    code = """
class C:
    @property
    def x(self): ...
    @x.setter
    def x(self, v): ...
"""
    assert run(tmp_path, code) == []


def test_singledispatch_registrations_not_flagged(tmp_path):
    code = """
from functools import singledispatch
@singledispatch
def show(x): ...
@show.register
def _(x: int): ...
@show.register
def _(x: str): ...
"""
    assert run(tmp_path, code) == []


def test_duplicate_decorated_functions_still_flagged(tmp_path):
    code = """
import pytest
@pytest.fixture
def data(): ...
@pytest.fixture
def data(): ...
"""
    assert run(tmp_path, code) == [shadowed("data", "function", 4, 6)]