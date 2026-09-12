# run from project root
from rules.mutable_default_args import find_mutable_defaults

def test_find_mutable_default_args(tmp_path):
    code = """
def add_item(item, items=[]):
    items.append(item)
    return items
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
    result = find_mutable_defaults(str(file))
    
    assert result == [("add_item", 2)]
    
def test_immutable_default_arg_not_flagged(tmp_path):
    code = """
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
"""
    file = tmp_path / "sample.py"
    file.write_text(code)
    
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
    file = tmp_path / "sample.py"
    file.write_text(code)
        
    result = find_mutable_defaults(str(file))
        
    assert result == [("add_item_to_list", 2),("add_item_to_set", 6)] # counting the newline after """ in lineno