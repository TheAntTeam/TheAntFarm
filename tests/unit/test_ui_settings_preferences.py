import pytest
from collections import OrderedDict as Od
from unittest.mock import MagicMock, Mock, patch


@pytest.fixture
def mock_ui():
    ui = MagicMock()
    ui.tool_probe_wm_pos_chb = MagicMock()
    ui.tool_probe_x_mpos_dsb = MagicMock()
    ui.tool_probe_y_mpos_dsb = MagicMock()
    ui.tool_probe_z_mpos_dsb = MagicMock()
    ui.tool_probe_x_wpos_dsb = MagicMock()
    ui.tool_probe_y_wpos_dsb = MagicMock()
    ui.tool_probe_z_wpos_dsb = MagicMock()
    ui.tool_change_x_mpos_dsb = MagicMock()
    ui.tool_change_y_mpos_dsb = MagicMock()
    ui.tool_change_z_mpos_dsb = MagicMock()
    ui.tool_probe_z_limit_dsb = MagicMock()
    ui.hold_on_probe_chb = MagicMock()
    ui.zeroing_after_probe_chb = MagicMock()
    ui.feedrate_xy_dsb = MagicMock()
    ui.feedrate_z_dsb = MagicMock()
    ui.feedrate_probe_dsb = MagicMock()
    ui.x_mirror_rb = MagicMock()
    ui.y_mirror_rb = MagicMock()
    ui.alignment_drill_diameter_dsb = MagicMock()
    ui.x_tool_camera_offset_dsb = MagicMock()
    ui.y_tool_camera_offset_dsb = MagicMock()
    ui.camera_rotation_dsb = MagicMock()
    ui.flip_cam_h_chb = MagicMock()
    ui.flip_cam_v_chb = MagicMock()
    ui.serial_error_warning_threshold_sb = MagicMock()
    ui.serial_error_critical_threshold_sb = MagicMock()
    ui.get_tool_probe_pb = MagicMock()
    ui.get_tool_change_pb = MagicMock()
    ui.top_layer_color_pb = MagicMock()
    ui.bottom_layer_color_pb = MagicMock()
    ui.profile_layer_color_pb = MagicMock()
    ui.drill_layer_color_pb = MagicMock()
    ui.nc_top_layer_color_pb = MagicMock()
    ui.nc_bottom_layer_color_pb = MagicMock()
    ui.top_layer_color_la = MagicMock()
    ui.bottom_layer_color_la = MagicMock()
    ui.profile_layer_color_la = MagicMock()
    ui.drill_layer_color_la = MagicMock()
    ui.nc_top_layer_color_la = MagicMock()
    ui.nc_bottom_layer_color_la = MagicMock()
    ui.tool_probe_wm_pos_chb = MagicMock()
    ui.tool_probe_wm_pos_chb.isChecked.return_value = False
    ui.save_settings_preferences_pb = MagicMock()
    ui.restore_settings_preferences_pb = MagicMock()
    ui.status_bar = MagicMock()
    return ui


@pytest.fixture
def mock_control_worker():
    worker = MagicMock()
    worker.report_status_report = MagicMock()
    worker.update_gerber_cfg = MagicMock()
    return worker


@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.app_settings = MagicMock()
    settings.app_settings.layer_color = {"top": "blue", "bottom": "red", "profile": "green", "drill": "yellow", "nc_top": "gray", "nc_bottom": "white"}
    settings.app_settings.serial_error_warning_threshold = 5
    settings.app_settings.serial_error_critical_threshold = 10
    settings.app_settings.camera_rotation_angle = 0
    settings.app_settings.camera_flip_h = False
    settings.app_settings.camera_flip_v = False
    settings.jobs_settings = MagicMock()
    settings.jobs_settings.jobs_settings_od = {"common": {"mirroring_axis": "X"}}
    return settings


@pytest.fixture
def mock_machine_settings():
    m_settings = MagicMock()
    m_settings.tool_probe_rel_flag = False
    m_settings.hold_on_probe_flag = False
    m_settings.zeroing_after_probe_flag = False
    m_settings.tool_probe_offset_x_mpos = 0.0
    m_settings.tool_probe_offset_y_mpos = 0.0
    m_settings.tool_probe_offset_z_mpos = 0.0
    m_settings.tool_probe_offset_x_wpos = 0.0
    m_settings.tool_probe_offset_y_wpos = 0.0
    m_settings.tool_probe_offset_z_wpos = 0.0
    m_settings.tool_change_offset_x_mpos = 0.0
    m_settings.tool_change_offset_y_mpos = 0.0
    m_settings.tool_change_offset_z_mpos = 0.0
    m_settings.tool_probe_z_limit = 0.0
    m_settings.feedrate_xy = 100.0
    m_settings.feedrate_z = 50.0
    m_settings.feedrate_probe = 50.0
    m_settings.alignment_drill_diameter = 0.7
    m_settings.tool_camera_offset_x = 0.0
    m_settings.tool_camera_offset_y = 0.0
    return m_settings


@pytest.fixture
def ui_settings_preferences(mock_settings, mock_machine_settings):
    mock_settings.machine_settings = mock_machine_settings
    mock_ui = MagicMock()
    return mock_ui


@pytest.fixture
def settings_tab(mock_ui, mock_control_worker, mock_settings):
    from TheAntFarm.ui_manager.ui_settings_preferences import UiSettingsPreferencesTab
    return UiSettingsPreferencesTab(mock_ui, mock_control_worker, mock_settings)


class TestResetApplicationSettings:
    def test_reset_application_settings(self, settings_tab, mock_ui):
        mock_ui.top_layer_color_la = MagicMock()
        settings_tab.reset_application_settings()
        mock_ui.top_layer_color_la.setStyleSheet.assert_called()


class TestResetSerialErrorThresholds:
    def test_reset_serial_error_thresholds(self, settings_tab, mock_ui, mock_settings):
        settings_tab.reset_serial_error_thresholds()
        mock_ui.serial_error_warning_threshold_sb.setValue.assert_called()


class TestResetJobsCommonInitialSettings:
    def test_reset_jobs_common_initial_settings_x(self, settings_tab, mock_ui, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od["common"]["mirroring_axis"] = "x"
        mock_ui.x_mirror_rb = MagicMock()
        mock_ui.y_mirror_rb = MagicMock()
        settings_tab.reset_jobs_common_initial_settings()
        mock_ui.x_mirror_rb.setChecked.assert_called_with(True)

    def test_reset_jobs_common_initial_settings_y(self, settings_tab, mock_ui, mock_settings):
        mock_settings.jobs_settings.jobs_settings_od["common"]["mirroring_axis"] = "y"
        mock_ui.x_mirror_rb = MagicMock()
        mock_ui.y_mirror_rb = MagicMock()
        settings_tab.reset_jobs_common_initial_settings()
        mock_ui.y_mirror_rb.setChecked.assert_called_with(True)


class TestResetToolProbeInitialEnables:
    def test_reset_tool_probe_initial_enables(self, settings_tab, mock_ui):
        mock_ui.tool_probe_wm_pos_chb.isChecked.return_value = False
        settings_tab.reset_tool_probe_initial_enables()
        mock_ui.tool_probe_wm_pos_chb.setChecked.assert_called()


class TestResetProbeInitialSettings:
    def test_reset_probe_initial_settings(self, settings_tab, mock_ui):
        settings_tab.reset_probe_initial_settings()
        mock_ui.hold_on_probe_chb.setChecked.assert_called()


class TestResetToolMachineInitialSettings:
    def test_reset_tool_machine_initial_settings(self, settings_tab, mock_ui):
        settings_tab.reset_tool_machine_initial_settings()
        mock_ui.tool_probe_x_mpos_dsb.setValue.assert_called()


class TestRestoreInitialSettings:
    def test_restore_initial_settings(self, settings_tab, mock_ui, mock_settings):
        settings_tab.settings_dirty = True
        settings_tab.restore_initial_settings()
        mock_ui.status_bar.showMessage.assert_called()
        assert settings_tab.settings_dirty is False


class TestUiToolProbeSetEnabling:
    def test_ui_tool_probe_set_enabling_true(self, settings_tab, mock_ui):
        settings_tab.ui_tool_probe_set_enabling(True)
        mock_ui.get_tool_probe_pb.setEnabled.assert_called_with(True)

    def test_ui_tool_probe_set_enabling_false(self, settings_tab, mock_ui):
        settings_tab.ui_tool_probe_set_enabling(False)
        mock_ui.get_tool_probe_pb.setEnabled.assert_called_with(False)


class TestUiToolChangeSetEnabling:
    def test_ui_tool_change_set_enabling_true(self, settings_tab, mock_ui):
        settings_tab.ui_tool_change_set_enabling(True)
        mock_ui.get_tool_change_pb.setEnabled.assert_called_with(True)

    def test_ui_tool_change_set_enabling_false(self, settings_tab, mock_ui):
        settings_tab.ui_tool_change_set_enabling(False)
        mock_ui.get_tool_change_pb.setEnabled.assert_called_with(False)


class TestToolProbeWmPosChecked:
    def test_tool_probe_wm_pos_checked(self, settings_tab, mock_ui):
        mock_ui.tool_probe_wm_pos_chb.isChecked.return_value = True
        settings_tab.tool_probe_wm_pos_checked()
        mock_ui.tool_probe_x_mpos_dsb.setEnabled.assert_called_with(False)
        mock_ui.tool_probe_x_wpos_dsb.setEnabled.assert_called_with(True)


class TestEnableDisableToolProbeWposMpos:
    def test_enable_disable_wpos(self, settings_tab, mock_ui):
        settings_tab.enable_disable_tool_probe_wpos_mpos(True)
        mock_ui.tool_probe_x_mpos_dsb.setEnabled.assert_called_with(False)
        mock_ui.tool_probe_x_wpos_dsb.setEnabled.assert_called_with(True)

    def test_enable_disable_mpos(self, settings_tab, mock_ui):
        settings_tab.enable_disable_tool_probe_wpos_mpos(False)
        mock_ui.tool_probe_x_mpos_dsb.setEnabled.assert_called_with(True)
        mock_ui.tool_probe_x_wpos_dsb.setEnabled.assert_called_with(False)


class TestAskStatusReport:
    def test_ask_status_report(self, settings_tab):
        settings_tab.ask_status_report()


class TestAskToolProbePosition:
    def test_ask_tool_probe_position(self, settings_tab):
        settings_tab.ask_tool_probe_position()
        assert settings_tab.get_tool_probe_flag is True


class TestAskToolChangePosition:
    def test_ask_tool_change_position(self, settings_tab):
        settings_tab.ask_tool_change_position()
        assert settings_tab.get_tool_change_flag is True


class TestAskToolCameraOffset:
    def test_ask_tool_camera_offset(self, settings_tab):
        settings_tab.ask_tool_camera_offset()
        assert settings_tab.get_tool_camera_offset_flag is True


class TestGetToolProbePosition:
    def test_get_tool_probe_position_wpos(self, settings_tab, mock_ui):
        mock_ui.tool_probe_wm_pos_chb.isChecked.return_value = True
        status_report = {"wpos": [1.0, 2.0, 3.0]}
        settings_tab.get_tool_probe_position(status_report)
        mock_ui.tool_probe_x_wpos_dsb.setValue.assert_called_with(1.0)

    def test_get_tool_probe_position_mpos(self, settings_tab, mock_ui):
        mock_ui.tool_probe_wm_pos_chb.isChecked.return_value = False
        status_report = {"mpos": [1.0, 2.0, 3.0]}
        settings_tab.get_tool_probe_position(status_report)
        mock_ui.tool_probe_x_mpos_dsb.setValue.assert_called_with(1.0)


class TestGetToolChangePosition:
    def test_get_tool_change_position(self, settings_tab, mock_ui):
        status_report = {"mpos": [1.0, 2.0, 3.0]}
        settings_tab.get_tool_change_position(status_report)
        mock_ui.tool_change_x_mpos_dsb.setValue.assert_called_with(1.0)


class TestGetToolCameraOffset:
    def test_get_tool_camera_offset(self, settings_tab, mock_ui):
        status_report = {"wpos": [1.0, 2.0, 3.0]}
        settings_tab.get_tool_camera_offset(status_report)
        mock_ui.x_tool_camera_offset_dsb.setValue.assert_called_with(1.0)


class TestGetAndManageStatusReport:
    def test_get_and_manage_status_report_probe(self, settings_tab):
        settings_tab.get_tool_probe_flag = True
        settings_tab.get_tool_change_flag = False
        settings_tab.get_tool_camera_offset_flag = False
        status_report = {"mpos": [1.0, 2.0, 3.0], "wpos": [1.0, 2.0, 3.0]}
        settings_tab.get_and_manage_status_report(status_report)
        assert settings_tab.get_tool_probe_flag is False

    def test_get_and_manage_status_report_change(self, settings_tab):
        settings_tab.get_tool_probe_flag = False
        settings_tab.get_tool_change_flag = True
        settings_tab.get_tool_camera_offset_flag = False
        status_report = {"mpos": [1.0, 2.0, 3.0], "wpos": [1.0, 2.0, 3.0]}
        settings_tab.get_and_manage_status_report(status_report)
        assert settings_tab.get_tool_change_flag is False

    def test_get_and_manage_status_report_camera(self, settings_tab):
        settings_tab.get_tool_probe_flag = False
        settings_tab.get_tool_change_flag = False
        settings_tab.get_tool_camera_offset_flag = True
        status_report = {"mpos": [1.0, 2.0, 3.0], "wpos": [1.0, 2.0, 3.0]}
        settings_tab.get_and_manage_status_report(status_report)
        assert settings_tab.get_tool_camera_offset_flag is False


class TestSettingsDirtyFlag:
    def test_initial_dirty_false(self, settings_tab):
        assert settings_tab.settings_dirty is False

    def test_set_focus_lost_sets_dirty(self, settings_tab):
        settings_tab.set_focus_lost()
        assert settings_tab.settings_dirty is True

    def test_reset_focus_lost_clears_dirty(self, settings_tab):
        settings_tab.settings_dirty = True
        settings_tab.reset_focus_lost()
        assert settings_tab.settings_dirty is False

    def test_has_unsaved_changes_returns_true(self, settings_tab):
        settings_tab.settings_dirty = True
        assert settings_tab.has_unsaved_changes() is True

    def test_has_unsaved_changes_returns_false(self, settings_tab):
        settings_tab.settings_dirty = False
        assert settings_tab.has_unsaved_changes() is False

    def test_restore_initial_settings_clears_dirty(self, settings_tab, mock_ui, mock_settings):
        settings_tab.settings_dirty = True
        settings_tab.restore_initial_settings()
        assert settings_tab.settings_dirty is False

    def test_save_settings_preferences_clears_dirty(self, settings_tab, mock_ui):
        settings_tab.settings_dirty = True
        settings_tab.save_settings_preferences()
        assert settings_tab.settings_dirty is False


class TestSetFocusLost:
    def test_set_focus_lost(self, settings_tab):
        settings_tab.set_focus_lost()
        assert settings_tab.settings_dirty is True