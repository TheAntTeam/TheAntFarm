"""On Windows, config_os adds the folder of the PySide6 module to the DLL search path."""

import logging
import os
import sys
from unittest.mock import patch

import pytest

from TheAntFarm import the_ant_farm


@pytest.fixture
def windows():
    with (
        patch.dict(os.environ),
        patch.object(the_ant_farm.platform, "system", return_value="Windows"),
        patch.object(the_ant_farm.os, "add_dll_directory", create=True) as add_dll_directory,
    ):
        yield add_dll_directory


class TestConfigOsOnWindows:
    def test_the_folder_of_the_pyside6_module_is_added(self, windows):
        the_ant_farm.config_os()

        windows.assert_called_once_with(os.path.dirname(sys.modules["PySide6"].__file__))

    def test_the_folder_is_found_in_the_executable(self, windows, tmp_path, caplog):
        bundled = tmp_path / "_internal" / "PySide6"
        bundled.mkdir(parents=True)
        with patch.object(sys.modules["PySide6"], "__file__", str(bundled / "__init__.pyc")):
            with caplog.at_level(logging.ERROR):
                the_ant_farm.config_os()

        windows.assert_called_once_with(str(bundled))
        assert not caplog.records
