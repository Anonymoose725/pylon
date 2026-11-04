# Pylon Agent Guide

## Commands & Workflows

- **Run analyzer**: `pylon <path-to-python-files>`
  - Accepts single file, directory, or wildcard pattern
  - Returns exit code 1 when issues found (important for CI)
  - Use `--explain` to trigger LLM explanations layer
  - LLM provider via `--provider` flag: `ollama`, `anthropic`, `openai`

- **Run tests**: `pytest testing/ -v`
- **Install from source**: `pip install -e .` (after creating venv)
- **Set API keys**: Copy `.env.example` to `.env` and fill with your keys

## Architecture Overview

**Entry point**: `cli.py` wraps Click command that:
1. Resolves input path(s) to Python files via `find_python_files()`
2. Iterates all registered rules from `rules/registry.ALL_RULES`
3. Collects findings, sorts by line number within each file
4. Optionally sends each finding to LLM via `ai.explain.explain_finding()`

**Rule registration**: Each rule in `rules/*.py` implements callable returning list of `Finding` dataclasses (`rule_id`, `message`, `line`). Rules collected into `ALL_RULES` list in `registry.py`.

**AI layer**: Providers (`ai/providers/*`) implement shared `LLMProvider` interface. Default is Ollama (`qwen2.5:7b-coder`).

## Key Implementation Details

- **Finding IDs**: Each finding has deterministic 8-char hash from `rule_id:line:message` for stable tracking across runs
- **AST-based analysis**: All rules traverse Python AST; no code execution
- **No false-positive LLM calls when `--explain` not used** (LLM only invoked via CLI flag)

## Rule Files

Located in `rules/`: bare_excepts, unused_imports, mutable_default_args, wildcard_imports, improper_compare_keyword_const, shadowed_functions, shadowed_builtins. See `registry.py` for complete list.
