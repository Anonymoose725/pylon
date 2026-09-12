import pytest

def func(x):
    return x+1

def test_answer():
    assert func(3) == 4 # assert that func(3) outputs 4
    
def f():
    raise SystemExit(1)

def test_myTest():
    with pytest.raises(SystemExit): # assert that f() raises an exception of type SystemExit
        f()