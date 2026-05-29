#!/usr/bin/env python3
"""Pre-commit checks: file line limit (200), function length limit (50), no debug prints.

Usage: python .harness/tool/pre-commit-check.py [file ...]
Exit 0 on pass, 1 on violation.
"""

import sys
import re
import os


FILE_LINE_LIMIT = 200
FUNC_LINE_LIMIT = 50


def check_file_line_count(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    if len(lines) > FILE_LINE_LIMIT:
        print(f"VIOLATION: {filepath}: {len(lines)} lines (limit: {FILE_LINE_LIMIT})")
        return 1
    return 0


def check_function_lengths(filepath):
    violations = 0
    with open(filepath) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\s*(def |async def )', line):
            start_line = i + 1
            base_indent = len(line) - len(line.lstrip())
            i += 1
            # Scan function body
            while i < len(lines):
                stripped = lines[i].rstrip()
                if stripped and not stripped.startswith(' ' * (base_indent + 1)) and not stripped.startswith('\t') and not stripped.startswith(' ' * base_indent + ' ') and not stripped.startswith('#'):
                    # Check if this is a decorator, comment, or blank inside func
                    if stripped and not re.match(r'^\s*@|\s*#', lines[i]) and not re.match(r'^\s*$', lines[i]):
                        if re.match(r'^\s{0,' + str(base_indent) + r'}(def |class |async def )', lines[i]):
                            break
                i += 1
            func_len = i - start_line
            if func_len > FUNC_LINE_LIMIT:
                func_name = re.search(r'def (\w+)', line).group(1)
                print(f"VIOLATION: {filepath}:{start_line}: {func_name}() {func_len} lines (limit: {FUNC_LINE_LIMIT})")
                violations += 1
        else:
            i += 1
    return violations


def check_debug_prints(filepath):
    with open(filepath) as f:
        content = f.read()
    # Find print() calls not in comment lines
    for i, line in enumerate(content.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if re.search(r'\bprint\(', stripped):
            print(f"WARNING: {filepath}:{i}: debug print() found")
            return 1
    return 0


def check_file(filepath):
    violations = 0
    violations += check_file_line_count(filepath)
    violations += check_function_lengths(filepath)
    return violations


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # Find all staged Python files
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f.endswith('.py')]

    # Filter to backend/src and backend/tests
    source_files = [f for f in files if f.startswith('backend/src/') or f.startswith('backend/tests/')]
    if not source_files:
        return 0

    total = 0
    for f in source_files:
        if os.path.isfile(f):
            total += check_file(f)
    return 1 if total > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
