"""config_os leaves the Qt plugin folders to Qt, which finds the plugins of PySide6 by itself."""

import os
from unittest.mock import patch

import pytest

from TheAntFarm import the_ant_farm

PLUGIN_VARIABLES = ("QT_PLUGIN_PATH", "QT_QPA_PLATFORM_PLUGIN_PATH")


@pytest.mark.parametrize("system", ["Windows", "Darwin", "Linux"])
def test_no_plugin_folder_is_set(system: str) -> None:
    with (
        patch.dict(os.environ),
        patch.object(the_ant_farm.platform, "system", return_value=system),
        patch.object(the_ant_farm.os, "add_dll_directory", create=True),
    ):
        for variable in PLUGIN_VARIABLES:
            os.environ.pop(variable, None)

        the_ant_farm.config_os()

        assert not [variable for variable in PLUGIN_VARIABLES if variable in os.environ]
