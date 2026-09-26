from rules.bare_excepts import find_bare_excepts
from rules.unused_imports import find_unused_imports
from rules.mutable_default_args import find_mutable_defaults
from rules.wildcard_imports import find_wildcard_imports
from rules.excessive_function_arguments import find_excessive_function_arguments

ALL_RULES = [
    find_bare_excepts,
    find_unused_imports,
    find_mutable_defaults,
    find_wildcard_imports,
    find_excessive_function_arguments
]