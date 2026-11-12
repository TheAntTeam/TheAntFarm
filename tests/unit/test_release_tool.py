"""Tests of tools/release.py, the helper of the "Prepare release" and "Release" workflows, and of the version."""

import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("release_tool", REPO_ROOT / "tools" / "release.py")
release = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release)

CHANGELOG = """# Change Log
Intro.


## [Unreleased]

### Added

- Feature already listed.

### Fixed

- Fix already listed.


## [0.3.2] - Jan 10, 2026

### Fixed

- Old fix.
"""

PR_BODY = """Fixes #1

## Problem

Text.

## Changelog

**Fixed**

- A fix (#1): first line
  continued on a second line.

**Added**

- A feature.

## Notes

- Not a changelog line.
"""


class TestVersion:
    def test_versions_of_the_code_agree(self) -> None:
        from settings_manager.settings_app import AppSettingsHandler

        init_version = release.code_version(release.read_text(release.INIT_PATH)[0])
        assert release.pyproject_version(release.read_text(release.PYPROJECT_PATH)[0]) == init_version
        assert AppSettingsHandler.APP_VERSION_DEFAULT == init_version
        release.parse_version(init_version)

    def test_set_versions(self) -> None:
        assert release.set_code_version('__version__ = "0.3.2"\n', "0.4.0") == '__version__ = "0.4.0"\n'
        pyproject = '[tool.poetry]\nversion = "0.3.2"\n[x]\nversion = "9"\n'
        expected = '[tool.poetry]\nversion = "0.4.0"\n[x]\nversion = "9"\n'
        assert release.set_pyproject_version(pyproject, "0.4.0") == expected

    @pytest.mark.parametrize("text", ["", "version = 1"])
    def test_missing_version(self, text: str) -> None:
        with pytest.raises(ValueError):
            release.code_version(text)
        with pytest.raises(ValueError):
            release.pyproject_version(text)

    @pytest.mark.parametrize("version", ["0.4", "v0.4.0", "0.4.0-rc1", ""])
    def test_parse_version_refuses(self, version: str) -> None:
        with pytest.raises(ValueError):
            release.parse_version(version)

    def test_parse_version_compares_numbers(self) -> None:
        assert release.parse_version("0.10.0") > release.parse_version("0.9.9")


class TestPullRequestLines:
    @pytest.mark.parametrize(
        "branch, category",
        [
            ("feature/x", "Added"),
            ("feat/x", "Added"),
            ("bugfix/x", "Fixed"),
            ("fix/x", "Fixed"),
            ("hotfix/x", "Fixed"),
            ("chore/x", "Changed"),
            ("ci/x", "Changed"),
            ("main", "Changed"),
        ],
    )
    def test_category_for_branch(self, branch: str, category: str) -> None:
        assert release.category_for_branch(branch) == category

    def test_headings_continuations_and_end_of_section(self) -> None:
        entries = release.parse_changelog_lines(PR_BODY, "chore/x")
        assert entries == {
            "Fixed": ["- A fix (#1): first line\n  continued on a second line."],
            "Added": ["- A feature."],
        }

    def test_lines_without_heading_take_the_branch_category(self) -> None:
        body = "## Changelog\r\n\r\n- One fix.\r\n- Another fix.\r\n"
        assert release.parse_changelog_lines(body, "bugfix/x") == {"Fixed": ["- One fix.", "- Another fix."]}

    @pytest.mark.parametrize("heading", ["### Changed", "Changed:", "**changed**"])
    def test_heading_forms(self, heading: str) -> None:
        body = f"## Changelog\n\n{heading}\n\n- A change.\n"
        assert release.parse_changelog_lines(body, "feature/x") == {"Changed": ["- A change."]}

    @pytest.mark.parametrize(
        "body", ["## Changelog\n\nNone: development tooling only.\n", "No changelog section.", "", None]
    )
    def test_no_lines(self, body: str) -> None:
        assert release.parse_changelog_lines(body, "feature/x") == {}

    def test_text_after_a_bullet_ends_it(self) -> None:
        body = "## Changelog\n\n- A fix.\nPlain text.\n  indented, not a continuation\n"
        assert release.parse_changelog_lines(body, "fix/x") == {"Fixed": ["- A fix."]}

    def test_collect_keeps_order_and_drops_duplicates(self) -> None:
        pulls = [
            {"body": "## Changelog\n\n- First.\n", "headRefName": "fix/a"},
            {"body": "## Changelog\n\n- Second.\n-   First.\n", "headRefName": "fix/b"},
            {"body": None, "headRefName": None},
        ]
        assert release.collect_entries(pulls) == {"Fixed": ["- First.", "- Second."]}


class TestChangelog:
    def test_release_moves_unreleased_and_collected_entries(self) -> None:
        collected = {"Fixed": ["- New fix."], "Changed": ["- New change."], "Other": ["- Odd."]}
        result = release.release_changelog(CHANGELOG, "0.4.0", date(2026, 11, 12), collected)
        assert result.startswith("# Change Log\nIntro.\n\n\n## [Unreleased]\n\n## [0.4.0] - Nov 12, 2026\n\n")
        section = release.version_section(result, "0.4.0")
        assert section == (
            "## [0.4.0] - Nov 12, 2026\n\n"
            "### Added\n\n- Feature already listed.\n\n"
            "### Changed\n\n- New change.\n\n"
            "### Fixed\n\n- Fix already listed.\n- New fix.\n\n"
            "### Other\n\n- Odd.\n"
        )
        assert result.endswith("\n\n\n## [0.3.2] - Jan 10, 2026\n\n### Fixed\n\n- Old fix.\n")
        assert release.split_unreleased(result)[1] == "\n"

    def test_release_drops_a_line_already_under_unreleased(self) -> None:
        result = release.release_changelog(CHANGELOG, "0.4.0", date(2026, 1, 2), {"Fixed": ["- Fix  already listed."]})
        assert release.version_section(result, "0.4.0").count("already listed") == 2

    def test_release_refuses_an_existing_version(self) -> None:
        with pytest.raises(ValueError, match="already has"):
            release.release_changelog(CHANGELOG, "0.3.2", date(2026, 1, 2), {})

    def test_release_refuses_nothing_to_release(self) -> None:
        empty = "# Change Log\n\n## [Unreleased]\n\n## [0.3.2] - Jan 10, 2026\n"
        with pytest.raises(ValueError, match="Nothing to release"):
            release.release_changelog(empty, "0.4.0", date(2026, 1, 2), {})

    def test_release_needs_an_unreleased_section(self) -> None:
        with pytest.raises(ValueError, match="Unreleased"):
            release.release_changelog("# Change Log\n", "0.4.0", date(2026, 1, 2), {"Fixed": ["- x"]})

    def test_last_section(self) -> None:
        assert release.version_section(CHANGELOG, "0.3.2") == "## [0.3.2] - Jan 10, 2026\n\n### Fixed\n\n- Old fix.\n"

    def test_notes(self) -> None:
        notes = release.release_notes(CHANGELOG, "0.3.2", "owner/repo", "v0.3.1")
        assert notes.startswith("### Fixed\n\n- Old fix.\n\n### Downloads\n\n")
        assert release.MACOS_NOTE in notes
        assert notes.endswith("**Full Changelog**: https://github.com/owner/repo/compare/v0.3.1...v0.3.2\n")

    def test_notes_without_previous_tag(self) -> None:
        assert "Full Changelog" not in release.release_notes(CHANGELOG, "0.3.2")

    def test_notes_of_a_missing_version(self) -> None:
        with pytest.raises(ValueError, match="No section"):
            release.release_notes(CHANGELOG, "9.9.9")

    def test_the_real_changelog_has_an_unreleased_section(self) -> None:
        release.split_unreleased(release.read_text(release.CHANGELOG_PATH)[0])


@pytest.fixture
def run_calls() -> list:
    return []


@pytest.fixture
def fake_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, run_calls: list) -> Path:
    """A copy of the release files in a temporary folder, with git and gh replaced."""
    (tmp_path / "src" / "TheAntFarm").mkdir(parents=True)
    (tmp_path / "src" / "TheAntFarm" / "__init__.py").write_bytes(b'__version__ = "0.3.2"\r\n')
    (tmp_path / "pyproject.toml").write_bytes(b'[tool.poetry]\nname = "x"\nversion = "0.3.2"\n')
    (tmp_path / "CHANGELOG.md").write_bytes(CHANGELOG.replace("\n", "\r\n").encode())
    monkeypatch.setattr(release, "REPO_ROOT", str(tmp_path))
    pulls = [
        {"number": 3, "headRefName": "bugfix/c", "mergedAt": "2026-03-01T00:00:00Z", "body": "## Changelog\n\n- C."},
        {"number": 2, "headRefName": "feature/b", "mergedAt": "2026-02-01T00:00:00Z", "body": "## Changelog\n\n- B."},
        {"number": 1, "headRefName": "bugfix/a", "mergedAt": "2026-01-01T00:00:00Z", "body": "## Changelog\n\n- A."},
    ]

    def fake_run(args):
        run_calls.append(list(args))
        if args[:2] == ["git", "describe"]:
            return "v0.3.2"
        if args[:2] == ["git", "log"]:
            return "1768003200"  # 2026-01-10T00:00:00Z
        if args[:2] == ["gh", "pr"]:
            return json.dumps(pulls)
        raise AssertionError(args)

    monkeypatch.setattr(release, "run", fake_run)
    return tmp_path


class TestPrepare:
    def test_dry_run_changes_nothing(self, fake_repo: Path, run_calls: list) -> None:
        before = (fake_repo / "CHANGELOG.md").read_bytes()
        output = release.prepare("0.4.0", "owner/repo", "", date(2026, 11, 12), dry_run=True)
        assert output.startswith("2 pull requests merged into dev since v0.3.2: #2, #3\n\n## [0.4.0] - Nov 12, 2026")
        assert "- B." in output and "- C." in output and "- A." not in output
        assert (fake_repo / "CHANGELOG.md").read_bytes() == before
        assert run_calls[2][:5] == ["gh", "pr", "list", "--repo", "owner/repo"]

    def test_writes_changelog_and_versions_keeping_line_ends(self, fake_repo: Path, run_calls: list) -> None:
        output = release.prepare("0.4.0", "owner/repo", "v0.3.1", date(2026, 11, 12), dry_run=False)
        assert output == "2 pull requests merged into dev since v0.3.1: #2, #3"
        assert not any(call[:2] == ["git", "describe"] for call in run_calls)
        assert (fake_repo / "src" / "TheAntFarm" / "__init__.py").read_bytes() == b'__version__ = "0.4.0"\r\n'
        assert b'version = "0.4.0"\n' in (fake_repo / "pyproject.toml").read_bytes()
        changelog = (fake_repo / "CHANGELOG.md").read_bytes()
        assert b"\n" not in changelog.replace(b"\r\n", b"")
        assert b"## [0.4.0] - Nov 12, 2026\r\n\r\n### Added\r\n\r\n- Feature already listed.\r\n- B.\r\n" in changelog

    @pytest.mark.parametrize("version", ["0.3.2", "0.3.1"])
    def test_refuses_a_version_not_greater(self, fake_repo: Path, version: str) -> None:
        with pytest.raises(ValueError, match="not greater"):
            release.prepare(version, "owner/repo", "", date(2026, 11, 12), dry_run=False)

    def test_no_pull_request(self, fake_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(release, "merged_pull_requests", lambda repo, since: [])
        output = release.prepare("0.4.0", "owner/repo", "", date(2026, 11, 12), dry_run=True)
        assert output.startswith("0 pull requests merged into dev since v0.3.2: none")


class TestMain:
    def test_version(self, fake_repo: Path, capsys: pytest.CaptureFixture) -> None:
        assert release.main(["version"]) == 0
        assert capsys.readouterr().out == "0.3.2\n"

    def test_notes(self, fake_repo: Path, capsys: pytest.CaptureFixture) -> None:
        assert release.main(["notes", "--version", "0.3.2", "--previous-tag", "v0.3.1"]) == 0
        assert capsys.readouterr().out.startswith("### Fixed\n\n- Old fix.\n")

    def test_prepare(self, fake_repo: Path, capsys: pytest.CaptureFixture) -> None:
        assert release.main(["prepare", "--version", "0.4.0", "--date", "2026-11-12", "--dry-run"]) == 0
        assert "## [0.4.0] - Nov 12, 2026" in capsys.readouterr().out

    def test_error(self, fake_repo: Path, capsys: pytest.CaptureFixture) -> None:
        assert release.main(["notes", "--version", "9.9.9"]) == 1
        assert capsys.readouterr().err.startswith("error: No section for 9.9.9")

    def test_command_error_shows_its_output(
        self, fake_repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
    ) -> None:
        def failing_run(args):
            raise subprocess.CalledProcessError(1, args, stderr="fatal: No names found\n")

        monkeypatch.setattr(release, "run", failing_run)
        assert release.main(["prepare", "--version", "0.4.0"]) == 1
        assert capsys.readouterr().err.rstrip().endswith(": fatal: No names found")


def test_run_returns_the_output() -> None:
    assert release.run(["git", "--version"]).startswith("git version")


def test_merged_pull_requests_filters_and_sorts(monkeypatch: pytest.MonkeyPatch) -> None:
    pulls = [
        {"number": 2, "mergedAt": "2026-02-01T00:00:00Z"},
        {"number": 1, "mergedAt": "2025-12-01T00:00:00Z"},
        {"number": 3, "mergedAt": "2026-01-15T00:00:00Z"},
    ]
    monkeypatch.setattr(release, "run", lambda args: json.dumps(pulls))
    result = release.merged_pull_requests("owner/repo", datetime(2026, 1, 1, tzinfo=timezone.utc))
    assert [pr["number"] for pr in result] == [3, 2]


def test_script_runs(tmp_path: Path) -> None:
    script = tmp_path / "tools" / "release.py"
    script.parent.mkdir()
    shutil.copy(REPO_ROOT / "tools" / "release.py", script)
    (tmp_path / "src" / "TheAntFarm").mkdir(parents=True)
    (tmp_path / "src" / "TheAntFarm" / "__init__.py").write_text('__version__ = "1.2.3"\n')
    result = subprocess.run([sys.executable, str(script), "version"], capture_output=True, text=True)
    assert result.stdout == "1.2.3\n"
