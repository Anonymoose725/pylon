# run from project root
from rules.base import Finding
from rules.mutable_default_args import find_mutable_defaults
from test_util import create_test_file

def test_find_mutable_default_args(tmp_path):
    code = """
def add_item(item, items=[]):
    items.append(item)
    return items
"""
    file = create_test_file(tmp_path, code)
    
    result = find_mutable_defaults(str(file))
    
    assert result == [Finding(rule_id="mutable-default", message="Mutable default argument in function def 'add_item'", line=2)]
    
def test_immutable_default_arg_not_flagged(tmp_path):
    code = """
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
"""
    file = create_test_file(tmp_path, code)
    
    result = find_mutable_defaults(str(file))
    
    assert result == []


def test_multiple_mutable_default_args_detected(tmp_path):
    code = """
def add_item_to_list(item, items=[]):
    items.append(item)
    return items

def add_item_to_set(item, items=set()):
    items.add(item)
    return items
"""
    file = create_test_file(tmp_path, code)
        
    result = find_mutable_defaults(str(file))
        
    assert result == [Finding(rule_id="mutable-default", message="Mutable default argument in function def 'add_item_to_list'", line=2),
                      Finding(rule_id="mutable-default", message="Mutable default argument in function def 'add_item_to_set'", line=6)]