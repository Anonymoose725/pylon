# https://click.palletsprojects.com/en/stable/
import click
from pathlib import Path
from rules.registry import ALL_RULES

def find_python_files(filepath: str) -> list[Path]:
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


@click.command()
@click.argument("filepath")
def check(filepath):
    """Run all Pylon validation rules on the specified Python file or directory and print findings."""
    files = find_python_files(filepath)
    click.echo(f"Validating {len(files)} file(s)...")

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
            raise SystemExit(1)

if __name__ == "__main__":
    check()