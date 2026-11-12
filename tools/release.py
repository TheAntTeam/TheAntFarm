"""Release helper of The Ant Farm, used by the "Prepare release" and "Release" workflows (see docs/releasing.md).

``version``  prints the version written in ``src/TheAntFarm/__init__.py``.
``prepare``  collects the "## Changelog" lines of the pull requests merged into ``dev`` since the last tag, moves them
             and the ``[Unreleased]`` entries into a new section of ``CHANGELOG.md`` and sets the new version in
             ``__init__.py`` and ``pyproject.toml``. It needs the GitHub CLI (``gh``), logged in.
``notes``    prints the release notes of a version: its section of ``CHANGELOG.md`` and the download notes.

Locally: ``python tools/release.py prepare --version 0.4.0 --dry-run`` prints the new section and changes no file.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from typing import Dict, List, Optional, Sequence, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INIT_PATH = "src/TheAntFarm/__init__.py"
PYPROJECT_PATH = "pyproject.toml"
CHANGELOG_PATH = "CHANGELOG.md"
DEFAULT_REPO = "TheAntTeam/TheAntFarm"
BASE_BRANCH = "dev"

CATEGORIES = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
INIT_VERSION_RE = re.compile(r'^__version__ = "([^"]*)"', re.MULTILINE)
PYPROJECT_VERSION_RE = re.compile(r'^version = "([^"]*)"', re.MULTILINE)
CATEGORY_HEADING_RE = re.compile(r"^(?:#+\s*|\*\*)?(" + "|".join(CATEGORIES) + r")(?:\*\*)?:?\s*$", re.IGNORECASE)
CHANGELOG_HEADING_RE = re.compile(r"^##\s+Changelog\s*$", re.IGNORECASE)
BULLET_RE = re.compile(r"^[-*]\s+\S")
UNRELEASED_RE = re.compile(r"^## \[Unreleased\][^\n]*\n", re.MULTILINE)
SECTION_RE = re.compile(r"^## ", re.MULTILINE)

MACOS_NOTE = (
    "The executables are not signed. On macOS, if the system refuses to open `the_ant_farm`, choose "
    "**Open Anyway** in System Settings > Privacy & Security, or run `xattr -d com.apple.quarantine the_ant_farm`."
)

Entries = Dict[str, List[str]]


def read_text(relative: str) -> Tuple[str, str]:
    """Return the text of a repository file with ``\\n`` line ends, and its original line end."""
    with open(os.path.join(REPO_ROOT, relative), "r", encoding="utf-8", newline="") as f:
        raw = f.read()
    newline = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), newline


def write_text(relative: str, text: str, newline: str) -> None:
    with open(os.path.join(REPO_ROOT, relative), "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", newline))


def parse_version(version: str) -> Tuple[int, int, int]:
    if not VERSION_RE.match(version):
        raise ValueError(f"Not a version (major.minor.patch): {version!r}")
    major, minor, patch = (int(part) for part in version.split("."))
    return major, minor, patch


def code_version(init_text: str) -> str:
    match = INIT_VERSION_RE.search(init_text)
    if not match:
        raise ValueError(f"No __version__ in {INIT_PATH}")
    return match.group(1)


def pyproject_version(pyproject_text: str) -> str:
    match = PYPROJECT_VERSION_RE.search(pyproject_text)
    if not match:
        raise ValueError(f"No version in {PYPROJECT_PATH}")
    return match.group(1)


def set_code_version(init_text: str, version: str) -> str:
    return INIT_VERSION_RE.sub(f'__version__ = "{version}"', init_text, count=1)


def set_pyproject_version(pyproject_text: str, version: str) -> str:
    return PYPROJECT_VERSION_RE.sub(f'version = "{version}"', pyproject_text, count=1)


def category_for_branch(branch: str) -> str:
    """The category of a changelog line written without a category heading, from the branch prefix."""
    prefix = branch.split("/", 1)[0].lower() if "/" in branch else ""
    if prefix in ("feature", "feat"):
        return "Added"
    if prefix in ("bugfix", "fix", "hotfix"):
        return "Fixed"
    return "Changed"


def changelog_section(body: str) -> List[str]:
    """The lines of the "## Changelog" section of a pull request description, up to the next heading."""
    section: List[str] = []
    inside = False
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        if CHANGELOG_HEADING_RE.match(line.strip()):
            inside = True
        elif inside and re.match(r"^#{1,2}\s", line):
            break
        elif inside:
            section.append(line)
    return section


def _collect_bullets(lines: Sequence[str], category: Optional[str], heading_re: "re.Pattern[str]") -> Entries:
    """Bullets by category: a heading line sets the category, indented lines continue the bullet above them."""
    entries: Entries = {}
    current: Optional[List[str]] = None
    for line in lines:
        heading = heading_re.match(line.strip())
        if heading:
            category = heading.group(1).strip("* ").capitalize()
            current = None
        elif category and BULLET_RE.match(line):
            current = [line.rstrip()]
            entries.setdefault(category, []).append(current[0])
        elif category and current is not None and line.strip() and line[:1] in (" ", "\t"):
            current.append(line.rstrip())
            entries[category][-1] = "\n".join(current)
        elif line.strip():
            current = None
    return entries


def parse_changelog_lines(body: str, branch: str) -> Entries:
    """The changelog entries of a pull request, by category.

    A category heading (``**Fixed**``, ``### Fixed`` or ``Fixed:``) applies to the bullets below it; bullets before
    any heading take the category of the branch prefix. Any text that is not a bullet (such as "None: development
    tooling only.") is left out.
    """
    return _collect_bullets(changelog_section(body), category_for_branch(branch), CATEGORY_HEADING_RE)


def parse_entries(block: str) -> Entries:
    """The entries of a section of CHANGELOG.md, under its ``### Category`` headings."""
    return _collect_bullets(block.split("\n"), None, re.compile(r"^###\s+(.+?)\s*$"))


def merge_entries(*groups: Entries) -> Entries:
    """Join entries by category, in order, leaving out an entry already listed."""
    merged: Entries = {}
    seen = set()
    for group in groups:
        for category, items in group.items():
            for item in items:
                key = " ".join(item.split())
                if key not in seen:
                    seen.add(key)
                    merged.setdefault(category, []).append(item)
    return merged


def format_entries(entries: Entries) -> str:
    order = [c for c in CATEGORIES if c in entries] + [c for c in entries if c not in CATEGORIES]
    return "\n".join(f"### {category}\n\n" + "\n".join(entries[category]) + "\n" for category in order)


def split_unreleased(changelog: str) -> Tuple[str, str, str]:
    """Split the changelog into the text up to the ``[Unreleased]`` heading included, its entries and the rest."""
    match = UNRELEASED_RE.search(changelog)
    if not match:
        raise ValueError(f"No '## [Unreleased]' section in {CHANGELOG_PATH}")
    following = SECTION_RE.search(changelog, match.end())
    end = following.start() if following else len(changelog)
    return changelog[: match.end()], changelog[match.end() : end], changelog[end:]


def format_date(day: date) -> str:
    return day.strftime("%b %d, %Y")


def release_changelog(changelog: str, version: str, day: date, collected: Entries) -> str:
    """Move the ``[Unreleased]`` entries and the collected ones into a new ``[version]`` section."""
    if re.search(rf"^## \[{re.escape(version)}\]", changelog, re.MULTILINE):
        raise ValueError(f"{CHANGELOG_PATH} already has a section for {version}")
    head, unreleased, rest = split_unreleased(changelog)
    entries = merge_entries(parse_entries(unreleased), collected)
    if not entries:
        raise ValueError("Nothing to release: no entry under [Unreleased] and no changelog line in the pull requests")
    section = f"## [{version}] - {format_date(day)}\n\n{format_entries(entries)}\n\n"
    return head + "\n" + section + rest


def version_section(changelog: str, version: str) -> str:
    """The section of a version in the changelog, heading included."""
    match = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n", changelog, re.MULTILINE)
    if not match:
        raise ValueError(f"No section for {version} in {CHANGELOG_PATH}")
    following = SECTION_RE.search(changelog, match.end())
    return changelog[match.start() : following.start() if following else len(changelog)].rstrip() + "\n"


def release_notes(changelog: str, version: str, repo: str = DEFAULT_REPO, previous_tag: str = "") -> str:
    """The notes of a release: its changelog section without the heading, the macOS note and the compare link."""
    body = version_section(changelog, version).split("\n", 1)[1].strip()
    notes = [body, "### Downloads", MACOS_NOTE]
    if previous_tag:
        notes.append(f"**Full Changelog**: https://github.com/{repo}/compare/{previous_tag}...v{version}")
    return "\n\n".join(notes) + "\n"


def run(args: Sequence[str]) -> str:
    return subprocess.run(list(args), cwd=REPO_ROOT, check=True, capture_output=True, text=True).stdout.strip()


def merged_at(pull: dict) -> datetime:
    return datetime.fromisoformat(pull["mergedAt"].replace("Z", "+00:00"))


def merged_pull_requests(repo: str, since: datetime) -> List[dict]:
    """The pull requests merged into the base branch after ``since``, oldest first."""
    fields = "number,headRefName,body,mergedAt"
    output = run(
        ["gh", "pr", "list", "--repo", repo, "--base", BASE_BRANCH, "--state", "merged", "--limit", "1000"]
        + ["--json", fields]
    )
    pulls = [pr for pr in json.loads(output or "[]") if merged_at(pr) > since]
    return sorted(pulls, key=merged_at)


def collect_entries(pulls: Sequence[dict]) -> Entries:
    return merge_entries(*(parse_changelog_lines(pr.get("body") or "", pr.get("headRefName") or "") for pr in pulls))


def prepare(version: str, repo: str, since_tag: str, day: date, dry_run: bool) -> str:
    """Write the release section and the new version; return a summary (and the section, on a dry run)."""
    init_text, init_newline = read_text(INIT_PATH)
    current = code_version(init_text)
    if parse_version(version) <= parse_version(current):
        raise ValueError(f"The new version {version} is not greater than the current one, {current}")
    tag = since_tag or run(["git", "describe", "--tags", "--abbrev=0", "--match", "v*", "HEAD"])
    since = datetime.fromtimestamp(int(run(["git", "log", "-1", "--format=%ct", tag])), timezone.utc)
    pulls = merged_pull_requests(repo, since)
    changelog, changelog_newline = read_text(CHANGELOG_PATH)
    new_changelog = release_changelog(changelog, version, day, collect_entries(pulls))
    numbers = ", ".join(f"#{pr['number']}" for pr in pulls) or "none"
    summary = f"{len(pulls)} pull requests merged into {BASE_BRANCH} since {tag}: {numbers}"
    if dry_run:
        return summary + "\n\n" + version_section(new_changelog, version)
    pyproject_text, pyproject_newline = read_text(PYPROJECT_PATH)
    write_text(CHANGELOG_PATH, new_changelog, changelog_newline)
    write_text(INIT_PATH, set_code_version(init_text, version), init_newline)
    write_text(PYPROJECT_PATH, set_pyproject_version(pyproject_text, version), pyproject_newline)
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("version", help="print the version of the code")
    prepare_cmd = commands.add_parser("prepare", help="write the changelog section and the version of a release")
    prepare_cmd.add_argument("--version", required=True)
    prepare_cmd.add_argument("--repo", default=DEFAULT_REPO)
    prepare_cmd.add_argument("--since-tag", default="", help="default: the last v* tag reachable from HEAD")
    prepare_cmd.add_argument("--date", default="", help="release date, YYYY-MM-DD (default: today)")
    prepare_cmd.add_argument("--dry-run", action="store_true", help="print the new section, change no file")
    notes_cmd = commands.add_parser("notes", help="print the release notes of a version")
    notes_cmd.add_argument("--version", required=True)
    notes_cmd.add_argument("--repo", default=DEFAULT_REPO)
    notes_cmd.add_argument("--previous-tag", default="")
    args = parser.parse_args(argv)
    try:
        if args.command == "version":
            print(code_version(read_text(INIT_PATH)[0]))
        elif args.command == "prepare":
            day = date.fromisoformat(args.date) if args.date else date.today()
            print(prepare(args.version, args.repo, args.since_tag, day, args.dry_run))
        else:
            print(release_notes(read_text(CHANGELOG_PATH)[0], args.version, args.repo, args.previous_tag), end="")
    except (ValueError, subprocess.CalledProcessError) as error:
        detail = (getattr(error, "stderr", "") or "").strip()
        print(f"error: {error}" + (f": {detail}" if detail else ""), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
