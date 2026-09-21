# https://click.palletsprojects.com/en/stable/
import click
from rules.registry import ALL_RULES

@click.command()
@click.argument("filepath")

def check(filepath):
    """Run all Pylon validation rules on the specified Python file and print findings."""
    all_findings = []
    for rule in ALL_RULES:
        all_findings.extend(rule(filepath))

    if not all_findings: # if all_findings == []
        click.echo("No issues found! :)")
        return

    for finding in sorted(all_findings, key=lambda f: f.line): # sorts findings by line number regardless of which rule found them
        click.echo(f"{filepath}:{finding.line}: [{finding.rule_id}] {finding.message}")

if __name__ == "__main__":
    check()