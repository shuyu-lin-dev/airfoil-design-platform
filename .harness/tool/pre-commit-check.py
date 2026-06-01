#!/usr/bin/env python3
"""Pre-commit checks: file line limit (200), function length limit (50), allowed_paths gate.

Usage: python .harness/tool/pre-commit-check.py [file ...]
Exit 0 on pass, 1 on violation.
"""

import sys
import re
import os
from fnmatch import fnmatch
from pathlib import PurePosixPath


FILE_LINE_LIMIT = 200
FUNC_LINE_LIMIT = 50

# Files always allowed regardless of task allowed_paths.
ALWAYS_ALLOW = {
    'PROGRESS.md', 'tasks/tasks.yaml', 'DECISIONS.md', 'CONTEXT.md',
    '.claude/settings.json', '.gitignore', '.pre-commit-config.yaml',
    '.harness/state/runs/telemetry.yaml',
}
ALWAYS_ALLOW_PREFIXES = (
    '.harness/state/runs/', 'docs/adr/', 'docs/spec.md',
    'docs/api-contracts.md', 'docs/backend-mvp-full-spec.md',
)


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
            while i < len(lines):
                stripped = lines[i].rstrip()
                if stripped and not stripped.startswith(' ' * (base_indent + 1)) and not stripped.startswith('\t') and not stripped.startswith(' ' * base_indent + ' ') and not stripped.startswith('#'):
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


def check_file(filepath):
    violations = 0
    violations += check_file_line_count(filepath)
    violations += check_function_lengths(filepath)
    return violations


# ---------------------------------------------------------------------------
# allowed_paths gate
# ---------------------------------------------------------------------------

def _parse_active_task_allowed_paths(tasks_path='tasks/tasks.yaml'):
    """Parse tasks/tasks.yaml to find the active task's allowed_paths.

    Returns (task_id, allowed_paths) or (None, []) if no active task found.
    Uses a lightweight state machine – no PyYAML dependency.
    """
    if not os.path.isfile(tasks_path):
        return None, []

    with open(tasks_path) as f:
        lines = f.readlines()

    current_task_id = None
    in_active = False
    in_allowed = False
    allowed = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('- id: '):
            # New task block – reset
            if in_active:
                return current_task_id, allowed
            current_task_id = stripped.split('- id: ', 1)[1].strip()
            in_active = False
            in_allowed = False
            allowed = []

        if in_active:
            if stripped == 'allowed_paths:':
                in_allowed = True
            elif in_allowed and stripped.startswith('- '):
                allowed.append(stripped[2:].strip())
            elif in_allowed and not stripped.startswith('- ') and not stripped.startswith('#'):
                in_allowed = False
        elif current_task_id is not None and stripped == 'status: active':
            in_active = True

    if in_active:
        return current_task_id, allowed
    return None, []


def _match_allowed(filepath, allowed_patterns):
    """Check if filepath matches any allowed_paths pattern (supports ** globs)."""
    pp = PurePosixPath(filepath)
    for pat in allowed_patterns:
        if pp.match(pat) or fnmatch(filepath, pat):
            return True
    return False


def check_allowed_paths(staged_files, tasks_path='tasks/tasks.yaml'):
    task_id, allowed = _parse_active_task_allowed_paths(tasks_path)
    if task_id is None:
        return 0  # no active task – allow all

    violations = 0
    for f in staged_files:
        if f in ALWAYS_ALLOW:
            continue
        if any(f.startswith(p) for p in ALWAYS_ALLOW_PREFIXES):
            continue
        if _match_allowed(f, allowed):
            continue
        print(f"VIOLATION: {f} not in {task_id} allowed_paths")
        violations += 1

    return violations


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f]

    if not files:
        return 0

    # Run allowed_paths check on all staged files (not just .py)
    total = check_allowed_paths(files)

    # Run line/function checks only on source Python files
    source_files = [f for f in files if f.startswith('backend/src/') or f.startswith('backend/tests/')]
    source_files = [f for f in source_files if f.endswith('.py') and os.path.isfile(f)]

    for f in source_files:
        total += check_file(f)
    return 1 if total > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
