"""The PyInstaller spec copies the application's own modules through its ``datas`` list.

PyInstaller does not collect them from the imports, so a module missing from the list builds an
executable that stops at startup with ModuleNotFoundError.
"""

import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest

APP_DIR = Path(__file__).resolve().parents[2] / "src" / "TheAntFarm"
SPEC = APP_DIR / "the_ant_farm.spec"
ENTRY = APP_DIR / "the_ant_farm.py"


def _analysis_keywords() -> Dict[str, ast.expr]:
    for node in ast.walk(ast.parse(SPEC.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "Analysis":
            return {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg}
    raise AssertionError("no Analysis call in the spec")


def _datas() -> List[Tuple[str, str]]:
    return [tuple(entry) for entry in ast.literal_eval(_analysis_keywords()["datas"])]


def _local_name(name: str) -> str:
    """The top-level module or package of the application that ``name`` belongs to, or ''."""
    top = name.split(".")[0]
    if (APP_DIR / f"{top}.py").is_file() or (APP_DIR / top).is_dir():
        return top
    return ""


def _imported_names(path: Path) -> Set[str]:
    names = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module)
    return names


def _local_modules_of_the_app() -> Set[str]:
    """The application's own top-level modules and packages reached from its entry point."""
    found: Set[str] = set()
    to_visit = [ENTRY]
    visited: Set[Path] = set()
    while to_visit:
        path = to_visit.pop()
        if path in visited:
            continue
        visited.add(path)
        for name in _imported_names(path):
            top = _local_name(name)
            if not top or top in found:
                continue
            found.add(top)
            if (APP_DIR / f"{top}.py").is_file():
                to_visit.append(APP_DIR / f"{top}.py")
            else:
                to_visit.extend(sorted((APP_DIR / top).rglob("*.py")))
    return found


def test_every_data_source_exists():
    missing = [source for source, _ in _datas() if not (APP_DIR / source).exists()]

    assert missing == []


def test_every_module_of_the_app_is_bundled():
    bundled = {Path(source).stem if source.endswith(".py") else source for source, _ in _datas()}

    missing = sorted(_local_modules_of_the_app() - bundled)

    assert missing == [], f"add these to the datas list of {SPEC.name}: {missing}"


@pytest.mark.parametrize("module", ["ui_the_ant_farm", "combobox_elide_left", "controller", "ui_manager"])
def test_the_import_walk_finds_the_modules_of_the_window(module):
    assert module in _local_modules_of_the_app()
