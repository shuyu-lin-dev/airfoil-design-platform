import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("pre-commit-check.py")
SPEC = importlib.util.spec_from_file_location("pre_commit_check", MODULE_PATH)
pre_commit_check = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(pre_commit_check)


def write_tasks(tmp_path, content):
    tasks_path = tmp_path / "tasks.yaml"
    tasks_path.write_text(content, encoding="utf-8")
    return str(tasks_path)


def test_parse_active_task_allowed_paths(tmp_path):
    tasks_path = write_tasks(
        tmp_path,
        """
tasks:
  - id: T003
    status: passing
    allowed_paths:
      - backend/old/**
  - id: T004
    status: active
    allowed_paths:
      - backend/src/airfoil_platform/artifacts/**
      - .harness/state/sprint-contracts/T004-*.md
  - id: T005
    status: not_started
""",
    )

    task_id, allowed = pre_commit_check._parse_active_task_allowed_paths(tasks_path)

    assert task_id == "T004"
    assert allowed == [
        "backend/src/airfoil_platform/artifacts/**",
        ".harness/state/sprint-contracts/T004-*.md",
    ]


def test_match_allowed_supports_globs():
    assert pre_commit_check._match_allowed(
        "backend/src/airfoil_platform/artifacts/hdf5_store.py",
        ["backend/src/airfoil_platform/artifacts/**"],
    )
    assert pre_commit_check._match_allowed(
        ".harness/state/sprint-contracts/T004-artifact-store.md",
        [".harness/state/sprint-contracts/T004-*.md"],
    )
    assert not pre_commit_check._match_allowed(
        "backend/tests/test_hdf5_store.py",
        ["backend/src/airfoil_platform/artifacts/**"],
    )


def test_allowed_paths_honors_workflow_whitelist(tmp_path):
    tasks_path = write_tasks(
        tmp_path,
        """
tasks:
  - id: T004
    status: active
    allowed_paths:
      - backend/src/airfoil_platform/artifacts/**
""",
    )

    assert pre_commit_check.check_allowed_paths(
        ["PROGRESS.md", ".harness/state/runs/telemetry.yaml"],
        tasks_path,
    ) == 0


def test_allowed_paths_blocks_files_outside_active_task(tmp_path, capsys):
    tasks_path = write_tasks(
        tmp_path,
        """
tasks:
  - id: T004
    status: active
    allowed_paths:
      - backend/src/airfoil_platform/artifacts/**
""",
    )

    violations = pre_commit_check.check_allowed_paths(
        ["backend/tests/test_hdf5_store.py"],
        tasks_path,
    )

    assert violations == 1
    assert "VIOLATION: backend/tests/test_hdf5_store.py not in T004" in capsys.readouterr().out


def test_allowed_paths_allows_all_when_no_active_task(tmp_path):
    tasks_path = write_tasks(
        tmp_path,
        """
tasks:
  - id: T004
    status: not_started
""",
    )

    assert pre_commit_check.check_allowed_paths(["any/path.txt"], tasks_path) == 0
