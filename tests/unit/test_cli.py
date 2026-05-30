import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def cli_script():
    return Path(__file__).parent.parent.parent / "src" / "TheAntFarm" / "cli.py"


@pytest.fixture
def gerber_path():
    return Path(__file__).parent.parent / "test_data" / "gerbers"


def test_cli_generate_gerber_success(cli_script, gerber_path, tmp_path):
    gerber_file = gerber_path / "simple_square.gbr"
    result = subprocess.run(
        [sys.executable, str(cli_script), "generate", "gerber", "top", str(gerber_file), "-o", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "Done" in result.stdout
    gcode_files = list(tmp_path.glob("*.gcode"))
    assert len(gcode_files) > 0
    assert gcode_files[0].stat().st_size > 0


def test_cli_generate_drill_reports_error_gracefully(cli_script, gerber_path, tmp_path):
    drill_file = gerber_path / "simple_drill.drl"
    result = subprocess.run(
        [sys.executable, str(cli_script), "generate", "drill", "drill", str(drill_file), "-o", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "G-code generation failed" in result.stderr


def test_cli_generate_invalid_file_fails(cli_script, gerber_path, tmp_path):
    invalid_file = gerber_path / "invalid.gbr"
    result = subprocess.run(
        [sys.executable, str(cli_script), "generate", "gerber", "top", str(invalid_file), "-o", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_cli_generate_with_custom_params(cli_script, gerber_path, tmp_path):
    gerber_file = gerber_path / "metric_trace.gbr"
    result = subprocess.run(
        [
            sys.executable, str(cli_script), "generate", "gerber", "top", str(gerber_file),
            "-o", str(tmp_path), "--cut-depth", "-0.1", "--travel-height", "1.0",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "Done" in result.stdout


def test_cli_generate_with_mirror(cli_script, gerber_path, tmp_path):
    gerber_file = gerber_path / "simple_square.gbr"
    result = subprocess.run(
        [
            sys.executable, str(cli_script), "generate", "gerber", "top", str(gerber_file),
            "-o", str(tmp_path), "--mirror", "--mirror-axis", "y",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "Done" in result.stdout


def test_cli_help_succeeds(cli_script):
    result = subprocess.run(
        [sys.executable, str(cli_script), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout
