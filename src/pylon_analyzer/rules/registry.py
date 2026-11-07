from pylon_analyzer.rules.bare_excepts import find_bare_excepts
from pylon_analyzer.rules.unused_imports import find_unused_imports
from pylon_analyzer.rules.mutable_default_args import find_mutable_defaults
from pylon_analyzer.rules.wildcard_imports import find_wildcard_imports
from pylon_analyzer.rules.improper_compare_keyword_const import find_improper_compares
from pylon_analyzer.rules.shadowed_functions import find_shadowed_functions
from pylon_analyzer.rules.shadowed_builtins import find_shadowed_builtins

ALL_RULES = [
    find_bare_excepts,
    find_unused_imports,
    find_mutable_defaults,
    find_wildcard_imports,
    find_improper_compares,
    find_shadowed_functions,
    find_shadowed_builtins
]