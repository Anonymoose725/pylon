# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands Reference

### Build/Install
```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

### Run Tests
```bash
pytest testing/ -v                    # run all tests with verbose output
pytest testing/test_bare_excepts.py -v  # single test file
pytest testing/test_improper_compare_keyword_const.py -v  # single test function example: pytest testing/test_improper_compare_keyword_const.py::test_find_all_bare_except -v
```

### Run the Static Analyzer
```bash
pylon path/to/file.py                # run all rules on a single file
pylon path/to/dir/                   # recursively analyze directory
pylon path/to/file.py --explain      # flag issues + get LLM explanations (uses Ollama by default)
pylon path/to/file.py --explain --provider anthropic  # use Anthropic API
pylon path/to/file.py --explain --provider openai     # use OpenAI API
```

## Architecture Overview

Pylon is a **static analysis CLI for Python** that uses AST traversal to detect code anti-patterns. It has two layers:

### 1. Deterministic Rule Engine (`rules/*.py`)
- Each rule lives in its own file under `rules/` (e.g., `bare_excepts.py`, `unused_imports.py`)
- Rules implement a consistent pattern: read file → parse AST → return `list[Finding]`
- `Finding` is a dataclass (`rule_id`, `message`, `line`) defined in `rules/base.py`
- All rules registered in `rules/registry.py` as the `ALL_RULES` list
- New rules follow: create file, add import to `registry.py`, write test in `testing/`

### 2. LLM Explanation Layer (`ai/`)
- When `--explain` flag is used, findings are sent to an LLM for contextual judgment
- Providers abstracted behind `ai/providers/base.py` (Ollama, Anthropic, OpenAI)
- Prompt logic in `ai/explain.py` — keeps explanations under 2-3 sentences

### CLI Entry Point (`cli.py`)
- Built with Click; single `check()` command routes through `ALL_RULES`
- Collects all findings → sorts by file:line → prints with optional LLM explanations
- Uses `find_python_files()` helper to resolve path (file, dir, or singleton)

## Key Patterns to Follow

### Adding a New Rule
1. Create `rules/new_rule.py` with function signature: `def find_new_rule(filepath: str) -> list[Finding]`
2. Add import in `rules/registry.py`: `from rules.new_rule import find_new_rule`
3. Append to `ALL_RULES = [..., find_new_rule]`
4. Write positive/negative tests in `testing/test_new_rule.py`

### Rule Output Structure
All findings must be `Finding` instances with:
- `rule_id`: slug like `"bare-except"`, `"unused-import"` (no hyphens in messages)
- `message`: human-readable description of the issue
- `line`: 1-indexed line number from source

Example Finding:
```python
Finding(
    rule_id="improper-compares",
    message="Improper comparison using operator '==' with keyword constant in line X",
    line=5
)
```

### AST Pattern Consistency
- Use `ast.parse()` → `ast.walk()` to traverse tree
- For unused imports: collect `ast.Import/ImportFrom` nodes, match against `ast.Name` usage
- For argument checking: walk function bodies and track `ast.arg` references
- For mutable defaults: check function argument defaults in `ast.FunctionDef` nodes

## Implemented Rules (as of Oct 2026)

| Rule | Description |
|------|-------------|
| bare-except | Bare `except:` clauses that catch all exceptions including KeyboardInterrupt |
| unused-import | Imports never referenced in file body; respects `__all__` exports and aliased imports |
| mutable-default | Mutable default args like `def f(x=[])` which accumulate state across calls |
| wildcard-import | `from module import *` statements that pollute namespace |
| improper-compares | '!=' or '==' rather than `is not` or other comparisons with constants like None/True/False |

## LLM Layer Details

The `--explain` flag routes each finding through an LLM for judgment. Prompts are templated with:
- Finding metadata (`rule_id`, `line`, `message`)
- Source code snippet (25 lines before/after the violation)
- Constraints: 2-3 sentences max, avoid overconfidence, note if likely false positive

Supported providers: `ollama` (default), `anthropic`, `openai`. API keys go in `.env`.

## Testing Philosophy

Every rule must have:
1. **Positive test**: Code that should trigger the finding
2. **Negative test**: Idiomatic code that should NOT be flagged
3. Edge cases for special patterns (e.g., catch-and-re-raise for bare-except)

Use `testing/test_util.py::create_test_file()` helper to create temp files in tests.

## Validation Benchmarks

Pylon was validated against 5 actively maintained production codebases:

| Repo | Files | Lines | Findings |
|---|---|---|---|
| Flask | 24 | 9,513 | 32 |
| Requests | 19 | 6,394 | 56 |
| Click | 17 | 12,821 | 19 |
| Django | 907 | 165,529 | 198 |
| NumPy | 428 | 260,868 | 764 |
| **Total** | **1,395** | **455,125** | **1,069** |

## LLM Providers Setup

```bash
# For Ollama (default, local models)
# Install ollama and pull a model:
ollama pull qwen2.5:7b-coder

# For Anthropic/OpenAI, set API keys in .env:
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## Rules Roadmap

Pending implementations:
- excessive-function-arguments: Functions with too many parameters
- shadowed-builtins: Variables shadowing builtins like `list`, `dict`, `id`
- unused-function-arguments: Parameters never referenced in function body
- global-variable-mutation: `global` usage to mutate outer-scope state
- cyclomatic-complexity: Tracking nesting depth/branch count while walking AST
