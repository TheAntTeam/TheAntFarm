"""config_os prepares the Qt environment of each operating system."""

import os
from unittest.mock import patch

import pytest

from TheAntFarm import the_ant_farm

LINUX_KEYS = ("QT_PLUGIN_PATH", "QT_QPA_PLATFORM_PLUGIN_PATH", "QT_QPA_PLATFORM", "GDK_BACKEND")


@pytest.fixture
def linux_env():
    """An environment without the Linux keys; the real one is restored afterwards."""
    with patch.dict(os.environ):
        for key in LINUX_KEYS:
            os.environ.pop(key, None)
        with patch.object(the_ant_farm.platform, "system", return_value="Linux"):
            yield os.environ


class TestConfigOsOnLinux:
    def test_defaults(self, linux_env):
        the_ant_farm.config_os()

        assert linux_env["QT_QPA_PLATFORM"] == "wayland;xcb"
        assert linux_env["GDK_BACKEND"] == "x11"

    def test_the_environment_wins(self, linux_env):
        linux_env["QT_QPA_PLATFORM"] = "xcb"
        linux_env["GDK_BACKEND"] = "wayland"

        the_ant_farm.config_os()

        assert linux_env["QT_QPA_PLATFORM"] == "xcb"
        assert linux_env["GDK_BACKEND"] == "wayland"
