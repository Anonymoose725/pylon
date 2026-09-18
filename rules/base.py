# defining a standard structure for rules to output
from dataclasses import dataclass

@dataclass  # basically a python shortcut for a class with no manual __init__
class Finding:
    rule_id: str    # an identifier ex. "unused-imports", "mutable-default-args"
    message: str
    line: int