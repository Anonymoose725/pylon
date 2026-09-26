import time
from pathlib import Path
from cli import find_python_files
from rules.registry import ALL_RULES

# point to respective source folders for each repo only, so we exclude things like setup .py scripts
REPOS = {
    "flask": "benchmarks/flask/src",
    "requests": "benchmarks/requests/src",
    "click": "benchmarks/click/src",
    "django": "benchmarks/django/django",
    "numpy": "benchmarks/numpy/numpy"
}

def count_lines(files):
    total = 0;
    for f in files:
        with open(f, encoding="utf-8", errors="ignore") as fh:
            total += sum(1 for _ in fh)
    return total

def main():
    grand_total_files = 0
    grand_total_lines = 0
    grand_total_findings = 0
    per_rule_totals = {}
    
    for repo_name, path_to_repo in REPOS.items():
        if not Path(path_to_repo).exists():
            print(f"Skipping {repo_name}, path not found: {path_to_repo}")
            continue
        
        files = find_python_files(path_to_repo)
        lines = count_lines(files)
        
        start = time.perf_counter()
        findings_this_repo = 0
        for file in files:
            for rule in ALL_RULES:
                results = rule(str(file))
                if results is not None:
                    findings_this_repo += len(results)
                    for finding in results:
                        per_rule_totals[finding.rule_id] = per_rule_totals.get(finding.rule_id, 0) + 1 # mapping +1
                    
        elapsed = time.perf_counter() - start # record time taken to find all findings in this repo
        
        print(f"\n{repo_name}")
        print(f"    files:      {len(files)}")
        print(f"    lines:      {lines}")
        print(f"    findings:   {findings_this_repo}")
        print(f"    time:       {elapsed:.2f}s ({len(files)/elapsed:.1f} files/s)")
        
        grand_total_files += len(files)
        grand_total_lines += lines
        grand_total_findings += findings_this_repo
        
    print(f"\n--------> total <--------\n")
    print(f"    files:      {grand_total_files}")
    print(f"    lines:      {grand_total_lines}")
    print(f"    findings:   {grand_total_findings}")
    print(f"\nfindings by rule:")
    for rule_id, count in sorted(per_rule_totals.items(), key=lambda x: -x[1]):
        print(f"    {rule_id}: {count}")

if __name__ == "__main__":
    main()
        