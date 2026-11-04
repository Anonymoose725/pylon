from pathlib import Path
from click.testing import CliRunner
import cli as cli_module
from rules.base import Finding


def write_python_file(directory: Path, name: str, source: str = "x = 1\n") -> Path:
    """Create a Python file under directory and return its path."""
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def make_finding(
    rule_id: str = "example-rule",
    message: str = "Example finding",
    line: int = 1,
) -> Finding:
    return Finding(rule_id=rule_id, message=message, line=line)


# find_python_files
# ___________________________________________________________________________________

def test_find_python_files_returns_single_python_file(tmp_path):
    source = write_python_file(tmp_path, "example.py")

    assert cli_module.find_python_files(str(source)) == [source]


def test_find_python_files_recursively_finds_python_files(tmp_path):
    first = write_python_file(tmp_path, "first.py")
    second = write_python_file(tmp_path, "nested/second.py")
    write_python_file(tmp_path, "notes.txt")

    result = cli_module.find_python_files(str(tmp_path))

    assert set(result) == {first, second}


def test_find_python_files_returns_empty_for_non_python_file(tmp_path):
    source = tmp_path / "notes.txt"
    source.write_text("not Python", encoding="utf-8")

    assert cli_module.find_python_files(str(source)) == []


def test_find_python_files_returns_empty_for_missing_path(tmp_path):
    missing = tmp_path / "does-not-exist"

    assert cli_module.find_python_files(str(missing)) == []


# get_snippet
# ___________________________________________________________________________________


def test_get_snippet_marks_the_finding_line(tmp_path):
    source = write_python_file(
        tmp_path,
        "example.py",
        "first = 1\nsecond = 2\nthird = 3\n",
    )

    result = cli_module.get_snippet(source, finding_line=2, margin=1)

    assert result == (
        "    1: first = 1\n"
        "----> 2: second = 2\n"
        "    3: third = 3\n"
    )


def test_get_snippet_clamps_context_at_start_of_file(tmp_path):
    source = write_python_file(
        tmp_path,
        "example.py",
        "first = 1\nsecond = 2\nthird = 3\n",
    )

    result = cli_module.get_snippet(source, finding_line=1, margin=2)

    assert result == (
        "----> 1: first = 1\n"
        "    2: second = 2\n"
        "    3: third = 3\n"
    )


def test_get_snippet_clamps_context_at_end_of_file(tmp_path):
    source = write_python_file(
        tmp_path,
        "example.py",
        "first = 1\nsecond = 2\nthird = 3\n",
    )

    result = cli_module.get_snippet(source, finding_line=3, margin=2)

    assert result == (
        "    1: first = 1\n"
        "    2: second = 2\n"
        "----> 3: third = 3\n"
    )


# check command: validation and reporting
# ___________________________________________________________________________________


def test_check_reports_number_of_files(tmp_path, monkeypatch):
    write_python_file(tmp_path, "first.py")
    write_python_file(tmp_path, "second.py")
    monkeypatch.setattr(cli_module, "ALL_RULES", [])

    result = CliRunner().invoke(cli_module.check, [str(tmp_path)])

    assert result.exit_code == 0
    assert "Validating 2 file(s)..." in result.output


def test_check_reports_no_issues_when_rules_find_nothing(tmp_path, monkeypatch):
    write_python_file(tmp_path, "example.py")
    monkeypatch.setattr(cli_module, "ALL_RULES", [lambda filepath: []])

    result = CliRunner().invoke(cli_module.check, [str(tmp_path)])

    assert result.exit_code == 0
    assert "No issues found! :)" in result.output


def test_check_reports_finding_and_exits_with_code_one(tmp_path, monkeypatch):
    source = write_python_file(tmp_path, "example.py")
    finding = make_finding(
        rule_id="improper-compares",
        message="Improper comparison using == with True",
        line=1,
    )
    monkeypatch.setattr(cli_module, "ALL_RULES", [lambda filepath: [finding]])

    result = CliRunner().invoke(cli_module.check, [str(source)])

    assert result.exit_code == 1
    assert f"{source}:1: [improper-compares] Improper comparison using == with True" in result.output


def test_check_runs_each_rule_for_each_python_file(tmp_path, monkeypatch):
    first = write_python_file(tmp_path, "first.py")
    second = write_python_file(tmp_path, "second.py")
    calls = []

    def rule(filepath):
        calls.append(Path(filepath))
        return []

    monkeypatch.setattr(cli_module, "ALL_RULES", [rule])

    result = CliRunner().invoke(cli_module.check, [str(tmp_path)])

    assert result.exit_code == 0
    assert set(calls) == {first, second}
    assert len(calls) == 2


def test_check_orders_findings_by_line_number(tmp_path, monkeypatch):
    source = write_python_file(
        tmp_path,
        "example.py",
        "one = 1\ntwo = 2\nthree = 3\n",
    )
    later = make_finding("later-rule", "Later finding", line=3)
    earlier = make_finding("earlier-rule", "Earlier finding", line=1)
    monkeypatch.setattr(
        cli_module,
        "ALL_RULES",
        [lambda filepath: [later, earlier]],
    )

    result = CliRunner().invoke(cli_module.check, [str(source)])

    assert result.exit_code == 1
    assert result.output.index("[earlier-rule]") < result.output.index("[later-rule]")


def test_check_does_not_initialize_provider_without_explain(tmp_path, monkeypatch):
    source = write_python_file(tmp_path, "example.py")
    provider_calls = []

    def unexpected_provider_call(name):
        provider_calls.append(name)
        raise AssertionError("Provider should not be initialized without --explain")

    monkeypatch.setattr(cli_module, "ALL_RULES", [])
    monkeypatch.setattr(cli_module, "get_provider", unexpected_provider_call)

    result = CliRunner().invoke(
        cli_module.check,
        [str(source), "--provider", "openai"],
    )

    assert result.exit_code == 0
    assert provider_calls == []


# check command: LLM explanations
# ___________________________________________________________________________________


def test_check_initializes_selected_provider_when_explain_is_enabled(
    tmp_path, monkeypatch
):
    source = write_python_file(tmp_path, "example.py")
    finding = make_finding()
    provider = object()
    provider_calls = []

    monkeypatch.setattr(cli_module, "ALL_RULES", [lambda filepath: [finding]])

    def fake_get_provider(name):
        provider_calls.append(name)
        return provider

    monkeypatch.setattr(cli_module, "get_provider", fake_get_provider)
    monkeypatch.setattr(
        cli_module,
        "explain_finding",
        lambda finding, snippet, llm: "A helpful explanation",
    )

    result = CliRunner().invoke(
        cli_module.check,
        [str(source), "--explain", "--provider", "openai"],
    )

    assert result.exit_code == 1
    assert provider_calls == ["openai"]
    assert "--> A helpful explanation" in result.output


def test_check_passes_finding_snippet_and_provider_to_explainer(
    tmp_path, monkeypatch
):
    source = write_python_file(
        tmp_path,
        "example.py",
        "first = 1\nproblem = (1 == True)\nlast = 3\n",
    )
    finding = make_finding(line=2)
    provider = object()
    received = {}

    monkeypatch.setattr(cli_module, "ALL_RULES", [lambda filepath: [finding]])
    monkeypatch.setattr(cli_module, "get_provider", lambda name: provider)

    def fake_explain_finding(actual_finding, snippet, actual_provider):
        received["finding"] = actual_finding
        received["snippet"] = snippet
        received["provider"] = actual_provider
        return "Explanation"

    monkeypatch.setattr(cli_module, "explain_finding", fake_explain_finding)

    result = CliRunner().invoke(
        cli_module.check,
        [str(source), "--explain"],
    )

    assert result.exit_code == 1
    assert received["finding"] is finding
    assert "----> 2: problem = (1 == True)" in received["snippet"]
    assert received["provider"] is provider


def test_check_uses_default_provider_when_explain_is_enabled(
    tmp_path, monkeypatch
):
    source = write_python_file(tmp_path, "example.py")
    provider_calls = []

    monkeypatch.setattr(cli_module, "ALL_RULES", [])
    monkeypatch.setattr(
        cli_module,
        "get_provider",
        lambda name: provider_calls.append(name) or object(),
    )

    result = CliRunner().invoke(
        cli_module.check,
        [str(source), "--explain"],
    )

    assert result.exit_code == 0
    assert provider_calls == ["ollama"]


def test_check_propagates_unknown_provider_error_when_explaining(
    tmp_path, monkeypatch
):
    source = write_python_file(tmp_path, "example.py")
    monkeypatch.setattr(cli_module, "ALL_RULES", [])

    def fake_get_provider(name):
        raise ValueError(f"Unknown LLM provider: {name}")

    monkeypatch.setattr(cli_module, "get_provider", fake_get_provider)

    result = CliRunner().invoke(
        cli_module.check,
        [str(source), "--explain", "--provider", "unknown"],
    )

    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "Unknown LLM provider: unknown" in str(result.exception)


# Click argument and option handling
# ___________________________________________________________________________________


def test_check_requires_filepath():
    result = CliRunner().invoke(cli_module.check, [])

    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_check_help_displays_cli_options():
    result = CliRunner().invoke(cli_module.check, ["--help"])

    assert result.exit_code == 0
    assert "--explain" in result.output
    assert "--provider" in result.output