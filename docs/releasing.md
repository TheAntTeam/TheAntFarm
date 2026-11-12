# Releasing

A release goes from `dev` to `main` and gets a tag; two workflows do the repetitive work.

## Where the pieces live

- **Version**: `src/TheAntFarm/__init__.py` (`__version__`). `pyproject.toml` repeats it; a test
  (`tests/unit/test_release_tool.py`) fails if the two differ. The About dialog shows it.
- **Changelog lines**: each pull request writes its own under a `## Changelog` heading in its description,
  never in `CHANGELOG.md`. Lines can be grouped under `**Added**`, `**Changed**`, `**Fixed**` (or `### Fixed`,
  `Fixed:`); lines without a heading take the category of the branch: `feature/` → Added, `bugfix/` and `fix/` →
  Fixed, anything else → Changed. Text that is not a bullet, such as "None: development tooling only.", is left out.
- **Helper**: `tools/release.py`, used by both workflows; it also runs locally (it needs `gh` logged in).

## Steps

1. **Prepare.** On the Actions page, run **Prepare release** with the new version (for example `0.4.0`).
   It collects the changelog lines of the pull requests merged into `dev` since the last tag, moves them and
   the `[Unreleased]` entries of `CHANGELOG.md` into a new `## [0.4.0] - date` section, sets the version and
   opens a pull request `release/v0.4.0` → `dev`.

   To see the section first without changing anything:

   ```bash
   python tools/release.py prepare --version 0.4.0 --dry-run
   ```

2. **Review and merge into dev.** Edit the wording and the categories of the new section in the pull request,
   then merge it as usual. The tests run on `dev` after the merge (a pull request opened by a workflow does not
   start them).

3. **Merge dev into main.** Open a pull request `dev` → `main` and merge it with **Create a merge commit**:
   a rebase or a squash would copy the commits of `dev` onto `main` with new hashes, and the two branches would
   no longer share their history.

4. **Tag main.** Once the tests pass on `main`:

   ```bash
   git fetch origin
   ```

   ```bash
   git tag v0.4.0 origin/main
   ```

   ```bash
   git push origin v0.4.0
   ```

   The **Release** workflow checks that the tag matches the version of the code and is on `main`, builds the
   executables on Linux, Windows and macOS and creates a **draft** release with:
   - `the_ant_farm-0.4.0-windows.zip`, `the_ant_farm-0.4.0-macos.zip`, `the_ant_farm-0.4.0-linux.tar.gz`;
   - `SHA256SUMS`;
   - the `CHANGELOG.md` section of the version as notes, a note on the unsigned executables and the link to the
     changes since the previous tag.

5. **Publish.** Open the draft on the Releases page, read it, try the executables and publish it.

If the Release workflow fails, fix the cause on `dev`, merge into `main` again, then move the tag:

```bash
git push origin :refs/tags/v0.4.0
```

```bash
git tag -f v0.4.0 origin/main
```

```bash
git push origin v0.4.0
```

## Not covered

The executables are not signed: Windows SmartScreen and macOS Gatekeeper warn the first time they are opened.
Signing needs a code signing certificate (Windows) and an Apple Developer account (macOS notarization).
