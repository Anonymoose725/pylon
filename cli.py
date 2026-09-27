# https://click.palletsprojects.com/en/stable/
import click
from pathlib import Path
from rules.registry import ALL_RULES
from ai.providers import get_provider
from ai.explain import explain_finding

def find_python_files(filepath: str) -> list[Path]:
    """Find all python files in a directory and return as list[Path]"""
    p = Path(filepath)
    # check if path is valid
    if not p.exists():
        click.echo(f"{filepath} is not a valid directory.")
        return []

    if p.is_file() and p.suffix == ".py":
        return [p]  # singleton file to append
    if p.is_file():
        return []   # not a python file

    return list(p.rglob("*.py")) # recursively search the directory


def get_snippet(filepath: Path, finding_line, margin = 25) -> str:
    """Receive a file and line number for a known finding, grab surrounding `margin` lines of code, and return the snippet as a surrounding context"""
    with open(filepath) as f:
        all_lines = f.readlines()
        
    first = max(0, finding_line - margin - 1) # -1 for from-zero indexing
    last = min(len(all_lines), finding_line + margin)
    
    return "".join(all_lines[first:last]) # concatenate lines from first to last and return as a new string

@click.command()
@click.argument("filepath")
@click.option("--explain", is_flag=True, help="Generate LLM explanations for each finding, using surrounding context.") # explain flag calls LLM layer
@click.option("--provider", default="ollama", help="LLM provider for --explain (ollama, anthropic, openai)")
def check(filepath, explain, provider):
    """Run all Pylon validation rules on the specified Python file or directory and print findings with LLM insight if explaining."""
    files = find_python_files(filepath)
    click.echo(f"Validating {len(files)} file(s)...")
    
    llm = get_provider(provider) if explain else None # dont fill if not explaining. here rather than in 'if explain' so it isnt recomputed

    all_findings = []
    for file in files:
        for rule in ALL_RULES:
            # need source file as well as the finding
            findings = rule(str(file))
            for finding in findings:
                all_findings.append((file, finding)) # returning a zipped tuple for later report
            

    if not all_findings: # if all_findings == []
        click.echo("No issues found! :)")
        return
    
    else: # all_findings != []
        for file, finding in sorted(all_findings, key=lambda pair: pair[1].line): # sorts by file by line number, with (file, _) used
            click.echo(f"{file}:{finding.line}: [{finding.rule_id}] {finding.message}")
            
            if explain: # employ the LLM layer!
                source_snippet = get_snippet(file, finding.line) # helper
            
                explanation = explain_finding(finding, source_snippet, llm)
                click.echo(f"   --> {explanation}")
        
    raise SystemExit(1)

if __name__ == "__main__":
    check()