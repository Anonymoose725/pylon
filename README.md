## Pylon

Pylon is a static analysis CLI for Python that flags real issues in your code and, on request, explains them and suggests fixes using an LLM.

Pylon mostly utilises Python's included [ast module](https://docs.python.org/3/library/ast.html) to traverse source code.

Built in collaboration with [Soham200613](https://github.com/Soham200613)

## List of rules to implement, so far

- Bare `except:` clauses, catching all exceptions, including KeyboardInterrupt and SystemExit, silently swallow bugs,
making debugging difficult
- Shadowed builtin types, caused by naming variables `list`, `dict`, `id`, `type`, etc. Check `ast.arg` names and assignment
targets against a known set of builtin names
- Too many function arguments, hard to maintain and signal a function is doing too much work. Let's say more than 7? Use
count the number of (length of []) `node.args.args` on `ast.FunctionDef`
- Comparing statements using `==` instead of `is` for None, True, False, etc. Check for `ast.Compare` nodes where one side is
`ast.Constant` with value None, True, etc. and check the operator is `Eq` or `NotEq`
- Unused function args: check for parameters never used in the function body. Signals incomplete refactoring or unfinished/dead code. Walk and collect `ast.Name` usages, similar to unused_imports. Apply per-function rather than per-file.
- Global variables state changed inside a function, using the `global` keyword inside the function to alter outer-scope variables. Often a hard to trace bug. Check for `ast.Global` nodes within functions.
- Wildcard imports: `from module import *` is not healthy, check `ast.ImportFrom` where `node.names[0].name == "8"`
- Heavily nested code, resulting in high complexity. A warning on program efficiency. With many while/if/for/try blocks nested, hard to read. Would need to track nesting depth and/or branch count while walking rather than at a single node. Involves breaking apart ast.walk().


## Setup, for contributors:

Clone the repo:
```bash
git clone https://github.com/Anonymoose725/pylon.git
cd pylon
```

Create and activate virtual environments:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

Run test suite to confirm everything works:
```bash
pytest testing/ -v
```


## On the roadmap

1. Update bare-except to find a catch-and-reraise pattern. In testing the CLI, I found a bare except in Python-Flask's src/flask/app.py. This is deliberately placed and not a poor use of
bare exception catching. Typically, following the pattern:
```python
except:
    error = sys.exc_info()[1]
    raise
```
so we can easily track and find except:...raise

2. Double import patterns are not unused imports.
```python
from .app import Flask as Flask
from .helpers import abort as abort
```
This is again deliberate and allows users of Flask to do `import Flask as Flask` as opposed to `import Flask.app as Flask`. We can check for this pattern!