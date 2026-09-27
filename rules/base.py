# defining a standard structure for rules to output
from dataclasses import dataclass
import hashlib

@dataclass  # basically a python shortcut for a class with no manual __init__
class Finding:
    rule_id: str    # an identifier ex. "unused-imports", "mutable-default-args"
    message: str
    line: int
    
    @property # property attribute class
    def id(self) -> str:
        # give each instance Finding a unique id stable across runs, 
        # so the same file-line-finding gives the same ID every time (without a database)
        # IDs needed for user flagging and metric collection
        raw_id = f"{self.rule_id}:{self.line}:{self.message}" # combo of fields
        encoded = hashlib.sha256(raw_id.encode()).hexdigest() # 64 digit encode
        return encoded[:8] 
    # return the first 8 digits like a commit ID, since 64 is way too many
    # 2^8 = worst case 256 incredibly similarly hashed issues. very unlikely
        