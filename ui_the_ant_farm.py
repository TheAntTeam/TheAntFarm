# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'the_ant_farm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from vispy_qt_widget import VispyCanvas

import app_resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1160, 952)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1160, 720))
        icon = QIcon()
        icon.addFile(u":/resources/resources/logo/the_ant_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.actionHide_Show_Console = QAction(MainWindow)
        self.actionHide_Show_Console.setObjectName(u"actionHide_Show_Console")
        self.actionHide_Show_Console.setCheckable(True)
        self.actionHide_Show_Console.setChecked(False)
        self.actionSettings_Preferences = QAction(MainWindow)
        self.actionSettings_Preferences.setObjectName(u"actionSettings_Preferences")
        self.actionSettings_Preferences.setCheckable(True)
        self.actionSettings_Preferences.setChecked(False)
        self.actionSave_Settings = QAction(MainWindow)
        self.actionSave_Settings.setObjectName(u"actionSave_Settings")
        self.action_critical = QAction(MainWindow)
        self.action_critical.setObjectName(u"action_critical")
        self.action_critical.setCheckable(True)
        self.action_error = QAction(MainWindow)
        self.action_error.setObjectName(u"action_error")
        self.action_error.setCheckable(True)
        self.action_warning = QAction(MainWindow)
        self.action_warning.setObjectName(u"action_warning")
        self.action_warning.setCheckable(True)
        self.action_info = QAction(MainWindow)
        self.action_info.setObjectName(u"action_info")
        self.action_info.setCheckable(True)
        self.action_info.setChecked(True)
        self.action_debug = QAction(MainWindow)
        self.action_debug.setObjectName(u"action_debug")
        self.action_debug.setCheckable(True)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.central_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.main_tab_widget = QTabWidget(self.central_widget)
        self.main_tab_widget.setObjectName(u"main_tab_widget")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.main_tab_widget.setFont(font)
        self.main_tab_widget.setTabShape(QTabWidget.Rounded)
        self.main_tab_widget.setTabsClosable(False)
        self.main_tab_widget.setTabBarAutoHide(False)
        self.view_tab = QWidget()
        self.view_tab.setObjectName(u"view_tab")
        self.view_tab.setFont(font)
        self.horizontalLayout_8 = QHBoxLayout(self.view_tab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.prepare_widget = QTabWidget(self.view_tab)
        self.prepare_widget.setObjectName(u"prepare_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.prepare_widget.sizePolicy().hasHeightForWidth())
        self.prepare_widget.setSizePolicy(sizePolicy1)
        self.prepare_widget.setTabPosition(QTabWidget.North)
        self.prepare_widget.setTabShape(QTabWidget.Rounded)
        self.load_layers_tab = QWidget()
        self.load_layers_tab.setObjectName(u"load_layers_tab")
        self.verticalLayout_7 = QVBoxLayout(self.load_layers_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.no_copper_1_le = QLineEdit(self.load_layers_tab)
        self.no_copper_1_le.setObjectName(u"no_copper_1_le")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.no_copper_1_le.sizePolicy().hasHeightForWidth())
        self.no_copper_1_le.setSizePolicy(sizePolicy2)
        self.no_copper_1_le.setReadOnly(True)

        self.gridLayout.addWidget(self.no_copper_1_le, 5, 0, 1, 1)

        self.no_copper_2_pb = QPushButton(self.load_layers_tab)
        self.no_copper_2_pb.setObjectName(u"no_copper_2_pb")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.no_copper_2_pb.sizePolicy().hasHeightForWidth())
        self.no_copper_2_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.no_copper_2_pb, 6, 1, 1, 1)

        self.no_copper_2_chb = QCheckBox(self.load_layers_tab)
        self.no_copper_2_chb.setObjectName(u"no_copper_2_chb")
        sizePolicy3.setHeightForWidth(self.no_copper_2_chb.sizePolicy().hasHeightForWidth())
        self.no_copper_2_chb.setSizePolicy(sizePolicy3)
        self.no_copper_2_chb.setChecked(True)

        self.gridLayout.addWidget(self.no_copper_2_chb, 6, 2, 1, 1, Qt.AlignHCenter)

        self.profile_file_le = QLineEdit(self.load_layers_tab)
        self.profile_file_le.setObjectName(u"profile_file_le")
        sizePolicy2.setHeightForWidth(self.profile_file_le.sizePolicy().hasHeightForWidth())
        self.profile_file_le.setSizePolicy(sizePolicy2)
        self.profile_file_le.setReadOnly(True)

        self.gridLayout.addWidget(self.profile_file_le, 3, 0, 1, 1)

        self.view_label = QLabel(self.load_layers_tab)
        self.view_label.setObjectName(u"view_label")
        sizePolicy3.setHeightForWidth(self.view_label.sizePolicy().hasHeightForWidth())
        self.view_label.setSizePolicy(sizePolicy3)
        self.view_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.view_label, 0, 2, 1, 1, Qt.AlignHCenter)

        self.top_view_chb = QCheckBox(self.load_layers_tab)
        self.top_view_chb.setObjectName(u"top_view_chb")
        sizePolicy3.setHeightForWidth(self.top_view_chb.sizePolicy().hasHeightForWidth())
        self.top_view_chb.setSizePolicy(sizePolicy3)
        self.top_view_chb.setChecked(True)
        self.top_view_chb.setTristate(False)

        self.gridLayout.addWidget(self.top_view_chb, 1, 2, 1, 1, Qt.AlignHCenter)

        self.drill_file_le = QLineEdit(self.load_layers_tab)
        self.drill_file_le.setObjectName(u"drill_file_le")
        sizePolicy2.setHeightForWidth(self.drill_file_le.sizePolicy().hasHeightForWidth())
        self.drill_file_le.setSizePolicy(sizePolicy2)
        self.drill_file_le.setReadOnly(True)

        self.gridLayout.addWidget(self.drill_file_le, 4, 0, 1, 1)

        self.no_copper_1_pb = QPushButton(self.load_layers_tab)
        self.no_copper_1_pb.setObjectName(u"no_copper_1_pb")
        sizePolicy3.setHeightForWidth(self.no_copper_1_pb.sizePolicy().hasHeightForWidth())
        self.no_copper_1_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.no_copper_1_pb, 5, 1, 1, 1)

        self.bottom_view_chb = QCheckBox(self.load_layers_tab)
        self.bottom_view_chb.setObjectName(u"bottom_view_chb")
        sizePolicy3.setHeightForWidth(self.bottom_view_chb.sizePolicy().hasHeightForWidth())
        self.bottom_view_chb.setSizePolicy(sizePolicy3)
        self.bottom_view_chb.setChecked(True)

        self.gridLayout.addWidget(self.bottom_view_chb, 2, 2, 1, 1, Qt.AlignHCenter)

        self.profile_load_pb = QPushButton(self.load_layers_tab)
        self.profile_load_pb.setObjectName(u"profile_load_pb")
        sizePolicy3.setHeightForWidth(self.profile_load_pb.sizePolicy().hasHeightForWidth())
        self.profile_load_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.profile_load_pb, 3, 1, 1, 1)

        self.no_copper_2_le = QLineEdit(self.load_layers_tab)
        self.no_copper_2_le.setObjectName(u"no_copper_2_le")
        sizePolicy2.setHeightForWidth(self.no_copper_2_le.sizePolicy().hasHeightForWidth())
        self.no_copper_2_le.setSizePolicy(sizePolicy2)
        self.no_copper_2_le.setReadOnly(True)

        self.gridLayout.addWidget(self.no_copper_2_le, 6, 0, 1, 1)

        self.no_copper_1_chb = QCheckBox(self.load_layers_tab)
        self.no_copper_1_chb.setObjectName(u"no_copper_1_chb")
        sizePolicy3.setHeightForWidth(self.no_copper_1_chb.sizePolicy().hasHeightForWidth())
        self.no_copper_1_chb.setSizePolicy(sizePolicy3)
        self.no_copper_1_chb.setChecked(True)

        self.gridLayout.addWidget(self.no_copper_1_chb, 5, 2, 1, 1, Qt.AlignHCenter)

        self.clear_views_pb = QPushButton(self.load_layers_tab)
        self.clear_views_pb.setObjectName(u"clear_views_pb")
        sizePolicy3.setHeightForWidth(self.clear_views_pb.sizePolicy().hasHeightForWidth())
        self.clear_views_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.clear_views_pb, 8, 1, 1, 1)

        self.drill_load_pb = QPushButton(self.load_layers_tab)
        self.drill_load_pb.setObjectName(u"drill_load_pb")
        sizePolicy3.setHeightForWidth(self.drill_load_pb.sizePolicy().hasHeightForWidth())
        self.drill_load_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.drill_load_pb, 4, 1, 1, 1)

        self.top_load_pb = QPushButton(self.load_layers_tab)
        self.top_load_pb.setObjectName(u"top_load_pb")
        sizePolicy3.setHeightForWidth(self.top_load_pb.sizePolicy().hasHeightForWidth())
        self.top_load_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.top_load_pb, 1, 1, 1, 1)

        self.bottom_file_le = QLineEdit(self.load_layers_tab)
        self.bottom_file_le.setObjectName(u"bottom_file_le")
        sizePolicy2.setHeightForWidth(self.bottom_file_le.sizePolicy().hasHeightForWidth())
        self.bottom_file_le.setSizePolicy(sizePolicy2)
        self.bottom_file_le.setReadOnly(True)

        self.gridLayout.addWidget(self.bottom_file_le, 2, 0, 1, 1)

        self.bottom_load_pb = QPushButton(self.load_layers_tab)
        self.bottom_load_pb.setObjectName(u"bottom_load_pb")
        sizePolicy3.setHeightForWidth(self.bottom_load_pb.sizePolicy().hasHeightForWidth())
        self.bottom_load_pb.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.bottom_load_pb, 2, 1, 1, 1)

        self.drill_view_chb = QCheckBox(self.load_layers_tab)
        self.drill_view_chb.setObjectName(u"drill_view_chb")
        sizePolicy3.setHeightForWidth(self.drill_view_chb.sizePolicy().hasHeightForWidth())
        self.drill_view_chb.setSizePolicy(sizePolicy3)
        self.drill_view_chb.setChecked(True)

        self.gridLayout.addWidget(self.drill_view_chb, 4, 2, 1, 1, Qt.AlignHCenter)

        self.file_path_l = QLabel(self.load_layers_tab)
        self.file_path_l.setObjectName(u"file_path_l")
        sizePolicy3.setHeightForWidth(self.file_path_l.sizePolicy().hasHeightForWidth())
        self.file_path_l.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.file_path_l, 0, 0, 1, 1, Qt.AlignHCenter)

        self.top_file_le = QLineEdit(self.load_layers_tab)
        self.top_file_le.setObjectName(u"top_file_le")
        sizePolicy2.setHeightForWidth(self.top_file_le.sizePolicy().hasHeightForWidth())
        self.top_file_le.setSizePolicy(sizePolicy2)
        self.top_file_le.setReadOnly(True)

        self.gridLayout.addWidget(self.top_file_le, 1, 0, 1, 1)

        self.all_view_chb = QCheckBox(self.load_layers_tab)
        self.all_view_chb.setObjectName(u"all_view_chb")
        sizePolicy3.setHeightForWidth(self.all_view_chb.sizePolicy().hasHeightForWidth())
        self.all_view_chb.setSizePolicy(sizePolicy3)
        self.all_view_chb.setChecked(True)

        self.gridLayout.addWidget(self.all_view_chb, 8, 2, 1, 1, Qt.AlignHCenter)

        self.profile_view_chb = QCheckBox(self.load_layers_tab)
        self.profile_view_chb.setObjectName(u"profile_view_chb")
        sizePolicy3.setHeightForWidth(self.profile_view_chb.sizePolicy().hasHeightForWidth())
        self.profile_view_chb.setSizePolicy(sizePolicy3)
        self.profile_view_chb.setChecked(True)

        self.gridLayout.addWidget(self.profile_view_chb, 3, 2, 1, 1, Qt.AlignHCenter)

        self.horizontal_spacer = QSpacerItem(140, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontal_spacer, 8, 0, 1, 1)

        self.horizontal_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontal_spacer_2, 7, 0, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.prepare_widget.addTab(self.load_layers_tab, "")
        self.create_job_tab = QWidget()
        self.create_job_tab.setObjectName(u"create_job_tab")
        self.verticalLayout_8 = QVBoxLayout(self.create_job_tab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.layer_choice_cb = QComboBox(self.create_job_tab)
        self.layer_choice_cb.setObjectName(u"layer_choice_cb")

        self.verticalLayout_8.addWidget(self.layer_choice_cb)

        self.jobs_sw = QStackedWidget(self.create_job_tab)
        self.jobs_sw.setObjectName(u"jobs_sw")
        self.empty_page = QWidget()
        self.empty_page.setObjectName(u"empty_page")
        self.gridLayout_8 = QGridLayout(self.empty_page)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label = QLabel(self.empty_page)
        self.label.setObjectName(u"label")

        self.gridLayout_8.addWidget(self.label, 0, 0, 1, 1)

        self.jobs_sw.addWidget(self.empty_page)
        self.top_page = QWidget()
        self.top_page.setObjectName(u"top_page")
        self.gridLayout_2 = QGridLayout(self.top_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.top_cut_z_dsb = QDoubleSpinBox(self.top_page)
        self.top_cut_z_dsb.setObjectName(u"top_cut_z_dsb")
        self.top_cut_z_dsb.setDecimals(2)
        self.top_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.top_cut_z_dsb.setMaximum(9999.000000000000000)
        self.top_cut_z_dsb.setValue(0.000000000000000)

        self.gridLayout_2.addWidget(self.top_cut_z_dsb, 3, 1, 1, 1)

        self.top_tool_diameter_la = QLabel(self.top_page)
        self.top_tool_diameter_la.setObjectName(u"top_tool_diameter_la")

        self.gridLayout_2.addWidget(self.top_tool_diameter_la, 0, 0, 1, 1)

        self.top_generate_job_pb = QPushButton(self.top_page)
        self.top_generate_job_pb.setObjectName(u"top_generate_job_pb")

        self.gridLayout_2.addWidget(self.top_generate_job_pb, 11, 0, 1, 2)

        self.top_n_passes_la = QLabel(self.top_page)
        self.top_n_passes_la.setObjectName(u"top_n_passes_la")

        self.gridLayout_2.addWidget(self.top_n_passes_la, 1, 0, 1, 1)

        self.top_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.top_vertical_spacer, 10, 0, 1, 2)

        self.top_travel_z_la = QLabel(self.top_page)
        self.top_travel_z_la.setObjectName(u"top_travel_z_la")

        self.gridLayout_2.addWidget(self.top_travel_z_la, 4, 0, 1, 1)

        self.top_travel_z_dsb = QDoubleSpinBox(self.top_page)
        self.top_travel_z_dsb.setObjectName(u"top_travel_z_dsb")
        self.top_travel_z_dsb.setDecimals(2)
        self.top_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.top_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.top_travel_z_dsb, 4, 1, 1, 1)

        self.top_cut_z_la = QLabel(self.top_page)
        self.top_cut_z_la.setObjectName(u"top_cut_z_la")

        self.gridLayout_2.addWidget(self.top_cut_z_la, 3, 0, 1, 1)

        self.top_overlap_la = QLabel(self.top_page)
        self.top_overlap_la.setObjectName(u"top_overlap_la")

        self.gridLayout_2.addWidget(self.top_overlap_la, 2, 0, 1, 1)

        self.top_spindle_speed_la = QLabel(self.top_page)
        self.top_spindle_speed_la.setObjectName(u"top_spindle_speed_la")

        self.gridLayout_2.addWidget(self.top_spindle_speed_la, 6, 0, 1, 1)

        self.top_xy_feed_rate_dsb = QDoubleSpinBox(self.top_page)
        self.top_xy_feed_rate_dsb.setObjectName(u"top_xy_feed_rate_dsb")
        self.top_xy_feed_rate_dsb.setDecimals(2)
        self.top_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.top_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.top_xy_feed_rate_dsb, 7, 1, 1, 1)

        self.top_tool_diameter_dsb = QDoubleSpinBox(self.top_page)
        self.top_tool_diameter_dsb.setObjectName(u"top_tool_diameter_dsb")
        self.top_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_2.addWidget(self.top_tool_diameter_dsb, 0, 1, 1, 1)

        self.top_xy_feed_rate_la = QLabel(self.top_page)
        self.top_xy_feed_rate_la.setObjectName(u"top_xy_feed_rate_la")

        self.gridLayout_2.addWidget(self.top_xy_feed_rate_la, 7, 0, 1, 1)

        self.top_n_passes_sb = QSpinBox(self.top_page)
        self.top_n_passes_sb.setObjectName(u"top_n_passes_sb")
        self.top_n_passes_sb.setMinimum(1)

        self.gridLayout_2.addWidget(self.top_n_passes_sb, 1, 1, 1, 1)

        self.top_spindle_speed_dsb = QDoubleSpinBox(self.top_page)
        self.top_spindle_speed_dsb.setObjectName(u"top_spindle_speed_dsb")
        self.top_spindle_speed_dsb.setDecimals(2)
        self.top_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.top_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.top_spindle_speed_dsb, 6, 1, 1, 1)

        self.top_overlap_dsb = QDoubleSpinBox(self.top_page)
        self.top_overlap_dsb.setObjectName(u"top_overlap_dsb")
        self.top_overlap_dsb.setDecimals(1)
        self.top_overlap_dsb.setMinimum(0.000000000000000)
        self.top_overlap_dsb.setMaximum(1.000000000000000)

        self.gridLayout_2.addWidget(self.top_overlap_dsb, 2, 1, 1, 1)

        self.top_z_feed_rate_la = QLabel(self.top_page)
        self.top_z_feed_rate_la.setObjectName(u"top_z_feed_rate_la")

        self.gridLayout_2.addWidget(self.top_z_feed_rate_la, 9, 0, 1, 1)

        self.top_z_feed_rate_dsb = QDoubleSpinBox(self.top_page)
        self.top_z_feed_rate_dsb.setObjectName(u"top_z_feed_rate_dsb")
        self.top_z_feed_rate_dsb.setDecimals(2)
        self.top_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.top_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.top_z_feed_rate_dsb, 9, 1, 1, 1)

        self.jobs_sw.addWidget(self.top_page)
        self.bottom_page = QWidget()
        self.bottom_page.setObjectName(u"bottom_page")
        self.gridLayout_3 = QGridLayout(self.bottom_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bottom_z_feed_rate_la = QLabel(self.bottom_page)
        self.bottom_z_feed_rate_la.setObjectName(u"bottom_z_feed_rate_la")

        self.gridLayout_3.addWidget(self.bottom_z_feed_rate_la, 9, 0, 1, 1)

        self.bottom_cut_z_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_cut_z_dsb.setObjectName(u"bottom_cut_z_dsb")
        self.bottom_cut_z_dsb.setDecimals(2)
        self.bottom_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.bottom_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_cut_z_dsb, 4, 1, 1, 1)

        self.bottom_z_feed_rate_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_z_feed_rate_dsb.setObjectName(u"bottom_z_feed_rate_dsb")
        self.bottom_z_feed_rate_dsb.setDecimals(2)
        self.bottom_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.bottom_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_z_feed_rate_dsb, 9, 1, 1, 1)

        self.bottom_tool_diameter_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_tool_diameter_dsb.setObjectName(u"bottom_tool_diameter_dsb")
        self.bottom_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_3.addWidget(self.bottom_tool_diameter_dsb, 1, 1, 1, 1)

        self.bottom_n_passes_sb = QSpinBox(self.bottom_page)
        self.bottom_n_passes_sb.setObjectName(u"bottom_n_passes_sb")
        self.bottom_n_passes_sb.setMinimum(1)

        self.gridLayout_3.addWidget(self.bottom_n_passes_sb, 2, 1, 1, 1)

        self.bottom_overlap_la = QLabel(self.bottom_page)
        self.bottom_overlap_la.setObjectName(u"bottom_overlap_la")

        self.gridLayout_3.addWidget(self.bottom_overlap_la, 3, 0, 1, 1)

        self.bottom_generate_job_pb = QPushButton(self.bottom_page)
        self.bottom_generate_job_pb.setObjectName(u"bottom_generate_job_pb")

        self.gridLayout_3.addWidget(self.bottom_generate_job_pb, 12, 0, 1, 2)

        self.bottom_xy_feed_rate_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_xy_feed_rate_dsb.setObjectName(u"bottom_xy_feed_rate_dsb")
        self.bottom_xy_feed_rate_dsb.setDecimals(2)
        self.bottom_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.bottom_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_xy_feed_rate_dsb, 8, 1, 1, 1)

        self.bottom_overlap_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_overlap_dsb.setObjectName(u"bottom_overlap_dsb")
        self.bottom_overlap_dsb.setDecimals(1)
        self.bottom_overlap_dsb.setMinimum(0.000000000000000)
        self.bottom_overlap_dsb.setMaximum(1.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_overlap_dsb, 3, 1, 1, 1)

        self.bottom_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.bottom_vertical_spacer, 11, 0, 1, 2)

        self.bottom_tool_diameter_la = QLabel(self.bottom_page)
        self.bottom_tool_diameter_la.setObjectName(u"bottom_tool_diameter_la")

        self.gridLayout_3.addWidget(self.bottom_tool_diameter_la, 1, 0, 1, 1)

        self.bottom_n_passes_la = QLabel(self.bottom_page)
        self.bottom_n_passes_la.setObjectName(u"bottom_n_passes_la")

        self.gridLayout_3.addWidget(self.bottom_n_passes_la, 2, 0, 1, 1)

        self.bottom_travel_z_la = QLabel(self.bottom_page)
        self.bottom_travel_z_la.setObjectName(u"bottom_travel_z_la")

        self.gridLayout_3.addWidget(self.bottom_travel_z_la, 5, 0, 1, 1)

        self.bottom_cut_z_la = QLabel(self.bottom_page)
        self.bottom_cut_z_la.setObjectName(u"bottom_cut_z_la")

        self.gridLayout_3.addWidget(self.bottom_cut_z_la, 4, 0, 1, 1)

        self.bottom_travel_z_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_travel_z_dsb.setObjectName(u"bottom_travel_z_dsb")
        self.bottom_travel_z_dsb.setDecimals(2)
        self.bottom_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.bottom_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_travel_z_dsb, 5, 1, 1, 1)

        self.bottom_xy_feed_rate_la = QLabel(self.bottom_page)
        self.bottom_xy_feed_rate_la.setObjectName(u"bottom_xy_feed_rate_la")

        self.gridLayout_3.addWidget(self.bottom_xy_feed_rate_la, 8, 0, 1, 1)

        self.bottom_spindle_speed_la = QLabel(self.bottom_page)
        self.bottom_spindle_speed_la.setObjectName(u"bottom_spindle_speed_la")

        self.gridLayout_3.addWidget(self.bottom_spindle_speed_la, 6, 0, 1, 1)

        self.bottom_spindle_speed_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_spindle_speed_dsb.setObjectName(u"bottom_spindle_speed_dsb")
        self.bottom_spindle_speed_dsb.setDecimals(2)
        self.bottom_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.bottom_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_spindle_speed_dsb, 6, 1, 1, 1)

        self.jobs_sw.addWidget(self.bottom_page)
        self.profile_page = QWidget()
        self.profile_page.setObjectName(u"profile_page")
        self.gridLayout_4 = QGridLayout(self.profile_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.profile_depth_pass_la = QLabel(self.profile_page)
        self.profile_depth_pass_la.setObjectName(u"profile_depth_pass_la")

        self.gridLayout_4.addWidget(self.profile_depth_pass_la, 3, 1, 1, 1)

        self.profile_xy_feed_rate_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_xy_feed_rate_dsb.setObjectName(u"profile_xy_feed_rate_dsb")
        self.profile_xy_feed_rate_dsb.setDecimals(2)
        self.profile_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.profile_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_xy_feed_rate_dsb, 9, 3, 1, 1)

        self.profile_cut_z_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_cut_z_dsb.setObjectName(u"profile_cut_z_dsb")
        self.profile_cut_z_dsb.setDecimals(2)
        self.profile_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.profile_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_cut_z_dsb, 5, 3, 1, 1)

        self.profile_margin_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_margin_dsb.setObjectName(u"profile_margin_dsb")
        self.profile_margin_dsb.setDecimals(2)
        self.profile_margin_dsb.setMinimum(0.000000000000000)
        self.profile_margin_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_margin_dsb, 1, 3, 1, 1)

        self.profile_depth_pass_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_depth_pass_dsb.setObjectName(u"profile_depth_pass_dsb")
        self.profile_depth_pass_dsb.setDecimals(2)
        self.profile_depth_pass_dsb.setMinimum(0.000000000000000)
        self.profile_depth_pass_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_depth_pass_dsb, 3, 3, 1, 1)

        self.profile_taps_layout_la = QLabel(self.profile_page)
        self.profile_taps_layout_la.setObjectName(u"profile_taps_layout_la")

        self.gridLayout_4.addWidget(self.profile_taps_layout_la, 11, 1, 1, 1)

        self.profile_margin_la = QLabel(self.profile_page)
        self.profile_margin_la.setObjectName(u"profile_margin_la")

        self.gridLayout_4.addWidget(self.profile_margin_la, 1, 1, 1, 1)

        self.profile_tap_size_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_tap_size_dsb.setObjectName(u"profile_tap_size_dsb")
        self.profile_tap_size_dsb.setDecimals(2)
        self.profile_tap_size_dsb.setMinimum(-9999.000000000000000)
        self.profile_tap_size_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_tap_size_dsb, 12, 3, 1, 1)

        self.profile_cut_z_la = QLabel(self.profile_page)
        self.profile_cut_z_la.setObjectName(u"profile_cut_z_la")

        self.gridLayout_4.addWidget(self.profile_cut_z_la, 5, 1, 1, 1)

        self.profile_xy_feed_rate_la = QLabel(self.profile_page)
        self.profile_xy_feed_rate_la.setObjectName(u"profile_xy_feed_rate_la")

        self.gridLayout_4.addWidget(self.profile_xy_feed_rate_la, 9, 1, 1, 1)

        self.profile_z_feed_rate_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_z_feed_rate_dsb.setObjectName(u"profile_z_feed_rate_dsb")
        self.profile_z_feed_rate_dsb.setDecimals(2)
        self.profile_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.profile_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_z_feed_rate_dsb, 10, 3, 1, 1)

        self.profile_generate_job_pb = QPushButton(self.profile_page)
        self.profile_generate_job_pb.setObjectName(u"profile_generate_job_pb")

        self.gridLayout_4.addWidget(self.profile_generate_job_pb, 16, 1, 1, 3)

        self.profile_tool_diameter_la = QLabel(self.profile_page)
        self.profile_tool_diameter_la.setObjectName(u"profile_tool_diameter_la")

        self.gridLayout_4.addWidget(self.profile_tool_diameter_la, 0, 1, 1, 1)

        self.profile_multi_depth_chb = QCheckBox(self.profile_page)
        self.profile_multi_depth_chb.setObjectName(u"profile_multi_depth_chb")
        sizePolicy2.setHeightForWidth(self.profile_multi_depth_chb.sizePolicy().hasHeightForWidth())
        self.profile_multi_depth_chb.setSizePolicy(sizePolicy2)
        self.profile_multi_depth_chb.setMinimumSize(QSize(123, 0))

        self.gridLayout_4.addWidget(self.profile_multi_depth_chb, 2, 3, 1, 1, Qt.AlignHCenter)

        self.profile_z_feed_rate_la = QLabel(self.profile_page)
        self.profile_z_feed_rate_la.setObjectName(u"profile_z_feed_rate_la")

        self.gridLayout_4.addWidget(self.profile_z_feed_rate_la, 10, 1, 1, 1)

        self.profile_tool_diameter_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_tool_diameter_dsb.setObjectName(u"profile_tool_diameter_dsb")
        self.profile_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_4.addWidget(self.profile_tool_diameter_dsb, 0, 3, 1, 1)

        self.profile_tap_size_la = QLabel(self.profile_page)
        self.profile_tap_size_la.setObjectName(u"profile_tap_size_la")

        self.gridLayout_4.addWidget(self.profile_tap_size_la, 12, 1, 1, 1)

        self.profile_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.profile_vertical_spacer, 15, 1, 1, 3)

        self.profile_travel_z_la = QLabel(self.profile_page)
        self.profile_travel_z_la.setObjectName(u"profile_travel_z_la")

        self.gridLayout_4.addWidget(self.profile_travel_z_la, 6, 1, 1, 1)

        self.profile_travel_z_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_travel_z_dsb.setObjectName(u"profile_travel_z_dsb")
        self.profile_travel_z_dsb.setDecimals(2)
        self.profile_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.profile_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_travel_z_dsb, 6, 3, 1, 1)

        self.profile_taps_layout_cb = QComboBox(self.profile_page)
        self.profile_taps_layout_cb.setObjectName(u"profile_taps_layout_cb")

        self.gridLayout_4.addWidget(self.profile_taps_layout_cb, 11, 3, 1, 1)

        self.profile_multi_depth_la = QLabel(self.profile_page)
        self.profile_multi_depth_la.setObjectName(u"profile_multi_depth_la")

        self.gridLayout_4.addWidget(self.profile_multi_depth_la, 2, 1, 1, 1)

        self.profile_spindle_speed_la = QLabel(self.profile_page)
        self.profile_spindle_speed_la.setObjectName(u"profile_spindle_speed_la")

        self.gridLayout_4.addWidget(self.profile_spindle_speed_la, 7, 1, 1, 1)

        self.profile_spindle_speed_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_spindle_speed_dsb.setObjectName(u"profile_spindle_speed_dsb")
        self.profile_spindle_speed_dsb.setDecimals(2)
        self.profile_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.profile_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_spindle_speed_dsb, 7, 3, 1, 1)

        self.profile_mirror_la = QLabel(self.profile_page)
        self.profile_mirror_la.setObjectName(u"profile_mirror_la")

        self.gridLayout_4.addWidget(self.profile_mirror_la, 13, 1, 1, 1)

        self.profile_mirror_chb = QCheckBox(self.profile_page)
        self.profile_mirror_chb.setObjectName(u"profile_mirror_chb")
        sizePolicy2.setHeightForWidth(self.profile_mirror_chb.sizePolicy().hasHeightForWidth())
        self.profile_mirror_chb.setSizePolicy(sizePolicy2)
        self.profile_mirror_chb.setMinimumSize(QSize(123, 0))

        self.gridLayout_4.addWidget(self.profile_mirror_chb, 13, 3, 1, 1)

        self.jobs_sw.addWidget(self.profile_page)
        self.drill_page = QWidget()
        self.drill_page.setObjectName(u"drill_page")
        self.gridLayout_5 = QGridLayout(self.drill_page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.drill_milling_tool_diameter_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_milling_tool_diameter_dsb.setObjectName(u"drill_milling_tool_diameter_dsb")
        self.drill_milling_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_5.addWidget(self.drill_milling_tool_diameter_dsb, 4, 2, 1, 1)

        self.drill_travel_z_la = QLabel(self.drill_page)
        self.drill_travel_z_la.setObjectName(u"drill_travel_z_la")

        self.gridLayout_5.addWidget(self.drill_travel_z_la, 7, 1, 1, 1)

        self.add_drill_tool_tb = QToolButton(self.drill_page)
        self.add_drill_tool_tb.setObjectName(u"add_drill_tool_tb")

        self.gridLayout_5.addWidget(self.add_drill_tool_tb, 2, 1, 1, 1, Qt.AlignHCenter)

        self.drill_z_feed_rate_la = QLabel(self.drill_page)
        self.drill_z_feed_rate_la.setObjectName(u"drill_z_feed_rate_la")

        self.gridLayout_5.addWidget(self.drill_z_feed_rate_la, 12, 1, 1, 1)

        self.drill_xy_feed_rate_la = QLabel(self.drill_page)
        self.drill_xy_feed_rate_la.setObjectName(u"drill_xy_feed_rate_la")

        self.gridLayout_5.addWidget(self.drill_xy_feed_rate_la, 10, 1, 1, 1)

        self.drill_cut_z_la = QLabel(self.drill_page)
        self.drill_cut_z_la.setObjectName(u"drill_cut_z_la")

        self.gridLayout_5.addWidget(self.drill_cut_z_la, 6, 1, 1, 1)

        self.drill_travel_z_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_travel_z_dsb.setObjectName(u"drill_travel_z_dsb")
        self.drill_travel_z_dsb.setDecimals(2)
        self.drill_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.drill_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_travel_z_dsb, 7, 2, 1, 1)

        self.drill_milling_tool_la = QLabel(self.drill_page)
        self.drill_milling_tool_la.setObjectName(u"drill_milling_tool_la")

        self.gridLayout_5.addWidget(self.drill_milling_tool_la, 3, 1, 1, 1)

        self.remove_drill_tool_tb = QToolButton(self.drill_page)
        self.remove_drill_tool_tb.setObjectName(u"remove_drill_tool_tb")

        self.gridLayout_5.addWidget(self.remove_drill_tool_tb, 2, 2, 1, 1, Qt.AlignHCenter)

        self.drill_milling_tool_chb = QCheckBox(self.drill_page)
        self.drill_milling_tool_chb.setObjectName(u"drill_milling_tool_chb")

        self.gridLayout_5.addWidget(self.drill_milling_tool_chb, 3, 2, 1, 1)

        self.drill_optimization_la = QLabel(self.drill_page)
        self.drill_optimization_la.setObjectName(u"drill_optimization_la")

        self.gridLayout_5.addWidget(self.drill_optimization_la, 13, 1, 1, 1)

        self.drill_z_feed_rate_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_z_feed_rate_dsb.setObjectName(u"drill_z_feed_rate_dsb")
        self.drill_z_feed_rate_dsb.setDecimals(2)
        self.drill_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.drill_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_z_feed_rate_dsb, 12, 2, 1, 1)

        self.drill_tw = QTableWidget(self.drill_page)
        if (self.drill_tw.columnCount() < 2):
            self.drill_tw.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.drill_tw.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.drill_tw.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.drill_tw.setObjectName(u"drill_tw")
        self.drill_tw.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.drill_tw.setColumnCount(2)

        self.gridLayout_5.addWidget(self.drill_tw, 0, 1, 1, 2, Qt.AlignHCenter|Qt.AlignVCenter)

        self.drill_optimization_chb = QCheckBox(self.drill_page)
        self.drill_optimization_chb.setObjectName(u"drill_optimization_chb")

        self.gridLayout_5.addWidget(self.drill_optimization_chb, 13, 2, 1, 1)

        self.drill_cut_z_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_cut_z_dsb.setObjectName(u"drill_cut_z_dsb")
        self.drill_cut_z_dsb.setDecimals(2)
        self.drill_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.drill_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_cut_z_dsb, 6, 2, 1, 1)

        self.drill_spindle_speed_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_spindle_speed_dsb.setObjectName(u"drill_spindle_speed_dsb")
        self.drill_spindle_speed_dsb.setDecimals(2)
        self.drill_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.drill_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_spindle_speed_dsb, 8, 2, 1, 1)

        self.drill_spindle_speed_la = QLabel(self.drill_page)
        self.drill_spindle_speed_la.setObjectName(u"drill_spindle_speed_la")

        self.gridLayout_5.addWidget(self.drill_spindle_speed_la, 8, 1, 1, 1)

        self.drill_xy_feed_rate_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_xy_feed_rate_dsb.setObjectName(u"drill_xy_feed_rate_dsb")
        self.drill_xy_feed_rate_dsb.setDecimals(2)
        self.drill_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.drill_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_xy_feed_rate_dsb, 10, 2, 1, 1)

        self.drill_milling_tool_diameter_la = QLabel(self.drill_page)
        self.drill_milling_tool_diameter_la.setObjectName(u"drill_milling_tool_diameter_la")

        self.gridLayout_5.addWidget(self.drill_milling_tool_diameter_la, 4, 1, 1, 1)

        self.drill_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.drill_vertical_spacer, 15, 1, 1, 2)

        self.drill_generate_job_pb = QPushButton(self.drill_page)
        self.drill_generate_job_pb.setObjectName(u"drill_generate_job_pb")

        self.gridLayout_5.addWidget(self.drill_generate_job_pb, 16, 1, 1, 2)

        self.drill_mirror_la = QLabel(self.drill_page)
        self.drill_mirror_la.setObjectName(u"drill_mirror_la")

        self.gridLayout_5.addWidget(self.drill_mirror_la, 14, 1, 1, 1)

        self.drill_mirror_chb = QCheckBox(self.drill_page)
        self.drill_mirror_chb.setObjectName(u"drill_mirror_chb")
        sizePolicy2.setHeightForWidth(self.drill_mirror_chb.sizePolicy().hasHeightForWidth())
        self.drill_mirror_chb.setSizePolicy(sizePolicy2)
        self.drill_mirror_chb.setMinimumSize(QSize(123, 0))

        self.gridLayout_5.addWidget(self.drill_mirror_chb, 14, 2, 1, 1)

        self.jobs_sw.addWidget(self.drill_page)
        self.nc_area_top_page = QWidget()
        self.nc_area_top_page.setObjectName(u"nc_area_top_page")
        self.gridLayout_6 = QGridLayout(self.nc_area_top_page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.nc_top_overlap_la = QLabel(self.nc_area_top_page)
        self.nc_top_overlap_la.setObjectName(u"nc_top_overlap_la")

        self.gridLayout_6.addWidget(self.nc_top_overlap_la, 1, 0, 1, 1)

        self.nc_top_cut_z_la = QLabel(self.nc_area_top_page)
        self.nc_top_cut_z_la.setObjectName(u"nc_top_cut_z_la")

        self.gridLayout_6.addWidget(self.nc_top_cut_z_la, 2, 0, 1, 1)

        self.nc_top_xy_feed_rate_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_xy_feed_rate_dsb.setObjectName(u"nc_top_xy_feed_rate_dsb")
        self.nc_top_xy_feed_rate_dsb.setDecimals(2)
        self.nc_top_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.nc_top_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_xy_feed_rate_dsb, 5, 1, 1, 1)

        self.nc_top_travel_z_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_travel_z_dsb.setObjectName(u"nc_top_travel_z_dsb")
        self.nc_top_travel_z_dsb.setDecimals(2)
        self.nc_top_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.nc_top_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_travel_z_dsb, 3, 1, 1, 1)

        self.nc_top_spindle_speed_la = QLabel(self.nc_area_top_page)
        self.nc_top_spindle_speed_la.setObjectName(u"nc_top_spindle_speed_la")

        self.gridLayout_6.addWidget(self.nc_top_spindle_speed_la, 4, 0, 1, 1)

        self.nc_top_tool_diameter_la = QLabel(self.nc_area_top_page)
        self.nc_top_tool_diameter_la.setObjectName(u"nc_top_tool_diameter_la")

        self.gridLayout_6.addWidget(self.nc_top_tool_diameter_la, 0, 0, 1, 1)

        self.nc_top_cut_z_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_cut_z_dsb.setObjectName(u"nc_top_cut_z_dsb")
        self.nc_top_cut_z_dsb.setDecimals(2)
        self.nc_top_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.nc_top_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_cut_z_dsb, 2, 1, 1, 1)

        self.nc_top_travel_z_la = QLabel(self.nc_area_top_page)
        self.nc_top_travel_z_la.setObjectName(u"nc_top_travel_z_la")

        self.gridLayout_6.addWidget(self.nc_top_travel_z_la, 3, 0, 1, 1)

        self.nc_top_z_feed_rate_la = QLabel(self.nc_area_top_page)
        self.nc_top_z_feed_rate_la.setObjectName(u"nc_top_z_feed_rate_la")

        self.gridLayout_6.addWidget(self.nc_top_z_feed_rate_la, 6, 0, 1, 1)

        self.nc_top_tool_diameter_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_tool_diameter_dsb.setObjectName(u"nc_top_tool_diameter_dsb")
        self.nc_top_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_6.addWidget(self.nc_top_tool_diameter_dsb, 0, 1, 1, 1)

        self.nc_top_spindle_speed_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_spindle_speed_dsb.setObjectName(u"nc_top_spindle_speed_dsb")
        self.nc_top_spindle_speed_dsb.setDecimals(2)
        self.nc_top_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.nc_top_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_spindle_speed_dsb, 4, 1, 1, 1)

        self.nc_top_overlap_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_overlap_dsb.setObjectName(u"nc_top_overlap_dsb")
        self.nc_top_overlap_dsb.setDecimals(1)
        self.nc_top_overlap_dsb.setMinimum(0.100000000000000)
        self.nc_top_overlap_dsb.setMaximum(1.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_overlap_dsb, 1, 1, 1, 1)

        self.nc_top_xy_feed_rate_la = QLabel(self.nc_area_top_page)
        self.nc_top_xy_feed_rate_la.setObjectName(u"nc_top_xy_feed_rate_la")

        self.gridLayout_6.addWidget(self.nc_top_xy_feed_rate_la, 5, 0, 1, 1)

        self.nc_top_z_feed_rate_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_z_feed_rate_dsb.setObjectName(u"nc_top_z_feed_rate_dsb")
        self.nc_top_z_feed_rate_dsb.setDecimals(2)
        self.nc_top_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.nc_top_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_z_feed_rate_dsb, 6, 1, 1, 1)

        self.nc_top_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.nc_top_vertical_spacer, 7, 0, 1, 2)

        self.nc_top_generate_pb = QPushButton(self.nc_area_top_page)
        self.nc_top_generate_pb.setObjectName(u"nc_top_generate_pb")

        self.gridLayout_6.addWidget(self.nc_top_generate_pb, 8, 0, 1, 2)

        self.jobs_sw.addWidget(self.nc_area_top_page)
        self.nc_area_bottom_page = QWidget()
        self.nc_area_bottom_page.setObjectName(u"nc_area_bottom_page")
        self.gridLayout_7 = QGridLayout(self.nc_area_bottom_page)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.nc_bottom_travel_z_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_travel_z_la.setObjectName(u"nc_bottom_travel_z_la")

        self.gridLayout_7.addWidget(self.nc_bottom_travel_z_la, 3, 0, 1, 1)

        self.nc_bottom_generate_pb = QPushButton(self.nc_area_bottom_page)
        self.nc_bottom_generate_pb.setObjectName(u"nc_bottom_generate_pb")

        self.gridLayout_7.addWidget(self.nc_bottom_generate_pb, 9, 0, 1, 2)

        self.nc_bottom_spindle_speed_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_spindle_speed_la.setObjectName(u"nc_bottom_spindle_speed_la")

        self.gridLayout_7.addWidget(self.nc_bottom_spindle_speed_la, 4, 0, 1, 1)

        self.nc_bottom_tool_diameter_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_tool_diameter_dsb.setObjectName(u"nc_bottom_tool_diameter_dsb")
        self.nc_bottom_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_tool_diameter_dsb, 0, 1, 1, 1)

        self.nc_bottom_overlap_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_overlap_dsb.setObjectName(u"nc_bottom_overlap_dsb")
        self.nc_bottom_overlap_dsb.setDecimals(1)
        self.nc_bottom_overlap_dsb.setMinimum(0.100000000000000)
        self.nc_bottom_overlap_dsb.setMaximum(1.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_overlap_dsb, 1, 1, 1, 1)

        self.nc_bottom_cut_z_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_cut_z_dsb.setObjectName(u"nc_bottom_cut_z_dsb")
        self.nc_bottom_cut_z_dsb.setDecimals(2)
        self.nc_bottom_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.nc_bottom_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_cut_z_dsb, 2, 1, 1, 1)

        self.nc_bottom_cut_z_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_cut_z_la.setObjectName(u"nc_bottom_cut_z_la")

        self.gridLayout_7.addWidget(self.nc_bottom_cut_z_la, 2, 0, 1, 1)

        self.nc_bottom_z_feed_rate_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_z_feed_rate_dsb.setObjectName(u"nc_bottom_z_feed_rate_dsb")
        self.nc_bottom_z_feed_rate_dsb.setDecimals(2)
        self.nc_bottom_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.nc_bottom_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_z_feed_rate_dsb, 7, 1, 1, 1)

        self.nc_bottom_overlap_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_overlap_la.setObjectName(u"nc_bottom_overlap_la")

        self.gridLayout_7.addWidget(self.nc_bottom_overlap_la, 1, 0, 1, 1)

        self.nc_bottom_tool_diameter_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_tool_diameter_la.setObjectName(u"nc_bottom_tool_diameter_la")

        self.gridLayout_7.addWidget(self.nc_bottom_tool_diameter_la, 0, 0, 1, 1)

        self.nc_bottom_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.nc_bottom_vertical_spacer, 8, 0, 1, 2)

        self.nc_bottom_spindle_speed_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_spindle_speed_dsb.setObjectName(u"nc_bottom_spindle_speed_dsb")
        self.nc_bottom_spindle_speed_dsb.setDecimals(2)
        self.nc_bottom_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.nc_bottom_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_spindle_speed_dsb, 4, 1, 1, 1)

        self.nc_bottom_travel_z_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_travel_z_dsb.setObjectName(u"nc_bottom_travel_z_dsb")
        self.nc_bottom_travel_z_dsb.setDecimals(2)
        self.nc_bottom_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.nc_bottom_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_travel_z_dsb, 3, 1, 1, 1)

        self.nc_bottom_xy_feed_rate_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_xy_feed_rate_dsb.setObjectName(u"nc_bottom_xy_feed_rate_dsb")
        self.nc_bottom_xy_feed_rate_dsb.setDecimals(2)
        self.nc_bottom_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.nc_bottom_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_xy_feed_rate_dsb, 6, 1, 1, 1)

        self.nc_bottom_z_feed_rate_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_z_feed_rate_la.setObjectName(u"nc_bottom_z_feed_rate_la")

        self.gridLayout_7.addWidget(self.nc_bottom_z_feed_rate_la, 7, 0, 1, 1)

        self.nc_bottom_xy_feed_rate_la = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_xy_feed_rate_la.setObjectName(u"nc_bottom_xy_feed_rate_la")

        self.gridLayout_7.addWidget(self.nc_bottom_xy_feed_rate_la, 6, 0, 1, 1)

        self.jobs_sw.addWidget(self.nc_area_bottom_page)

        self.verticalLayout_8.addWidget(self.jobs_sw)

        self.prepare_widget.addTab(self.create_job_tab, "")

        self.verticalLayout_2.addWidget(self.prepare_widget)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.viewCanvasWidget = VispyCanvas(self.view_tab)
        self.viewCanvasWidget.setObjectName(u"viewCanvasWidget")
        sizePolicy.setHeightForWidth(self.viewCanvasWidget.sizePolicy().hasHeightForWidth())
        self.viewCanvasWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_9.addWidget(self.viewCanvasWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_3 = QPushButton(self.view_tab)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.view_tab)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_6.addLayout(self.verticalLayout_9)


        self.horizontalLayout_8.addLayout(self.horizontalLayout_6)

        self.main_tab_widget.addTab(self.view_tab, "")
        self.control_tab = QWidget()
        self.control_tab.setObjectName(u"control_tab")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.control_tab.sizePolicy().hasHeightForWidth())
        self.control_tab.setSizePolicy(sizePolicy4)
        self.control_tab.setFont(font)
        self.horizontalLayout_5 = QHBoxLayout(self.control_tab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ctrl_tab_widget = QTabWidget(self.control_tab)
        self.ctrl_tab_widget.setObjectName(u"ctrl_tab_widget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ctrl_tab_widget.sizePolicy().hasHeightForWidth())
        self.ctrl_tab_widget.setSizePolicy(sizePolicy5)
        self.gcode_load = QWidget()
        self.gcode_load.setObjectName(u"gcode_load")
        sizePolicy3.setHeightForWidth(self.gcode_load.sizePolicy().hasHeightForWidth())
        self.gcode_load.setSizePolicy(sizePolicy3)
        self.verticalLayout_11 = QVBoxLayout(self.gcode_load)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gcode_tw = QTableWidget(self.gcode_load)
        if (self.gcode_tw.columnCount() < 2):
            self.gcode_tw.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.gcode_tw.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.gcode_tw.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.gcode_tw.setObjectName(u"gcode_tw")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.gcode_tw.sizePolicy().hasHeightForWidth())
        self.gcode_tw.setSizePolicy(sizePolicy6)
        self.gcode_tw.setMinimumSize(QSize(320, 0))
        self.gcode_tw.setMaximumSize(QSize(320, 16777215))
        self.gcode_tw.setFrameShape(QFrame.NoFrame)
        self.gcode_tw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gcode_tw.setSelectionMode(QAbstractItemView.MultiSelection)
        self.gcode_tw.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.gcode_tw.setShowGrid(False)
        self.gcode_tw.setColumnCount(2)
        self.gcode_tw.horizontalHeader().setCascadingSectionResizes(True)

        self.verticalLayout_11.addWidget(self.gcode_tw)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.upload_temp_tb = QToolButton(self.gcode_load)
        self.upload_temp_tb.setObjectName(u"upload_temp_tb")
        self.upload_temp_tb.setMinimumSize(QSize(50, 50))
        icon1 = QIcon()
        icon1.addFile(u":/resources/resources/icons/white-upload-file.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/resources/resources/icons/white-upload-file.svg", QSize(), QIcon.Normal, QIcon.On)
        icon1.addFile(u":/resources/resources/icons/gray-upload-file.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon1.addFile(u":/resources/resources/icons/gray-upload-file.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.upload_temp_tb.setIcon(icon1)

        self.horizontalLayout_10.addWidget(self.upload_temp_tb)

        self.open_gcode_tb = QToolButton(self.gcode_load)
        self.open_gcode_tb.setObjectName(u"open_gcode_tb")
        sizePolicy3.setHeightForWidth(self.open_gcode_tb.sizePolicy().hasHeightForWidth())
        self.open_gcode_tb.setSizePolicy(sizePolicy3)
        self.open_gcode_tb.setMinimumSize(QSize(50, 50))
        icon2 = QIcon()
        icon2.addFile(u":/resources/resources/icons/white-open-folder.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_gcode_tb.setIcon(icon2)

        self.horizontalLayout_10.addWidget(self.open_gcode_tb)

        self.remove_gcode_tb = QToolButton(self.gcode_load)
        self.remove_gcode_tb.setObjectName(u"remove_gcode_tb")
        self.remove_gcode_tb.setMinimumSize(QSize(50, 50))
        icon3 = QIcon()
        icon3.addFile(u":/resources/resources/icons/white-delete.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_gcode_tb.setIcon(icon3)

        self.horizontalLayout_10.addWidget(self.remove_gcode_tb)


        self.verticalLayout_11.addLayout(self.horizontalLayout_10)

        self.ctrl_tab_widget.addTab(self.gcode_load, "")
        self.sender_tab = QWidget()
        self.sender_tab.setObjectName(u"sender_tab")
        sizePolicy3.setHeightForWidth(self.sender_tab.sizePolicy().hasHeightForWidth())
        self.sender_tab.setSizePolicy(sizePolicy3)
        self.verticalLayout_10 = QVBoxLayout(self.sender_tab)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.controlsVerticalLayout = QVBoxLayout()
        self.controlsVerticalLayout.setObjectName(u"controlsVerticalLayout")
        self.controlsVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.line_4 = QFrame(self.sender_tab)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.controlsVerticalLayout.addWidget(self.line_4)

        self.droGridLayout = QGridLayout()
        self.droGridLayout.setObjectName(u"droGridLayout")
        self.droGridLayout.setHorizontalSpacing(0)
        self.droGridLayout.setVerticalSpacing(2)
        self.droGridLayout.setContentsMargins(0, 0, 0, 0)
        self.zero_xy_pb = QPushButton(self.sender_tab)
        self.zero_xy_pb.setObjectName(u"zero_xy_pb")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.zero_xy_pb.sizePolicy().hasHeightForWidth())
        self.zero_xy_pb.setSizePolicy(sizePolicy7)
        self.zero_xy_pb.setMinimumSize(QSize(0, 20))
        self.zero_xy_pb.setMaximumSize(QSize(16777215, 23))
        self.zero_xy_pb.setFont(font)

        self.droGridLayout.addWidget(self.zero_xy_pb, 3, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.zero_y_pb = QPushButton(self.sender_tab)
        self.zero_y_pb.setObjectName(u"zero_y_pb")
        sizePolicy7.setHeightForWidth(self.zero_y_pb.sizePolicy().hasHeightForWidth())
        self.zero_y_pb.setSizePolicy(sizePolicy7)
        self.zero_y_pb.setMinimumSize(QSize(0, 20))
        self.zero_y_pb.setMaximumSize(QSize(16777215, 23))
        self.zero_y_pb.setFont(font)

        self.droGridLayout.addWidget(self.zero_y_pb, 3, 2, 1, 1, Qt.AlignHCenter)

        self.z_axis_l = QLabel(self.sender_tab)
        self.z_axis_l.setObjectName(u"z_axis_l")
        sizePolicy7.setHeightForWidth(self.z_axis_l.sizePolicy().hasHeightForWidth())
        self.z_axis_l.setSizePolicy(sizePolicy7)
        self.z_axis_l.setMinimumSize(QSize(0, 12))
        self.z_axis_l.setMaximumSize(QSize(16777215, 13))
        self.z_axis_l.setFont(font)
        self.z_axis_l.setLayoutDirection(Qt.LeftToRight)
        self.z_axis_l.setFrameShape(QFrame.NoFrame)
        self.z_axis_l.setFrameShadow(QFrame.Plain)
        self.z_axis_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.z_axis_l, 0, 3, 1, 1, Qt.AlignHCenter)

        self.wpos_y_l = QLabel(self.sender_tab)
        self.wpos_y_l.setObjectName(u"wpos_y_l")
        sizePolicy7.setHeightForWidth(self.wpos_y_l.sizePolicy().hasHeightForWidth())
        self.wpos_y_l.setSizePolicy(sizePolicy7)
        self.wpos_y_l.setMinimumSize(QSize(0, 12))
        self.wpos_y_l.setMaximumSize(QSize(16777215, 13))
        self.wpos_y_l.setLayoutDirection(Qt.LeftToRight)
        self.wpos_y_l.setFrameShape(QFrame.NoFrame)
        self.wpos_y_l.setFrameShadow(QFrame.Plain)
        self.wpos_y_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.wpos_y_l, 2, 2, 1, 1, Qt.AlignHCenter)

        self.wpos_l = QLabel(self.sender_tab)
        self.wpos_l.setObjectName(u"wpos_l")
        sizePolicy7.setHeightForWidth(self.wpos_l.sizePolicy().hasHeightForWidth())
        self.wpos_l.setSizePolicy(sizePolicy7)
        self.wpos_l.setMinimumSize(QSize(0, 12))
        self.wpos_l.setMaximumSize(QSize(16777215, 13))
        self.wpos_l.setFont(font)
        self.wpos_l.setLayoutDirection(Qt.LeftToRight)
        self.wpos_l.setFrameShape(QFrame.NoFrame)
        self.wpos_l.setFrameShadow(QFrame.Plain)
        self.wpos_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.wpos_l, 2, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.zero_z_pb = QPushButton(self.sender_tab)
        self.zero_z_pb.setObjectName(u"zero_z_pb")
        sizePolicy7.setHeightForWidth(self.zero_z_pb.sizePolicy().hasHeightForWidth())
        self.zero_z_pb.setSizePolicy(sizePolicy7)
        self.zero_z_pb.setMinimumSize(QSize(0, 20))
        self.zero_z_pb.setMaximumSize(QSize(16777215, 23))
        self.zero_z_pb.setFont(font)

        self.droGridLayout.addWidget(self.zero_z_pb, 3, 3, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.mpos_y_l = QLabel(self.sender_tab)
        self.mpos_y_l.setObjectName(u"mpos_y_l")
        sizePolicy7.setHeightForWidth(self.mpos_y_l.sizePolicy().hasHeightForWidth())
        self.mpos_y_l.setSizePolicy(sizePolicy7)
        self.mpos_y_l.setMinimumSize(QSize(0, 12))
        self.mpos_y_l.setMaximumSize(QSize(16777215, 13))
        self.mpos_y_l.setLayoutDirection(Qt.LeftToRight)
        self.mpos_y_l.setFrameShape(QFrame.NoFrame)
        self.mpos_y_l.setFrameShadow(QFrame.Plain)
        self.mpos_y_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_y_l, 1, 2, 1, 1, Qt.AlignHCenter)

        self.mpos_z_l = QLabel(self.sender_tab)
        self.mpos_z_l.setObjectName(u"mpos_z_l")
        sizePolicy7.setHeightForWidth(self.mpos_z_l.sizePolicy().hasHeightForWidth())
        self.mpos_z_l.setSizePolicy(sizePolicy7)
        self.mpos_z_l.setMinimumSize(QSize(0, 12))
        self.mpos_z_l.setMaximumSize(QSize(16777215, 13))
        self.mpos_z_l.setLayoutDirection(Qt.LeftToRight)
        self.mpos_z_l.setFrameShape(QFrame.NoFrame)
        self.mpos_z_l.setFrameShadow(QFrame.Plain)
        self.mpos_z_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_z_l, 1, 3, 1, 1, Qt.AlignHCenter)

        self.x_axis_l = QLabel(self.sender_tab)
        self.x_axis_l.setObjectName(u"x_axis_l")
        sizePolicy7.setHeightForWidth(self.x_axis_l.sizePolicy().hasHeightForWidth())
        self.x_axis_l.setSizePolicy(sizePolicy7)
        self.x_axis_l.setMinimumSize(QSize(0, 12))
        self.x_axis_l.setMaximumSize(QSize(16777215, 13))
        self.x_axis_l.setFont(font)
        self.x_axis_l.setLayoutDirection(Qt.LeftToRight)
        self.x_axis_l.setFrameShape(QFrame.NoFrame)
        self.x_axis_l.setFrameShadow(QFrame.Plain)
        self.x_axis_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.x_axis_l, 0, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.wpos_x_l = QLabel(self.sender_tab)
        self.wpos_x_l.setObjectName(u"wpos_x_l")
        sizePolicy7.setHeightForWidth(self.wpos_x_l.sizePolicy().hasHeightForWidth())
        self.wpos_x_l.setSizePolicy(sizePolicy7)
        self.wpos_x_l.setMinimumSize(QSize(0, 12))
        self.wpos_x_l.setMaximumSize(QSize(16777215, 13))
        self.wpos_x_l.setLayoutDirection(Qt.LeftToRight)
        self.wpos_x_l.setFrameShape(QFrame.NoFrame)
        self.wpos_x_l.setFrameShadow(QFrame.Plain)
        self.wpos_x_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.wpos_x_l, 2, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.axis_l = QLabel(self.sender_tab)
        self.axis_l.setObjectName(u"axis_l")
        sizePolicy7.setHeightForWidth(self.axis_l.sizePolicy().hasHeightForWidth())
        self.axis_l.setSizePolicy(sizePolicy7)
        self.axis_l.setMinimumSize(QSize(0, 12))
        self.axis_l.setMaximumSize(QSize(16777215, 13))
        self.axis_l.setFont(font)
        self.axis_l.setLayoutDirection(Qt.LeftToRight)
        self.axis_l.setFrameShape(QFrame.NoFrame)
        self.axis_l.setFrameShadow(QFrame.Plain)
        self.axis_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.axis_l, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.mpos_l = QLabel(self.sender_tab)
        self.mpos_l.setObjectName(u"mpos_l")
        sizePolicy7.setHeightForWidth(self.mpos_l.sizePolicy().hasHeightForWidth())
        self.mpos_l.setSizePolicy(sizePolicy7)
        self.mpos_l.setMinimumSize(QSize(0, 12))
        self.mpos_l.setMaximumSize(QSize(16777215, 13))
        self.mpos_l.setFont(font)
        self.mpos_l.setLayoutDirection(Qt.LeftToRight)
        self.mpos_l.setFrameShape(QFrame.NoFrame)
        self.mpos_l.setFrameShadow(QFrame.Plain)
        self.mpos_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_l, 1, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.wpos_z_l = QLabel(self.sender_tab)
        self.wpos_z_l.setObjectName(u"wpos_z_l")
        sizePolicy7.setHeightForWidth(self.wpos_z_l.sizePolicy().hasHeightForWidth())
        self.wpos_z_l.setSizePolicy(sizePolicy7)
        self.wpos_z_l.setMinimumSize(QSize(0, 12))
        self.wpos_z_l.setMaximumSize(QSize(16777215, 13))
        self.wpos_z_l.setLayoutDirection(Qt.LeftToRight)
        self.wpos_z_l.setFrameShape(QFrame.NoFrame)
        self.wpos_z_l.setFrameShadow(QFrame.Plain)
        self.wpos_z_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.wpos_z_l, 2, 3, 1, 1, Qt.AlignHCenter)

        self.zero_x_pb = QPushButton(self.sender_tab)
        self.zero_x_pb.setObjectName(u"zero_x_pb")
        sizePolicy7.setHeightForWidth(self.zero_x_pb.sizePolicy().hasHeightForWidth())
        self.zero_x_pb.setSizePolicy(sizePolicy7)
        self.zero_x_pb.setMinimumSize(QSize(0, 20))
        self.zero_x_pb.setMaximumSize(QSize(16777215, 23))
        self.zero_x_pb.setFont(font)

        self.droGridLayout.addWidget(self.zero_x_pb, 3, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.y_axis_l = QLabel(self.sender_tab)
        self.y_axis_l.setObjectName(u"y_axis_l")
        sizePolicy7.setHeightForWidth(self.y_axis_l.sizePolicy().hasHeightForWidth())
        self.y_axis_l.setSizePolicy(sizePolicy7)
        self.y_axis_l.setMinimumSize(QSize(0, 12))
        self.y_axis_l.setMaximumSize(QSize(16777215, 13))
        self.y_axis_l.setFont(font)
        self.y_axis_l.setLayoutDirection(Qt.LeftToRight)
        self.y_axis_l.setFrameShape(QFrame.NoFrame)
        self.y_axis_l.setFrameShadow(QFrame.Plain)
        self.y_axis_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.y_axis_l, 0, 2, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.mpos_x_l = QLabel(self.sender_tab)
        self.mpos_x_l.setObjectName(u"mpos_x_l")
        sizePolicy7.setHeightForWidth(self.mpos_x_l.sizePolicy().hasHeightForWidth())
        self.mpos_x_l.setSizePolicy(sizePolicy7)
        self.mpos_x_l.setMinimumSize(QSize(0, 12))
        self.mpos_x_l.setMaximumSize(QSize(16777215, 13))
        self.mpos_x_l.setLayoutDirection(Qt.LeftToRight)
        self.mpos_x_l.setFrameShape(QFrame.NoFrame)
        self.mpos_x_l.setFrameShadow(QFrame.Plain)
        self.mpos_x_l.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_x_l, 1, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)


        self.controlsVerticalLayout.addLayout(self.droGridLayout)

        self.line_3 = QFrame(self.sender_tab)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.controlsVerticalLayout.addWidget(self.line_3)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.probe_pb = QPushButton(self.sender_tab)
        self.probe_pb.setObjectName(u"probe_pb")
        sizePolicy7.setHeightForWidth(self.probe_pb.sizePolicy().hasHeightForWidth())
        self.probe_pb.setSizePolicy(sizePolicy7)
        self.probe_pb.setMinimumSize(QSize(0, 20))
        self.probe_pb.setMaximumSize(QSize(16777215, 23))

        self.gridLayout_10.addWidget(self.probe_pb, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.get_bbox_pb = QPushButton(self.sender_tab)
        self.get_bbox_pb.setObjectName(u"get_bbox_pb")
        sizePolicy7.setHeightForWidth(self.get_bbox_pb.sizePolicy().hasHeightForWidth())
        self.get_bbox_pb.setSizePolicy(sizePolicy7)
        self.get_bbox_pb.setMinimumSize(QSize(0, 20))
        self.get_bbox_pb.setMaximumSize(QSize(16777215, 23))
        self.get_bbox_pb.setFont(font)

        self.gridLayout_10.addWidget(self.get_bbox_pb, 0, 2, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.ABL_pb = QPushButton(self.sender_tab)
        self.ABL_pb.setObjectName(u"ABL_pb")
        sizePolicy7.setHeightForWidth(self.ABL_pb.sizePolicy().hasHeightForWidth())
        self.ABL_pb.setSizePolicy(sizePolicy7)
        self.ABL_pb.setMinimumSize(QSize(0, 20))
        self.ABL_pb.setMaximumSize(QSize(16777215, 23))
        self.ABL_pb.setFont(font)

        self.horizontalLayout_11.addWidget(self.ABL_pb)

        self.abl_active_chb = QCheckBox(self.sender_tab)
        self.abl_active_chb.setObjectName(u"abl_active_chb")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.abl_active_chb.sizePolicy().hasHeightForWidth())
        self.abl_active_chb.setSizePolicy(sizePolicy8)
        self.abl_active_chb.setMinimumSize(QSize(0, 20))
        self.abl_active_chb.setMaximumSize(QSize(16777215, 23))
        self.abl_active_chb.setChecked(True)

        self.horizontalLayout_11.addWidget(self.abl_active_chb)


        self.gridLayout_10.addLayout(self.horizontalLayout_11, 0, 1, 1, 1)


        self.controlsVerticalLayout.addLayout(self.gridLayout_10)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(0)
        self.label_6 = QLabel(self.sender_tab)
        self.label_6.setObjectName(u"label_6")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy9)
        self.label_6.setMinimumSize(QSize(0, 20))
        self.label_6.setMaximumSize(QSize(16777215, 23))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_6, 0, 1, 1, 1)

        self.label_7 = QLabel(self.sender_tab)
        self.label_7.setObjectName(u"label_7")
        sizePolicy9.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy9)
        self.label_7.setMinimumSize(QSize(0, 20))
        self.label_7.setMaximumSize(QSize(16777215, 23))
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_7, 0, 2, 1, 1)

        self.label_8 = QLabel(self.sender_tab)
        self.label_8.setObjectName(u"label_8")
        sizePolicy9.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy9)
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setMaximumSize(QSize(16777215, 23))
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_8, 0, 3, 1, 1)

        self.label_9 = QLabel(self.sender_tab)
        self.label_9.setObjectName(u"label_9")
        sizePolicy9.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy9)
        self.label_9.setMinimumSize(QSize(0, 20))
        self.label_9.setMaximumSize(QSize(16777215, 23))
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_9, 0, 4, 1, 1)

        self.label_10 = QLabel(self.sender_tab)
        self.label_10.setObjectName(u"label_10")
        sizePolicy9.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy9)
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setMaximumSize(QSize(16777215, 23))
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_10, 1, 0, 1, 1)

        self.x_min_dsb = QDoubleSpinBox(self.sender_tab)
        self.x_min_dsb.setObjectName(u"x_min_dsb")
        sizePolicy8.setHeightForWidth(self.x_min_dsb.sizePolicy().hasHeightForWidth())
        self.x_min_dsb.setSizePolicy(sizePolicy8)
        self.x_min_dsb.setMinimumSize(QSize(0, 20))
        self.x_min_dsb.setMaximumSize(QSize(16777215, 23))
        self.x_min_dsb.setAlignment(Qt.AlignCenter)
        self.x_min_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.x_min_dsb.setMinimum(-1000.000000000000000)
        self.x_min_dsb.setMaximum(1000.000000000000000)

        self.gridLayout_11.addWidget(self.x_min_dsb, 1, 1, 1, 1)

        self.x_max_dsb = QDoubleSpinBox(self.sender_tab)
        self.x_max_dsb.setObjectName(u"x_max_dsb")
        sizePolicy8.setHeightForWidth(self.x_max_dsb.sizePolicy().hasHeightForWidth())
        self.x_max_dsb.setSizePolicy(sizePolicy8)
        self.x_max_dsb.setMinimumSize(QSize(0, 20))
        self.x_max_dsb.setMaximumSize(QSize(16777215, 23))
        self.x_max_dsb.setAlignment(Qt.AlignCenter)
        self.x_max_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.x_max_dsb.setMinimum(-1000.000000000000000)
        self.x_max_dsb.setMaximum(1000.000000000000000)

        self.gridLayout_11.addWidget(self.x_max_dsb, 1, 2, 1, 1)

        self.x_step_dsb = QDoubleSpinBox(self.sender_tab)
        self.x_step_dsb.setObjectName(u"x_step_dsb")
        self.x_step_dsb.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.x_step_dsb.sizePolicy().hasHeightForWidth())
        self.x_step_dsb.setSizePolicy(sizePolicy8)
        self.x_step_dsb.setMinimumSize(QSize(0, 20))
        self.x_step_dsb.setMaximumSize(QSize(16777215, 23))
        self.x_step_dsb.setAlignment(Qt.AlignCenter)
        self.x_step_dsb.setReadOnly(True)
        self.x_step_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_11.addWidget(self.x_step_dsb, 1, 3, 1, 1)

        self.x_num_step_sb = QSpinBox(self.sender_tab)
        self.x_num_step_sb.setObjectName(u"x_num_step_sb")
        sizePolicy8.setHeightForWidth(self.x_num_step_sb.sizePolicy().hasHeightForWidth())
        self.x_num_step_sb.setSizePolicy(sizePolicy8)
        self.x_num_step_sb.setMinimumSize(QSize(0, 20))
        self.x_num_step_sb.setMaximumSize(QSize(16777215, 23))
        self.x_num_step_sb.setAlignment(Qt.AlignCenter)
        self.x_num_step_sb.setMinimum(1)

        self.gridLayout_11.addWidget(self.x_num_step_sb, 1, 4, 1, 1)

        self.label_11 = QLabel(self.sender_tab)
        self.label_11.setObjectName(u"label_11")
        sizePolicy9.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy9)
        self.label_11.setMinimumSize(QSize(0, 20))
        self.label_11.setMaximumSize(QSize(16777215, 23))
        self.label_11.setFont(font)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_11, 2, 0, 1, 1)

        self.y_min_dsb = QDoubleSpinBox(self.sender_tab)
        self.y_min_dsb.setObjectName(u"y_min_dsb")
        sizePolicy8.setHeightForWidth(self.y_min_dsb.sizePolicy().hasHeightForWidth())
        self.y_min_dsb.setSizePolicy(sizePolicy8)
        self.y_min_dsb.setMinimumSize(QSize(0, 20))
        self.y_min_dsb.setMaximumSize(QSize(16777215, 23))
        self.y_min_dsb.setAlignment(Qt.AlignCenter)
        self.y_min_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.y_min_dsb.setMinimum(-1000.000000000000000)
        self.y_min_dsb.setMaximum(1000.000000000000000)

        self.gridLayout_11.addWidget(self.y_min_dsb, 2, 1, 1, 1)

        self.y_max_dsb = QDoubleSpinBox(self.sender_tab)
        self.y_max_dsb.setObjectName(u"y_max_dsb")
        sizePolicy8.setHeightForWidth(self.y_max_dsb.sizePolicy().hasHeightForWidth())
        self.y_max_dsb.setSizePolicy(sizePolicy8)
        self.y_max_dsb.setMinimumSize(QSize(0, 20))
        self.y_max_dsb.setMaximumSize(QSize(16777215, 23))
        self.y_max_dsb.setAlignment(Qt.AlignCenter)
        self.y_max_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.y_max_dsb.setMinimum(-1000.000000000000000)
        self.y_max_dsb.setMaximum(1000.000000000000000)

        self.gridLayout_11.addWidget(self.y_max_dsb, 2, 2, 1, 1)

        self.y_step_dsb = QDoubleSpinBox(self.sender_tab)
        self.y_step_dsb.setObjectName(u"y_step_dsb")
        self.y_step_dsb.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.y_step_dsb.sizePolicy().hasHeightForWidth())
        self.y_step_dsb.setSizePolicy(sizePolicy8)
        self.y_step_dsb.setMinimumSize(QSize(0, 20))
        self.y_step_dsb.setMaximumSize(QSize(16777215, 23))
        self.y_step_dsb.setAlignment(Qt.AlignCenter)
        self.y_step_dsb.setReadOnly(True)
        self.y_step_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_11.addWidget(self.y_step_dsb, 2, 3, 1, 1)

        self.y_num_step_sb = QSpinBox(self.sender_tab)
        self.y_num_step_sb.setObjectName(u"y_num_step_sb")
        sizePolicy8.setHeightForWidth(self.y_num_step_sb.sizePolicy().hasHeightForWidth())
        self.y_num_step_sb.setSizePolicy(sizePolicy8)
        self.y_num_step_sb.setMinimumSize(QSize(0, 20))
        self.y_num_step_sb.setMaximumSize(QSize(16777215, 23))
        self.y_num_step_sb.setAlignment(Qt.AlignCenter)
        self.y_num_step_sb.setMinimum(1)

        self.gridLayout_11.addWidget(self.y_num_step_sb, 2, 4, 1, 1)

        self.label_12 = QLabel(self.sender_tab)
        self.label_12.setObjectName(u"label_12")
        sizePolicy9.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy9)
        self.label_12.setMinimumSize(QSize(0, 20))
        self.label_12.setMaximumSize(QSize(16777215, 23))
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_12, 3, 0, 1, 1)

        self.z_min_dsb = QDoubleSpinBox(self.sender_tab)
        self.z_min_dsb.setObjectName(u"z_min_dsb")
        sizePolicy8.setHeightForWidth(self.z_min_dsb.sizePolicy().hasHeightForWidth())
        self.z_min_dsb.setSizePolicy(sizePolicy8)
        self.z_min_dsb.setMinimumSize(QSize(0, 20))
        self.z_min_dsb.setMaximumSize(QSize(16777215, 23))
        self.z_min_dsb.setAlignment(Qt.AlignCenter)
        self.z_min_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.z_min_dsb.setMinimum(-1000.000000000000000)
        self.z_min_dsb.setMaximum(1000.000000000000000)

        self.gridLayout_11.addWidget(self.z_min_dsb, 3, 1, 1, 1)

        self.z_max_dsb = QDoubleSpinBox(self.sender_tab)
        self.z_max_dsb.setObjectName(u"z_max_dsb")
        sizePolicy8.setHeightForWidth(self.z_max_dsb.sizePolicy().hasHeightForWidth())
        self.z_max_dsb.setSizePolicy(sizePolicy8)
        self.z_max_dsb.setMinimumSize(QSize(0, 20))
        self.z_max_dsb.setMaximumSize(QSize(16777215, 23))
        self.z_max_dsb.setAlignment(Qt.AlignCenter)
        self.z_max_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.z_max_dsb.setMinimum(-1000.000000000000000)
        self.z_max_dsb.setMaximum(1000.000000000000000)

        self.gridLayout_11.addWidget(self.z_max_dsb, 3, 2, 1, 1)


        self.controlsVerticalLayout.addLayout(self.gridLayout_11)

        self.line = QFrame(self.sender_tab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.controlsVerticalLayout.addWidget(self.line)

        self.jog_layout = QGridLayout()
        self.jog_layout.setObjectName(u"jog_layout")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.z_plus_pb = QPushButton(self.sender_tab)
        self.z_plus_pb.setObjectName(u"z_plus_pb")
        sizePolicy3.setHeightForWidth(self.z_plus_pb.sizePolicy().hasHeightForWidth())
        self.z_plus_pb.setSizePolicy(sizePolicy3)
        self.z_plus_pb.setMinimumSize(QSize(0, 24))
        self.z_plus_pb.setMaximumSize(QSize(100, 16777215))
        icon4 = QIcon()
        icon4.addFile(u":/resources/resources/icons/white_north_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.z_plus_pb.setIcon(icon4)

        self.gridLayout_17.addWidget(self.z_plus_pb, 0, 0, 1, 1)

        self.z_minus_pb = QPushButton(self.sender_tab)
        self.z_minus_pb.setObjectName(u"z_minus_pb")
        sizePolicy3.setHeightForWidth(self.z_minus_pb.sizePolicy().hasHeightForWidth())
        self.z_minus_pb.setSizePolicy(sizePolicy3)
        self.z_minus_pb.setMinimumSize(QSize(0, 24))
        self.z_minus_pb.setMaximumSize(QSize(100, 16777215))
        icon5 = QIcon()
        icon5.addFile(u":/resources/resources/icons/white_south_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.z_minus_pb.setIcon(icon5)

        self.gridLayout_17.addWidget(self.z_minus_pb, 1, 0, 1, 1)


        self.jog_layout.addLayout(self.gridLayout_17, 2, 0, 1, 1)

        self.gridLayoutDirections_3 = QGridLayout()
        self.gridLayoutDirections_3.setObjectName(u"gridLayoutDirections_3")
        self.gridLayoutDirections_3.setContentsMargins(0, 0, 0, 0)
        self.xYMinusPlusButton = QToolButton(self.sender_tab)
        self.xYMinusPlusButton.setObjectName(u"xYMinusPlusButton")
        sizePolicy3.setHeightForWidth(self.xYMinusPlusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusPlusButton.setSizePolicy(sizePolicy3)
        self.xYMinusPlusButton.setMinimumSize(QSize(0, 22))
        self.xYMinusPlusButton.setMaximumSize(QSize(50, 16777215))
        icon6 = QIcon()
        icon6.addFile(u":/resources/resources/icons/white_north_west_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.xYMinusPlusButton.setIcon(icon6)

        self.gridLayoutDirections_3.addWidget(self.xYMinusPlusButton, 0, 0, 1, 1)

        self.xYPlusMinuButton = QToolButton(self.sender_tab)
        self.xYPlusMinuButton.setObjectName(u"xYPlusMinuButton")
        sizePolicy3.setHeightForWidth(self.xYPlusMinuButton.sizePolicy().hasHeightForWidth())
        self.xYPlusMinuButton.setSizePolicy(sizePolicy3)
        self.xYPlusMinuButton.setMinimumSize(QSize(0, 22))
        self.xYPlusMinuButton.setMaximumSize(QSize(50, 16777215))
        icon7 = QIcon()
        icon7.addFile(u":/resources/resources/icons/white_south_east_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.xYPlusMinuButton.setIcon(icon7)

        self.gridLayoutDirections_3.addWidget(self.xYPlusMinuButton, 2, 2, 1, 1)

        self.xMinusButton = QToolButton(self.sender_tab)
        self.xMinusButton.setObjectName(u"xMinusButton")
        sizePolicy3.setHeightForWidth(self.xMinusButton.sizePolicy().hasHeightForWidth())
        self.xMinusButton.setSizePolicy(sizePolicy3)
        self.xMinusButton.setMinimumSize(QSize(0, 22))
        self.xMinusButton.setMaximumSize(QSize(50, 16777215))
        icon8 = QIcon()
        icon8.addFile(u":/resources/resources/icons/white_west_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.xMinusButton.setIcon(icon8)

        self.gridLayoutDirections_3.addWidget(self.xMinusButton, 1, 0, 1, 1)

        self.xYMinusButton = QToolButton(self.sender_tab)
        self.xYMinusButton.setObjectName(u"xYMinusButton")
        sizePolicy3.setHeightForWidth(self.xYMinusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusButton.setSizePolicy(sizePolicy3)
        self.xYMinusButton.setMinimumSize(QSize(0, 22))
        self.xYMinusButton.setMaximumSize(QSize(50, 16777215))
        icon9 = QIcon()
        icon9.addFile(u":/resources/resources/icons/white_south_west_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.xYMinusButton.setIcon(icon9)

        self.gridLayoutDirections_3.addWidget(self.xYMinusButton, 2, 0, 1, 1)

        self.yPlusButton = QToolButton(self.sender_tab)
        self.yPlusButton.setObjectName(u"yPlusButton")
        sizePolicy3.setHeightForWidth(self.yPlusButton.sizePolicy().hasHeightForWidth())
        self.yPlusButton.setSizePolicy(sizePolicy3)
        self.yPlusButton.setMinimumSize(QSize(0, 22))
        self.yPlusButton.setMaximumSize(QSize(50, 16777215))
        self.yPlusButton.setIcon(icon4)

        self.gridLayoutDirections_3.addWidget(self.yPlusButton, 0, 1, 1, 1)

        self.center_tb = QToolButton(self.sender_tab)
        self.center_tb.setObjectName(u"center_tb")
        sizePolicy3.setHeightForWidth(self.center_tb.sizePolicy().hasHeightForWidth())
        self.center_tb.setSizePolicy(sizePolicy3)
        self.center_tb.setMinimumSize(QSize(0, 22))
        self.center_tb.setMaximumSize(QSize(50, 16777215))
        icon10 = QIcon()
        icon10.addFile(u":/resources/resources/icons/white_circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.center_tb.setIcon(icon10)

        self.gridLayoutDirections_3.addWidget(self.center_tb, 1, 1, 1, 1)

        self.yMinusButton = QToolButton(self.sender_tab)
        self.yMinusButton.setObjectName(u"yMinusButton")
        sizePolicy3.setHeightForWidth(self.yMinusButton.sizePolicy().hasHeightForWidth())
        self.yMinusButton.setSizePolicy(sizePolicy3)
        self.yMinusButton.setMinimumSize(QSize(0, 22))
        self.yMinusButton.setMaximumSize(QSize(50, 16777215))
        self.yMinusButton.setIcon(icon5)

        self.gridLayoutDirections_3.addWidget(self.yMinusButton, 2, 1, 1, 1)

        self.xYPlusButton = QToolButton(self.sender_tab)
        self.xYPlusButton.setObjectName(u"xYPlusButton")
        sizePolicy3.setHeightForWidth(self.xYPlusButton.sizePolicy().hasHeightForWidth())
        self.xYPlusButton.setSizePolicy(sizePolicy3)
        self.xYPlusButton.setMinimumSize(QSize(0, 22))
        self.xYPlusButton.setMaximumSize(QSize(50, 16777215))
        icon11 = QIcon()
        icon11.addFile(u":/resources/resources/icons/white_north_east_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.xYPlusButton.setIcon(icon11)

        self.gridLayoutDirections_3.addWidget(self.xYPlusButton, 0, 2, 1, 1)

        self.xPlusButton = QToolButton(self.sender_tab)
        self.xPlusButton.setObjectName(u"xPlusButton")
        sizePolicy3.setHeightForWidth(self.xPlusButton.sizePolicy().hasHeightForWidth())
        self.xPlusButton.setSizePolicy(sizePolicy3)
        self.xPlusButton.setMinimumSize(QSize(0, 22))
        self.xPlusButton.setMaximumSize(QSize(50, 16777215))
        icon12 = QIcon()
        icon12.addFile(u":/resources/resources/icons/white_east_arrow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.xPlusButton.setIcon(icon12)

        self.gridLayoutDirections_3.addWidget(self.xPlusButton, 1, 2, 1, 1)


        self.jog_layout.addLayout(self.gridLayoutDirections_3, 0, 0, 1, 1)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.z_jog_l_2 = QLabel(self.sender_tab)
        self.z_jog_l_2.setObjectName(u"z_jog_l_2")
        sizePolicy3.setHeightForWidth(self.z_jog_l_2.sizePolicy().hasHeightForWidth())
        self.z_jog_l_2.setSizePolicy(sizePolicy3)
        self.z_jog_l_2.setMinimumSize(QSize(0, 20))
        self.z_jog_l_2.setMaximumSize(QSize(16777215, 23))
        self.z_jog_l_2.setFont(font)
        self.z_jog_l_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.z_jog_l_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.z_step_cb = QComboBox(self.sender_tab)
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.addItem("")
        self.z_step_cb.setObjectName(u"z_step_cb")
        sizePolicy3.setHeightForWidth(self.z_step_cb.sizePolicy().hasHeightForWidth())
        self.z_step_cb.setSizePolicy(sizePolicy3)
        self.z_step_cb.setMinimumSize(QSize(75, 20))
        self.z_step_cb.setMaximumSize(QSize(75, 16777215))
        self.z_step_cb.setFont(font)

        self.horizontalLayout_14.addWidget(self.z_step_cb, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_15.addLayout(self.horizontalLayout_14)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.z_step_val_dsb = QDoubleSpinBox(self.sender_tab)
        self.z_step_val_dsb.setObjectName(u"z_step_val_dsb")
        self.z_step_val_dsb.setMinimumSize(QSize(70, 20))
        self.z_step_val_dsb.setMaximumSize(QSize(70, 16777215))
        self.z_step_val_dsb.setFont(font)
        self.z_step_val_dsb.setAlignment(Qt.AlignCenter)
        self.z_step_val_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.z_step_val_dsb.setMinimum(0.010000000000000)
        self.z_step_val_dsb.setMaximum(1000.000000000000000)
        self.z_step_val_dsb.setSingleStep(0.100000000000000)
        self.z_step_val_dsb.setValue(0.100000000000000)

        self.gridLayout_18.addWidget(self.z_step_val_dsb, 1, 1, 1, 1)

        self.z_mul_10_pb = QPushButton(self.sender_tab)
        self.z_mul_10_pb.setObjectName(u"z_mul_10_pb")
        sizePolicy3.setHeightForWidth(self.z_mul_10_pb.sizePolicy().hasHeightForWidth())
        self.z_mul_10_pb.setSizePolicy(sizePolicy3)
        self.z_mul_10_pb.setMinimumSize(QSize(0, 23))
        self.z_mul_10_pb.setMaximumSize(QSize(50, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setWeight(75)
        self.z_mul_10_pb.setFont(font1)
        self.z_mul_10_pb.setAutoRepeat(False)

        self.gridLayout_18.addWidget(self.z_mul_10_pb, 1, 2, 1, 1)

        self.z_div_10_pb = QPushButton(self.sender_tab)
        self.z_div_10_pb.setObjectName(u"z_div_10_pb")
        sizePolicy3.setHeightForWidth(self.z_div_10_pb.sizePolicy().hasHeightForWidth())
        self.z_div_10_pb.setSizePolicy(sizePolicy3)
        self.z_div_10_pb.setMinimumSize(QSize(0, 23))
        self.z_div_10_pb.setMaximumSize(QSize(50, 16777215))
        self.z_div_10_pb.setFont(font)
        self.z_div_10_pb.setAutoRepeat(False)

        self.gridLayout_18.addWidget(self.z_div_10_pb, 1, 0, 1, 1)

        self.z_minus_1_pb = QPushButton(self.sender_tab)
        self.z_minus_1_pb.setObjectName(u"z_minus_1_pb")
        sizePolicy3.setHeightForWidth(self.z_minus_1_pb.sizePolicy().hasHeightForWidth())
        self.z_minus_1_pb.setSizePolicy(sizePolicy3)
        self.z_minus_1_pb.setMinimumSize(QSize(70, 23))
        self.z_minus_1_pb.setMaximumSize(QSize(70, 16777215))
        self.z_minus_1_pb.setFont(font)
        self.z_minus_1_pb.setAutoRepeat(True)

        self.gridLayout_18.addWidget(self.z_minus_1_pb, 2, 1, 1, 1)

        self.z_plus_1_pb = QPushButton(self.sender_tab)
        self.z_plus_1_pb.setObjectName(u"z_plus_1_pb")
        sizePolicy3.setHeightForWidth(self.z_plus_1_pb.sizePolicy().hasHeightForWidth())
        self.z_plus_1_pb.setSizePolicy(sizePolicy3)
        self.z_plus_1_pb.setMinimumSize(QSize(70, 23))
        self.z_plus_1_pb.setMaximumSize(QSize(70, 16777215))
        self.z_plus_1_pb.setFont(font)
        self.z_plus_1_pb.setAutoRepeat(True)

        self.gridLayout_18.addWidget(self.z_plus_1_pb, 0, 1, 1, 1)


        self.verticalLayout_15.addLayout(self.gridLayout_18)


        self.jog_layout.addLayout(self.verticalLayout_15, 2, 1, 1, 1)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.xy_jog_l = QLabel(self.sender_tab)
        self.xy_jog_l.setObjectName(u"xy_jog_l")
        sizePolicy3.setHeightForWidth(self.xy_jog_l.sizePolicy().hasHeightForWidth())
        self.xy_jog_l.setSizePolicy(sizePolicy3)
        self.xy_jog_l.setMinimumSize(QSize(0, 0))
        self.xy_jog_l.setMaximumSize(QSize(16777215, 23))
        self.xy_jog_l.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.xy_jog_l, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.xy_step_cb = QComboBox(self.sender_tab)
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.addItem("")
        self.xy_step_cb.setObjectName(u"xy_step_cb")
        sizePolicy3.setHeightForWidth(self.xy_step_cb.sizePolicy().hasHeightForWidth())
        self.xy_step_cb.setSizePolicy(sizePolicy3)
        self.xy_step_cb.setMinimumSize(QSize(75, 0))
        self.xy_step_cb.setMaximumSize(QSize(75, 23))

        self.horizontalLayout_12.addWidget(self.xy_step_cb, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_14.addLayout(self.horizontalLayout_12)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.xy_plus_1_pb = QPushButton(self.sender_tab)
        self.xy_plus_1_pb.setObjectName(u"xy_plus_1_pb")
        sizePolicy3.setHeightForWidth(self.xy_plus_1_pb.sizePolicy().hasHeightForWidth())
        self.xy_plus_1_pb.setSizePolicy(sizePolicy3)
        self.xy_plus_1_pb.setMinimumSize(QSize(70, 20))
        self.xy_plus_1_pb.setMaximumSize(QSize(70, 23))
        self.xy_plus_1_pb.setFont(font)
        self.xy_plus_1_pb.setAutoRepeat(True)

        self.gridLayout_16.addWidget(self.xy_plus_1_pb, 0, 1, 1, 1)

        self.xy_div_10_pb = QPushButton(self.sender_tab)
        self.xy_div_10_pb.setObjectName(u"xy_div_10_pb")
        sizePolicy3.setHeightForWidth(self.xy_div_10_pb.sizePolicy().hasHeightForWidth())
        self.xy_div_10_pb.setSizePolicy(sizePolicy3)
        self.xy_div_10_pb.setMinimumSize(QSize(50, 23))
        self.xy_div_10_pb.setMaximumSize(QSize(50, 23))
        self.xy_div_10_pb.setFont(font)
        self.xy_div_10_pb.setAutoRepeat(False)

        self.gridLayout_16.addWidget(self.xy_div_10_pb, 1, 0, 1, 1)

        self.xy_step_val_dsb = QDoubleSpinBox(self.sender_tab)
        self.xy_step_val_dsb.setObjectName(u"xy_step_val_dsb")
        sizePolicy3.setHeightForWidth(self.xy_step_val_dsb.sizePolicy().hasHeightForWidth())
        self.xy_step_val_dsb.setSizePolicy(sizePolicy3)
        self.xy_step_val_dsb.setMinimumSize(QSize(70, 23))
        self.xy_step_val_dsb.setMaximumSize(QSize(70, 23))
        self.xy_step_val_dsb.setFont(font)
        self.xy_step_val_dsb.setAlignment(Qt.AlignCenter)
        self.xy_step_val_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.xy_step_val_dsb.setMinimum(0.010000000000000)
        self.xy_step_val_dsb.setMaximum(1000.000000000000000)
        self.xy_step_val_dsb.setSingleStep(0.100000000000000)
        self.xy_step_val_dsb.setValue(0.100000000000000)

        self.gridLayout_16.addWidget(self.xy_step_val_dsb, 1, 1, 1, 1)

        self.xy_mul_10_pb = QPushButton(self.sender_tab)
        self.xy_mul_10_pb.setObjectName(u"xy_mul_10_pb")
        sizePolicy3.setHeightForWidth(self.xy_mul_10_pb.sizePolicy().hasHeightForWidth())
        self.xy_mul_10_pb.setSizePolicy(sizePolicy3)
        self.xy_mul_10_pb.setMinimumSize(QSize(50, 23))
        self.xy_mul_10_pb.setMaximumSize(QSize(50, 23))
        self.xy_mul_10_pb.setFont(font1)
        self.xy_mul_10_pb.setAutoRepeat(False)

        self.gridLayout_16.addWidget(self.xy_mul_10_pb, 1, 2, 1, 1)

        self.xy_minus_1_pb = QPushButton(self.sender_tab)
        self.xy_minus_1_pb.setObjectName(u"xy_minus_1_pb")
        sizePolicy3.setHeightForWidth(self.xy_minus_1_pb.sizePolicy().hasHeightForWidth())
        self.xy_minus_1_pb.setSizePolicy(sizePolicy3)
        self.xy_minus_1_pb.setMinimumSize(QSize(70, 23))
        self.xy_minus_1_pb.setMaximumSize(QSize(70, 23))
        self.xy_minus_1_pb.setFont(font)
        self.xy_minus_1_pb.setAutoRepeat(True)

        self.gridLayout_16.addWidget(self.xy_minus_1_pb, 2, 1, 1, 1)


        self.verticalLayout_14.addLayout(self.gridLayout_16)


        self.jog_layout.addLayout(self.verticalLayout_14, 0, 1, 1, 1)

        self.line_2 = QFrame(self.sender_tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.jog_layout.addWidget(self.line_2, 1, 1, 1, 1)

        self.line_5 = QFrame(self.sender_tab)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.jog_layout.addWidget(self.line_5, 1, 0, 1, 1)


        self.controlsVerticalLayout.addLayout(self.jog_layout)

        self.terminalVerticalLayout = QVBoxLayout()
        self.terminalVerticalLayout.setObjectName(u"terminalVerticalLayout")
        self.serial_te = QTextEdit(self.sender_tab)
        self.serial_te.setObjectName(u"serial_te")
        self.serial_te.setEnabled(True)
        sizePolicy10 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.serial_te.sizePolicy().hasHeightForWidth())
        self.serial_te.setSizePolicy(sizePolicy10)
        self.serial_te.setMinimumSize(QSize(0, 40))
        self.serial_te.setFrameShadow(QFrame.Sunken)
        self.serial_te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.serial_te.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.terminalVerticalLayout.addWidget(self.serial_te)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.send_te = QLineEdit(self.sender_tab)
        self.send_te.setObjectName(u"send_te")

        self.horizontalLayout_2.addWidget(self.send_te)

        self.send_pb = QPushButton(self.sender_tab)
        self.send_pb.setObjectName(u"send_pb")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.send_pb.sizePolicy().hasHeightForWidth())
        self.send_pb.setSizePolicy(sizePolicy11)
        self.send_pb.setFont(font)

        self.horizontalLayout_2.addWidget(self.send_pb)


        self.terminalVerticalLayout.addLayout(self.horizontalLayout_2)

        self.connectVerticalLayout = QVBoxLayout()
        self.connectVerticalLayout.setSpacing(6)
        self.connectVerticalLayout.setObjectName(u"connectVerticalLayout")
        self.connectVerticalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serial_ports_cb = QComboBox(self.sender_tab)
        self.serial_ports_cb.setObjectName(u"serial_ports_cb")
        sizePolicy2.setHeightForWidth(self.serial_ports_cb.sizePolicy().hasHeightForWidth())
        self.serial_ports_cb.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.serial_ports_cb)

        self.serial_baud_cb = QComboBox(self.sender_tab)
        self.serial_baud_cb.setObjectName(u"serial_baud_cb")
        sizePolicy2.setHeightForWidth(self.serial_baud_cb.sizePolicy().hasHeightForWidth())
        self.serial_baud_cb.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.serial_baud_cb)

        self.refresh_pb = QPushButton(self.sender_tab)
        self.refresh_pb.setObjectName(u"refresh_pb")
        sizePolicy11.setHeightForWidth(self.refresh_pb.sizePolicy().hasHeightForWidth())
        self.refresh_pb.setSizePolicy(sizePolicy11)
        self.refresh_pb.setFont(font)
        self.refresh_pb.setCheckable(False)

        self.horizontalLayout.addWidget(self.refresh_pb)


        self.connectVerticalLayout.addLayout(self.horizontalLayout)


        self.terminalVerticalLayout.addLayout(self.connectVerticalLayout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.clear_terminal_pb = QPushButton(self.sender_tab)
        self.clear_terminal_pb.setObjectName(u"clear_terminal_pb")
        self.clear_terminal_pb.setEnabled(True)
        sizePolicy12 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.clear_terminal_pb.sizePolicy().hasHeightForWidth())
        self.clear_terminal_pb.setSizePolicy(sizePolicy12)
        self.clear_terminal_pb.setFont(font)

        self.horizontalLayout_9.addWidget(self.clear_terminal_pb)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)

        self.connect_pb = QPushButton(self.sender_tab)
        self.connect_pb.setObjectName(u"connect_pb")
        sizePolicy3.setHeightForWidth(self.connect_pb.sizePolicy().hasHeightForWidth())
        self.connect_pb.setSizePolicy(sizePolicy3)
        self.connect_pb.setFont(font)

        self.horizontalLayout_9.addWidget(self.connect_pb)


        self.terminalVerticalLayout.addLayout(self.horizontalLayout_9)


        self.controlsVerticalLayout.addLayout(self.terminalVerticalLayout)


        self.verticalLayout_10.addLayout(self.controlsVerticalLayout)

        self.ctrl_tab_widget.addTab(self.sender_tab, "")

        self.horizontalLayout_4.addWidget(self.ctrl_tab_widget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.controlCanvasWidget = VispyCanvas(self.control_tab)
        self.controlCanvasWidget.setObjectName(u"controlCanvasWidget")
        sizePolicy.setHeightForWidth(self.controlCanvasWidget.sizePolicy().hasHeightForWidth())
        self.controlCanvasWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.controlCanvasWidget)

        self.progressBar = QProgressBar(self.control_tab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalLayout_4.setStretch(1, 10)

        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.soft_reset_tb = QToolButton(self.control_tab)
        self.soft_reset_tb.setObjectName(u"soft_reset_tb")
        sizePolicy6.setHeightForWidth(self.soft_reset_tb.sizePolicy().hasHeightForWidth())
        self.soft_reset_tb.setSizePolicy(sizePolicy6)
        self.soft_reset_tb.setMinimumSize(QSize(120, 25))
        self.soft_reset_tb.setMaximumSize(QSize(120, 16777215))
        icon13 = QIcon()
        icon13.addFile(u":/resources/resources/icons/white-refresh.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon13.addFile(u":/resources/resources/icons/white-refresh.svg", QSize(), QIcon.Normal, QIcon.On)
        icon13.addFile(u":/resources/resources/icons/gray-refresh.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon13.addFile(u":/resources/resources/icons/gray-refresh.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.soft_reset_tb.setIcon(icon13)
        self.soft_reset_tb.setIconSize(QSize(64, 64))
        self.soft_reset_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.soft_reset_tb)

        self.status_l = QLabel(self.control_tab)
        self.status_l.setObjectName(u"status_l")
        sizePolicy6.setHeightForWidth(self.status_l.sizePolicy().hasHeightForWidth())
        self.status_l.setSizePolicy(sizePolicy6)
        self.status_l.setMinimumSize(QSize(120, 50))
        self.status_l.setMaximumSize(QSize(120, 16777215))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 255, 127, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(127, 255, 191, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(63, 255, 159, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(0, 127, 63, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(0, 170, 84, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(0, 255, 255, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        brush7 = QBrush(QColor(170, 170, 255, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush7)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush8 = QBrush(QColor(255, 255, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush8)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        brush9 = QBrush(QColor(170, 170, 0, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush2)
        brush10 = QBrush(QColor(170, 85, 255, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.NoRole, brush10)
        brush11 = QBrush(QColor(255, 255, 220, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush11)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush12 = QBrush(QColor(255, 255, 127, 128))
        brush12.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush12)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.NoRole, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush11)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        brush13 = QBrush(QColor(0, 0, 0, 128))
        brush13.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush13)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.NoRole, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush11)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush13)
#endif
        self.status_l.setPalette(palette)
        font2 = QFont()
        font2.setFamily(u"MS Shell Dlg 2")
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setWeight(75)
        self.status_l.setFont(font2)
        self.status_l.setFrameShape(QFrame.StyledPanel)
        self.status_l.setFrameShadow(QFrame.Plain)
        self.status_l.setAlignment(Qt.AlignCenter)
        self.status_l.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.status_l)

        self.unlock_tb = QToolButton(self.control_tab)
        self.unlock_tb.setObjectName(u"unlock_tb")
        sizePolicy6.setHeightForWidth(self.unlock_tb.sizePolicy().hasHeightForWidth())
        self.unlock_tb.setSizePolicy(sizePolicy6)
        self.unlock_tb.setMinimumSize(QSize(120, 80))
        self.unlock_tb.setMaximumSize(QSize(120, 16777215))
        icon14 = QIcon()
        icon14.addFile(u":/resources/resources/icons/white-unlock-padlock.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon14.addFile(u":/resources/resources/icons/gray-unlock-padlock.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon14.addFile(u":/resources/resources/icons/gray-unlock-padlock.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.unlock_tb.setIcon(icon14)
        self.unlock_tb.setIconSize(QSize(64, 64))
        self.unlock_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.unlock_tb)

        self.homing_tb = QToolButton(self.control_tab)
        self.homing_tb.setObjectName(u"homing_tb")
        sizePolicy6.setHeightForWidth(self.homing_tb.sizePolicy().hasHeightForWidth())
        self.homing_tb.setSizePolicy(sizePolicy6)
        self.homing_tb.setMinimumSize(QSize(120, 80))
        self.homing_tb.setMaximumSize(QSize(120, 16777215))
        icon15 = QIcon()
        icon15.addFile(u":/resources/resources/icons/white-home.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon15.addFile(u":/resources/resources/icons/gray-home.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon15.addFile(u":/resources/resources/icons/gray-home.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.homing_tb.setIcon(icon15)
        self.homing_tb.setIconSize(QSize(64, 64))
        self.homing_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.homing_tb)

        self.play_tb = QToolButton(self.control_tab)
        self.play_tb.setObjectName(u"play_tb")
        sizePolicy6.setHeightForWidth(self.play_tb.sizePolicy().hasHeightForWidth())
        self.play_tb.setSizePolicy(sizePolicy6)
        self.play_tb.setMinimumSize(QSize(120, 80))
        self.play_tb.setMaximumSize(QSize(120, 16777215))
        icon16 = QIcon()
        icon16.addFile(u":/resources/resources/icons/white-play-button-arrowhead.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon16.addFile(u":/resources/resources/icons/gray-play-button-arrowhead.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon16.addFile(u":/resources/resources/icons/gray-play-button-arrowhead.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.play_tb.setIcon(icon16)
        self.play_tb.setIconSize(QSize(64, 64))
        self.play_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.play_tb)

        self.pause_resume_tb = QToolButton(self.control_tab)
        self.pause_resume_tb.setObjectName(u"pause_resume_tb")
        sizePolicy6.setHeightForWidth(self.pause_resume_tb.sizePolicy().hasHeightForWidth())
        self.pause_resume_tb.setSizePolicy(sizePolicy6)
        self.pause_resume_tb.setMinimumSize(QSize(120, 80))
        self.pause_resume_tb.setMaximumSize(QSize(120, 16777215))
        icon17 = QIcon()
        icon17.addFile(u":/resources/resources/icons/white-pause-multimedia-big-gross-symbol-lines.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon17.addFile(u":/resources/resources/icons/gray-pause-multimedia-big-gross-symbol-lines.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon17.addFile(u":/resources/resources/icons/gray-pause-multimedia-big-gross-symbol-lines.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.pause_resume_tb.setIcon(icon17)
        self.pause_resume_tb.setIconSize(QSize(64, 64))
        self.pause_resume_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.pause_resume_tb)

        self.stop_tb = QToolButton(self.control_tab)
        self.stop_tb.setObjectName(u"stop_tb")
        sizePolicy6.setHeightForWidth(self.stop_tb.sizePolicy().hasHeightForWidth())
        self.stop_tb.setSizePolicy(sizePolicy6)
        self.stop_tb.setMinimumSize(QSize(120, 80))
        self.stop_tb.setMaximumSize(QSize(120, 16777215))
        icon18 = QIcon()
        icon18.addFile(u":/resources/resources/icons/white-stop-button-black-rounded-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon18.addFile(u":/resources/resources/icons/gray-stop-button-black-rounded-square.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon18.addFile(u":/resources/resources/icons/gray-stop-button-black-rounded-square.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.stop_tb.setIcon(icon18)
        self.stop_tb.setIconSize(QSize(64, 64))
        self.stop_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.stop_tb)

        self.tool_change_tb = QToolButton(self.control_tab)
        self.tool_change_tb.setObjectName(u"tool_change_tb")
        sizePolicy6.setHeightForWidth(self.tool_change_tb.sizePolicy().hasHeightForWidth())
        self.tool_change_tb.setSizePolicy(sizePolicy6)
        self.tool_change_tb.setMinimumSize(QSize(120, 80))
        self.tool_change_tb.setMaximumSize(QSize(120, 16777215))
        icon19 = QIcon()
        icon19.addFile(u":/resources/resources/icons/white-milling-machine.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon19.addFile(u":/resources/resources/icons/gray-milling-machine.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon19.addFile(u":/resources/resources/icons/gray-milling-machine.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.tool_change_tb.setIcon(icon19)
        self.tool_change_tb.setIconSize(QSize(72, 72))
        self.tool_change_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_3.addWidget(self.tool_change_tb)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.main_tab_widget.addTab(self.control_tab, "")
        self.align_tab = QWidget()
        self.align_tab.setObjectName(u"align_tab")
        self.align_tab.setFont(font)
        self.horizontalLayout_7 = QHBoxLayout(self.align_tab)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.openGLWidget_2 = QOpenGLWidget(self.align_tab)
        self.openGLWidget_2.setObjectName(u"openGLWidget_2")

        self.horizontalLayout_7.addWidget(self.openGLWidget_2)

        self.label_2 = QLabel(self.align_tab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.verticalSlider = QSlider(self.align_tab)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMaximum(255)
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.horizontalLayout_7.addWidget(self.verticalSlider)

        self.main_tab_widget.addTab(self.align_tab, "")
        self.settings_tab = QWidget()
        self.settings_tab.setObjectName(u"settings_tab")
        self.verticalLayout_12 = QVBoxLayout(self.settings_tab)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.settings_sub_tab = QTabWidget(self.settings_tab)
        self.settings_sub_tab.setObjectName(u"settings_sub_tab")
        self.settings_sub_tab.setEnabled(True)
        self.application_settings_tab = QWidget()
        self.application_settings_tab.setObjectName(u"application_settings_tab")
        self.gridLayout_9 = QGridLayout(self.application_settings_tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.top_layer_color_pb = QPushButton(self.application_settings_tab)
        self.top_layer_color_pb.setObjectName(u"top_layer_color_pb")

        self.gridLayout_12.addWidget(self.top_layer_color_pb, 0, 0, 1, 1)

        self.bottom_layer_color_pb = QPushButton(self.application_settings_tab)
        self.bottom_layer_color_pb.setObjectName(u"bottom_layer_color_pb")

        self.gridLayout_12.addWidget(self.bottom_layer_color_pb, 1, 0, 1, 1)

        self.bottom_layer_color_la = QLabel(self.application_settings_tab)
        self.bottom_layer_color_la.setObjectName(u"bottom_layer_color_la")
        self.bottom_layer_color_la.setMinimumSize(QSize(150, 0))
        self.bottom_layer_color_la.setFrameShape(QFrame.WinPanel)

        self.gridLayout_12.addWidget(self.bottom_layer_color_la, 1, 1, 1, 1)

        self.drill_layer_color_pb = QPushButton(self.application_settings_tab)
        self.drill_layer_color_pb.setObjectName(u"drill_layer_color_pb")

        self.gridLayout_12.addWidget(self.drill_layer_color_pb, 3, 0, 1, 1)

        self.nc_top_layer_color_pb = QPushButton(self.application_settings_tab)
        self.nc_top_layer_color_pb.setObjectName(u"nc_top_layer_color_pb")

        self.gridLayout_12.addWidget(self.nc_top_layer_color_pb, 4, 0, 1, 1)

        self.top_layer_color_la = QLabel(self.application_settings_tab)
        self.top_layer_color_la.setObjectName(u"top_layer_color_la")
        self.top_layer_color_la.setMinimumSize(QSize(150, 0))
        self.top_layer_color_la.setFrameShape(QFrame.WinPanel)

        self.gridLayout_12.addWidget(self.top_layer_color_la, 0, 1, 1, 1)

        self.profile_layer_color_pb = QPushButton(self.application_settings_tab)
        self.profile_layer_color_pb.setObjectName(u"profile_layer_color_pb")

        self.gridLayout_12.addWidget(self.profile_layer_color_pb, 2, 0, 1, 1)

        self.nc_bottom_layer_color_pb = QPushButton(self.application_settings_tab)
        self.nc_bottom_layer_color_pb.setObjectName(u"nc_bottom_layer_color_pb")

        self.gridLayout_12.addWidget(self.nc_bottom_layer_color_pb, 5, 0, 1, 1)

        self.profile_layer_color_la = QLabel(self.application_settings_tab)
        self.profile_layer_color_la.setObjectName(u"profile_layer_color_la")
        self.profile_layer_color_la.setMinimumSize(QSize(150, 0))
        self.profile_layer_color_la.setFrameShape(QFrame.WinPanel)

        self.gridLayout_12.addWidget(self.profile_layer_color_la, 2, 1, 1, 1)

        self.drill_layer_color_la = QLabel(self.application_settings_tab)
        self.drill_layer_color_la.setObjectName(u"drill_layer_color_la")
        self.drill_layer_color_la.setMinimumSize(QSize(150, 0))
        self.drill_layer_color_la.setFrameShape(QFrame.WinPanel)

        self.gridLayout_12.addWidget(self.drill_layer_color_la, 3, 1, 1, 1)

        self.nc_top_layer_color_la = QLabel(self.application_settings_tab)
        self.nc_top_layer_color_la.setObjectName(u"nc_top_layer_color_la")
        self.nc_top_layer_color_la.setMinimumSize(QSize(150, 0))
        self.nc_top_layer_color_la.setFrameShape(QFrame.WinPanel)

        self.gridLayout_12.addWidget(self.nc_top_layer_color_la, 4, 1, 1, 1)

        self.nc_bottom_layer_color_la = QLabel(self.application_settings_tab)
        self.nc_bottom_layer_color_la.setObjectName(u"nc_bottom_layer_color_la")
        self.nc_bottom_layer_color_la.setMinimumSize(QSize(150, 0))
        self.nc_bottom_layer_color_la.setFrameShape(QFrame.WinPanel)

        self.gridLayout_12.addWidget(self.nc_bottom_layer_color_la, 5, 1, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_12, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.settings_sub_tab.addTab(self.application_settings_tab, "")
        self.jobs_machine_settings_tab = QWidget()
        self.jobs_machine_settings_tab.setObjectName(u"jobs_machine_settings_tab")
        self.gridLayout_13 = QGridLayout(self.jobs_machine_settings_tab)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetFixedSize)
        self.line_15 = QFrame(self.jobs_machine_settings_tab)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setFrameShape(QFrame.HLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_15)

        self.probe_settings_section_la = QLabel(self.jobs_machine_settings_tab)
        self.probe_settings_section_la.setObjectName(u"probe_settings_section_la")
        sizePolicy3.setHeightForWidth(self.probe_settings_section_la.sizePolicy().hasHeightForWidth())
        self.probe_settings_section_la.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setPointSize(12)
        self.probe_settings_section_la.setFont(font3)

        self.verticalLayout_4.addWidget(self.probe_settings_section_la, 0, Qt.AlignHCenter)

        self.line_16 = QFrame(self.jobs_machine_settings_tab)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setFrameShape(QFrame.HLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_16)

        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setHorizontalSpacing(0)
        self.gridLayout_21.setVerticalSpacing(2)
        self.horizontalSpacer_10 = QSpacerItem(180, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_10, 0, 0, 1, 1)

        self.hold_on_probe_chb = QCheckBox(self.jobs_machine_settings_tab)
        self.hold_on_probe_chb.setObjectName(u"hold_on_probe_chb")
        sizePolicy3.setHeightForWidth(self.hold_on_probe_chb.sizePolicy().hasHeightForWidth())
        self.hold_on_probe_chb.setSizePolicy(sizePolicy3)
        self.hold_on_probe_chb.setMinimumSize(QSize(150, 0))
        self.hold_on_probe_chb.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_21.addWidget(self.hold_on_probe_chb, 0, 1, 1, 1, Qt.AlignHCenter)

        self.zeroing_after_probe_chb = QCheckBox(self.jobs_machine_settings_tab)
        self.zeroing_after_probe_chb.setObjectName(u"zeroing_after_probe_chb")
        sizePolicy3.setHeightForWidth(self.zeroing_after_probe_chb.sizePolicy().hasHeightForWidth())
        self.zeroing_after_probe_chb.setSizePolicy(sizePolicy3)
        self.zeroing_after_probe_chb.setMinimumSize(QSize(150, 0))
        self.zeroing_after_probe_chb.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_21.addWidget(self.zeroing_after_probe_chb, 0, 2, 1, 1, Qt.AlignHCenter)


        self.verticalLayout_4.addLayout(self.gridLayout_21)


        self.gridLayout_13.addLayout(self.verticalLayout_4, 6, 0, 1, 1)

        self.line_9 = QFrame(self.jobs_machine_settings_tab)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_9, 14, 0, 1, 1)

        self.line_13 = QFrame(self.jobs_machine_settings_tab)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.HLine)
        self.line_13.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_13, 4, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout_14.setVerticalSpacing(2)
        self.tool_probe_y_wpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_y_wpos_dsb.setObjectName(u"tool_probe_y_wpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_y_wpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_y_wpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_y_wpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_y_wpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_y_wpos_dsb.setFont(font)
        self.tool_probe_y_wpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_y_wpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_y_wpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_y_wpos_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_y_wpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_y_wpos_dsb, 2, 2, 1, 1)

        self.tool_probe_y_mpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_y_mpos_dsb.setObjectName(u"tool_probe_y_mpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_y_mpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_y_mpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_y_mpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_y_mpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_y_mpos_dsb.setFont(font)
        self.tool_probe_y_mpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_y_mpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_y_mpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_y_mpos_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_y_mpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_y_mpos_dsb, 1, 2, 1, 1)

        self.x_la = QLabel(self.jobs_machine_settings_tab)
        self.x_la.setObjectName(u"x_la")
        sizePolicy3.setHeightForWidth(self.x_la.sizePolicy().hasHeightForWidth())
        self.x_la.setSizePolicy(sizePolicy3)
        self.x_la.setMaximumSize(QSize(80, 50))
        self.x_la.setFont(font)
        self.x_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.x_la, 0, 1, 1, 1, Qt.AlignHCenter)

        self.y_la = QLabel(self.jobs_machine_settings_tab)
        self.y_la.setObjectName(u"y_la")
        sizePolicy3.setHeightForWidth(self.y_la.sizePolicy().hasHeightForWidth())
        self.y_la.setSizePolicy(sizePolicy3)
        self.y_la.setMaximumSize(QSize(80, 50))
        self.y_la.setFont(font)
        self.y_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.y_la, 0, 2, 1, 1, Qt.AlignHCenter)

        self.tool_probe_z_limit_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_z_limit_dsb.setObjectName(u"tool_probe_z_limit_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_z_limit_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_z_limit_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_z_limit_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_z_limit_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_z_limit_dsb.setFont(font)
        self.tool_probe_z_limit_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.tool_probe_z_limit_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_z_limit_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_z_limit_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_z_limit_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_z_limit_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_z_limit_dsb, 3, 3, 1, 1)

        self.tool_probe_x_wpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_x_wpos_dsb.setObjectName(u"tool_probe_x_wpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_x_wpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_x_wpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_x_wpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_x_wpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_x_wpos_dsb.setFont(font)
        self.tool_probe_x_wpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_x_wpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_x_wpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_x_wpos_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_x_wpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_x_wpos_dsb, 2, 1, 1, 1)

        self.z_la = QLabel(self.jobs_machine_settings_tab)
        self.z_la.setObjectName(u"z_la")
        sizePolicy3.setHeightForWidth(self.z_la.sizePolicy().hasHeightForWidth())
        self.z_la.setSizePolicy(sizePolicy3)
        self.z_la.setMaximumSize(QSize(80, 50))
        self.z_la.setFont(font)
        self.z_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.z_la, 0, 3, 1, 1, Qt.AlignHCenter)

        self.tool_probe_x_mpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_x_mpos_dsb.setObjectName(u"tool_probe_x_mpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_x_mpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_x_mpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_x_mpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_x_mpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_x_mpos_dsb.setFont(font)
        self.tool_probe_x_mpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_x_mpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_x_mpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_x_mpos_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_x_mpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_x_mpos_dsb, 1, 1, 1, 1)

        self.tool_probe_wpos_la = QLabel(self.jobs_machine_settings_tab)
        self.tool_probe_wpos_la.setObjectName(u"tool_probe_wpos_la")
        sizePolicy3.setHeightForWidth(self.tool_probe_wpos_la.sizePolicy().hasHeightForWidth())
        self.tool_probe_wpos_la.setSizePolicy(sizePolicy3)
        self.tool_probe_wpos_la.setMinimumSize(QSize(130, 20))
        self.tool_probe_wpos_la.setMaximumSize(QSize(130, 16777215))
        self.tool_probe_wpos_la.setFont(font)
        self.tool_probe_wpos_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.tool_probe_wpos_la, 2, 0, 1, 1)

        self.tool_probe_z_mpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_z_mpos_dsb.setObjectName(u"tool_probe_z_mpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_z_mpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_z_mpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_z_mpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_z_mpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_z_mpos_dsb.setFont(font)
        self.tool_probe_z_mpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_z_mpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_z_mpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_z_mpos_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_z_mpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_z_mpos_dsb, 1, 3, 1, 1)

        self.tool_probe_mpos_la = QLabel(self.jobs_machine_settings_tab)
        self.tool_probe_mpos_la.setObjectName(u"tool_probe_mpos_la")
        sizePolicy3.setHeightForWidth(self.tool_probe_mpos_la.sizePolicy().hasHeightForWidth())
        self.tool_probe_mpos_la.setSizePolicy(sizePolicy3)
        self.tool_probe_mpos_la.setMinimumSize(QSize(130, 20))
        self.tool_probe_mpos_la.setMaximumSize(QSize(130, 16777215))
        self.tool_probe_mpos_la.setFont(font)
        self.tool_probe_mpos_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.tool_probe_mpos_la, 1, 0, 1, 1)

        self.tool_probe_z_wpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_probe_z_wpos_dsb.setObjectName(u"tool_probe_z_wpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_probe_z_wpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_probe_z_wpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_probe_z_wpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_probe_z_wpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_probe_z_wpos_dsb.setFont(font)
        self.tool_probe_z_wpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_probe_z_wpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_probe_z_wpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_probe_z_wpos_dsb.setMaximum(1000.000000000000000)
        self.tool_probe_z_wpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_14.addWidget(self.tool_probe_z_wpos_dsb, 2, 3, 1, 1)

        self.tool_probe_z_limit_la = QLabel(self.jobs_machine_settings_tab)
        self.tool_probe_z_limit_la.setObjectName(u"tool_probe_z_limit_la")
        sizePolicy3.setHeightForWidth(self.tool_probe_z_limit_la.sizePolicy().hasHeightForWidth())
        self.tool_probe_z_limit_la.setSizePolicy(sizePolicy3)
        self.tool_probe_z_limit_la.setMinimumSize(QSize(130, 20))
        self.tool_probe_z_limit_la.setMaximumSize(QSize(130, 16777215))
        self.tool_probe_z_limit_la.setFont(font)
        self.tool_probe_z_limit_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.tool_probe_z_limit_la, 3, 0, 1, 1)

        self.tool_probe_wm_pos_chb = QCheckBox(self.jobs_machine_settings_tab)
        self.tool_probe_wm_pos_chb.setObjectName(u"tool_probe_wm_pos_chb")
        sizePolicy3.setHeightForWidth(self.tool_probe_wm_pos_chb.sizePolicy().hasHeightForWidth())
        self.tool_probe_wm_pos_chb.setSizePolicy(sizePolicy3)
        self.tool_probe_wm_pos_chb.setMinimumSize(QSize(150, 20))
        self.tool_probe_wm_pos_chb.setMaximumSize(QSize(150, 20))
        self.tool_probe_wm_pos_chb.setLayoutDirection(Qt.LeftToRight)
        self.tool_probe_wm_pos_chb.setAutoFillBackground(True)

        self.gridLayout_14.addWidget(self.tool_probe_wm_pos_chb, 1, 4, 1, 1, Qt.AlignHCenter)

        self.get_tool_probe_pb = QPushButton(self.jobs_machine_settings_tab)
        self.get_tool_probe_pb.setObjectName(u"get_tool_probe_pb")
        sizePolicy3.setHeightForWidth(self.get_tool_probe_pb.sizePolicy().hasHeightForWidth())
        self.get_tool_probe_pb.setSizePolicy(sizePolicy3)
        self.get_tool_probe_pb.setMinimumSize(QSize(180, 20))
        self.get_tool_probe_pb.setMaximumSize(QSize(180, 20))
        self.get_tool_probe_pb.setFont(font)
        self.get_tool_probe_pb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_14.addWidget(self.get_tool_probe_pb, 2, 4, 1, 1, Qt.AlignHCenter)


        self.horizontalLayout_13.addLayout(self.gridLayout_14)


        self.verticalLayout_5.addLayout(self.horizontalLayout_13)

        self.line_6 = QFrame(self.jobs_machine_settings_tab)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_6)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setSizeConstraint(QLayout.SetFixedSize)
        self.tool_change_z_mpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_change_z_mpos_dsb.setObjectName(u"tool_change_z_mpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_change_z_mpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_change_z_mpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_change_z_mpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_change_z_mpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_change_z_mpos_dsb.setFont(font)
        self.tool_change_z_mpos_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.tool_change_z_mpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_change_z_mpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_change_z_mpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_change_z_mpos_dsb.setMaximum(1000.000000000000000)
        self.tool_change_z_mpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_15.addWidget(self.tool_change_z_mpos_dsb, 0, 4, 1, 1)

        self.tool_change_y_mpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_change_y_mpos_dsb.setObjectName(u"tool_change_y_mpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_change_y_mpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_change_y_mpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_change_y_mpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_change_y_mpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_change_y_mpos_dsb.setFont(font)
        self.tool_change_y_mpos_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.tool_change_y_mpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_change_y_mpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_change_y_mpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_change_y_mpos_dsb.setMaximum(1000.000000000000000)
        self.tool_change_y_mpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_15.addWidget(self.tool_change_y_mpos_dsb, 0, 2, 1, 1)

        self.tool_change_x_mpos_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.tool_change_x_mpos_dsb.setObjectName(u"tool_change_x_mpos_dsb")
        sizePolicy3.setHeightForWidth(self.tool_change_x_mpos_dsb.sizePolicy().hasHeightForWidth())
        self.tool_change_x_mpos_dsb.setSizePolicy(sizePolicy3)
        self.tool_change_x_mpos_dsb.setMinimumSize(QSize(80, 20))
        self.tool_change_x_mpos_dsb.setMaximumSize(QSize(80, 16777215))
        self.tool_change_x_mpos_dsb.setFont(font)
        self.tool_change_x_mpos_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.tool_change_x_mpos_dsb.setAlignment(Qt.AlignCenter)
        self.tool_change_x_mpos_dsb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.tool_change_x_mpos_dsb.setMinimum(-1000.000000000000000)
        self.tool_change_x_mpos_dsb.setMaximum(1000.000000000000000)
        self.tool_change_x_mpos_dsb.setSingleStep(0.100000000000000)

        self.gridLayout_15.addWidget(self.tool_change_x_mpos_dsb, 0, 1, 1, 1)

        self.tool_change_la = QLabel(self.jobs_machine_settings_tab)
        self.tool_change_la.setObjectName(u"tool_change_la")
        sizePolicy3.setHeightForWidth(self.tool_change_la.sizePolicy().hasHeightForWidth())
        self.tool_change_la.setSizePolicy(sizePolicy3)
        self.tool_change_la.setMinimumSize(QSize(130, 20))
        self.tool_change_la.setMaximumSize(QSize(130, 16777215))
        self.tool_change_la.setFont(font)
        self.tool_change_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_15.addWidget(self.tool_change_la, 0, 0, 1, 1)

        self.get_tool_change_pb = QPushButton(self.jobs_machine_settings_tab)
        self.get_tool_change_pb.setObjectName(u"get_tool_change_pb")
        sizePolicy3.setHeightForWidth(self.get_tool_change_pb.sizePolicy().hasHeightForWidth())
        self.get_tool_change_pb.setSizePolicy(sizePolicy3)
        self.get_tool_change_pb.setMinimumSize(QSize(150, 20))
        self.get_tool_change_pb.setMaximumSize(QSize(180, 20))
        self.get_tool_change_pb.setFont(font)
        self.get_tool_change_pb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_15.addWidget(self.get_tool_change_pb, 0, 5, 1, 1, Qt.AlignHCenter)


        self.horizontalLayout_15.addLayout(self.gridLayout_15)


        self.verticalLayout_5.addLayout(self.horizontalLayout_15)


        self.gridLayout_13.addLayout(self.verticalLayout_5, 11, 0, 1, 1)

        self.line_7 = QFrame(self.jobs_machine_settings_tab)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_7, 12, 0, 1, 1)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setSizeConstraint(QLayout.SetFixedSize)
        self.x_axis_la = QLabel(self.jobs_machine_settings_tab)
        self.x_axis_la.setObjectName(u"x_axis_la")
        sizePolicy3.setHeightForWidth(self.x_axis_la.sizePolicy().hasHeightForWidth())
        self.x_axis_la.setSizePolicy(sizePolicy3)
        self.x_axis_la.setMinimumSize(QSize(150, 20))
        self.x_axis_la.setMaximumSize(QSize(150, 20))
        self.x_axis_la.setFont(font)
        self.x_axis_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_20.addWidget(self.x_axis_la, 0, 1, 1, 1, Qt.AlignHCenter)

        self.x_la_2 = QLabel(self.jobs_machine_settings_tab)
        self.x_la_2.setObjectName(u"x_la_2")
        sizePolicy3.setHeightForWidth(self.x_la_2.sizePolicy().hasHeightForWidth())
        self.x_la_2.setSizePolicy(sizePolicy3)
        self.x_la_2.setMinimumSize(QSize(150, 20))
        self.x_la_2.setMaximumSize(QSize(150, 20))
        self.x_la_2.setFont(font)
        self.x_la_2.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_20.addWidget(self.x_la_2, 0, 2, 1, 1, Qt.AlignHCenter)

        self.mirroring_axis_la = QLabel(self.jobs_machine_settings_tab)
        self.mirroring_axis_la.setObjectName(u"mirroring_axis_la")
        sizePolicy3.setHeightForWidth(self.mirroring_axis_la.sizePolicy().hasHeightForWidth())
        self.mirroring_axis_la.setSizePolicy(sizePolicy3)
        self.mirroring_axis_la.setMinimumSize(QSize(130, 0))
        self.mirroring_axis_la.setMaximumSize(QSize(130, 16777215))
        self.mirroring_axis_la.setFont(font)
        self.mirroring_axis_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_20.addWidget(self.mirroring_axis_la, 1, 0, 1, 1, Qt.AlignLeft|Qt.AlignVCenter)

        self.x_mirror_rb = QRadioButton(self.jobs_machine_settings_tab)
        self.x_mirror_rb.setObjectName(u"x_mirror_rb")
        sizePolicy3.setHeightForWidth(self.x_mirror_rb.sizePolicy().hasHeightForWidth())
        self.x_mirror_rb.setSizePolicy(sizePolicy3)
        self.x_mirror_rb.setMaximumSize(QSize(120, 20))

        self.gridLayout_20.addWidget(self.x_mirror_rb, 1, 1, 1, 1, Qt.AlignHCenter)

        self.y_mirror_rb = QRadioButton(self.jobs_machine_settings_tab)
        self.y_mirror_rb.setObjectName(u"y_mirror_rb")
        sizePolicy3.setHeightForWidth(self.y_mirror_rb.sizePolicy().hasHeightForWidth())
        self.y_mirror_rb.setSizePolicy(sizePolicy3)
        self.y_mirror_rb.setMaximumSize(QSize(120, 20))

        self.gridLayout_20.addWidget(self.y_mirror_rb, 1, 2, 1, 1, Qt.AlignHCenter)

        self.horizontalSpacer_9 = QSpacerItem(130, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_20, 3, 0, 1, 1)

        self.line_12 = QFrame(self.jobs_machine_settings_tab)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.HLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_12, 0, 0, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setVerticalSpacing(2)
        self.feedrate_z_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.feedrate_z_dsb.setObjectName(u"feedrate_z_dsb")
        self.feedrate_z_dsb.setMinimumSize(QSize(252, 0))
        self.feedrate_z_dsb.setMaximumSize(QSize(252, 16777215))
        self.feedrate_z_dsb.setFont(font)
        self.feedrate_z_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.feedrate_z_dsb.setAlignment(Qt.AlignCenter)
        self.feedrate_z_dsb.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.feedrate_z_dsb.setMaximum(100000.000000000000000)
        self.feedrate_z_dsb.setSingleStep(1.000000000000000)

        self.gridLayout_19.addWidget(self.feedrate_z_dsb, 1, 1, 1, 1)

        self.z_feedrate_la = QLabel(self.jobs_machine_settings_tab)
        self.z_feedrate_la.setObjectName(u"z_feedrate_la")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.z_feedrate_la.sizePolicy().hasHeightForWidth())
        self.z_feedrate_la.setSizePolicy(sizePolicy13)
        self.z_feedrate_la.setMinimumSize(QSize(130, 0))
        self.z_feedrate_la.setMaximumSize(QSize(130, 16777215))
        self.z_feedrate_la.setFont(font)
        self.z_feedrate_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_19.addWidget(self.z_feedrate_la, 1, 0, 1, 1)

        self.xy_feedrate_la = QLabel(self.jobs_machine_settings_tab)
        self.xy_feedrate_la.setObjectName(u"xy_feedrate_la")
        sizePolicy3.setHeightForWidth(self.xy_feedrate_la.sizePolicy().hasHeightForWidth())
        self.xy_feedrate_la.setSizePolicy(sizePolicy3)
        self.xy_feedrate_la.setMinimumSize(QSize(130, 0))
        self.xy_feedrate_la.setMaximumSize(QSize(130, 16777215))
        self.xy_feedrate_la.setFont(font)
        self.xy_feedrate_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_19.addWidget(self.xy_feedrate_la, 0, 0, 1, 1)

        self.feedrate_xy_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.feedrate_xy_dsb.setObjectName(u"feedrate_xy_dsb")
        sizePolicy3.setHeightForWidth(self.feedrate_xy_dsb.sizePolicy().hasHeightForWidth())
        self.feedrate_xy_dsb.setSizePolicy(sizePolicy3)
        self.feedrate_xy_dsb.setMinimumSize(QSize(252, 0))
        self.feedrate_xy_dsb.setMaximumSize(QSize(252, 16777215))
        self.feedrate_xy_dsb.setFont(font)
        self.feedrate_xy_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.feedrate_xy_dsb.setAlignment(Qt.AlignCenter)
        self.feedrate_xy_dsb.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.feedrate_xy_dsb.setMaximum(100000.000000000000000)
        self.feedrate_xy_dsb.setSingleStep(1.000000000000000)

        self.gridLayout_19.addWidget(self.feedrate_xy_dsb, 0, 1, 1, 1)

        self.feedrate_probe_dsb = QDoubleSpinBox(self.jobs_machine_settings_tab)
        self.feedrate_probe_dsb.setObjectName(u"feedrate_probe_dsb")
        self.feedrate_probe_dsb.setMinimumSize(QSize(252, 0))
        self.feedrate_probe_dsb.setMaximumSize(QSize(252, 16777215))
        self.feedrate_probe_dsb.setFont(font)
        self.feedrate_probe_dsb.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.feedrate_probe_dsb.setAlignment(Qt.AlignCenter)
        self.feedrate_probe_dsb.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.feedrate_probe_dsb.setMaximum(100000.000000000000000)
        self.feedrate_probe_dsb.setSingleStep(1.000000000000000)

        self.gridLayout_19.addWidget(self.feedrate_probe_dsb, 2, 1, 1, 1)

        self.probe_feedrate_la = QLabel(self.jobs_machine_settings_tab)
        self.probe_feedrate_la.setObjectName(u"probe_feedrate_la")
        sizePolicy3.setHeightForWidth(self.probe_feedrate_la.sizePolicy().hasHeightForWidth())
        self.probe_feedrate_la.setSizePolicy(sizePolicy3)
        self.probe_feedrate_la.setMinimumSize(QSize(130, 0))
        self.probe_feedrate_la.setMaximumSize(QSize(130, 16777215))
        self.probe_feedrate_la.setFont(font)
        self.probe_feedrate_la.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        self.gridLayout_19.addWidget(self.probe_feedrate_la, 2, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(200, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_6, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(200, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_7, 1, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(200, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_8, 2, 2, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_19, 17, 0, 1, 1)

        self.line_8 = QFrame(self.jobs_machine_settings_tab)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_8, 10, 0, 1, 1)

        self.feedrates_section_la = QLabel(self.jobs_machine_settings_tab)
        self.feedrates_section_la.setObjectName(u"feedrates_section_la")
        self.feedrates_section_la.setFont(font3)

        self.gridLayout_13.addWidget(self.feedrates_section_la, 15, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.line_10 = QFrame(self.jobs_machine_settings_tab)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_10, 16, 0, 1, 1)

        self.jobs_common_settings_section_la = QLabel(self.jobs_machine_settings_tab)
        self.jobs_common_settings_section_la.setObjectName(u"jobs_common_settings_section_la")
        sizePolicy3.setHeightForWidth(self.jobs_common_settings_section_la.sizePolicy().hasHeightForWidth())
        self.jobs_common_settings_section_la.setSizePolicy(sizePolicy3)
        self.jobs_common_settings_section_la.setMinimumSize(QSize(210, 0))
        self.jobs_common_settings_section_la.setMaximumSize(QSize(300, 20))
        self.jobs_common_settings_section_la.setFont(font3)

        self.gridLayout_13.addWidget(self.jobs_common_settings_section_la, 1, 0, 1, 1, Qt.AlignHCenter)

        self.line_14 = QFrame(self.jobs_machine_settings_tab)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setFrameShape(QFrame.HLine)
        self.line_14.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_14, 8, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_13.addItem(self.verticalSpacer_4, 13, 0, 1, 1)

        self.tool_change_section_la = QLabel(self.jobs_machine_settings_tab)
        self.tool_change_section_la.setObjectName(u"tool_change_section_la")
        sizePolicy3.setHeightForWidth(self.tool_change_section_la.sizePolicy().hasHeightForWidth())
        self.tool_change_section_la.setSizePolicy(sizePolicy3)
        self.tool_change_section_la.setFont(font3)

        self.gridLayout_13.addWidget(self.tool_change_section_la, 9, 0, 1, 1, Qt.AlignHCenter)

        self.line_11 = QFrame(self.jobs_machine_settings_tab)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.HLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_11, 2, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_4, 11, 1, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_13.addItem(self.verticalSpacer_6, 7, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_13.addItem(self.verticalSpacer_5, 5, 0, 1, 1)

        self.settings_sub_tab.addTab(self.jobs_machine_settings_tab, "")

        self.verticalLayout_12.addWidget(self.settings_sub_tab)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_11)

        self.restore_settings_preferences_pb = QPushButton(self.settings_tab)
        self.restore_settings_preferences_pb.setObjectName(u"restore_settings_preferences_pb")

        self.horizontalLayout_16.addWidget(self.restore_settings_preferences_pb)

        self.save_settings_preferences_pb = QPushButton(self.settings_tab)
        self.save_settings_preferences_pb.setObjectName(u"save_settings_preferences_pb")

        self.horizontalLayout_16.addWidget(self.save_settings_preferences_pb)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_5)


        self.verticalLayout_12.addLayout(self.horizontalLayout_16)

        self.main_tab_widget.addTab(self.settings_tab, "")

        self.verticalLayout_6.addWidget(self.main_tab_widget)

        self.logging_plain_te = QPlainTextEdit(self.central_widget)
        self.logging_plain_te.setObjectName(u"logging_plain_te")
        sizePolicy10.setHeightForWidth(self.logging_plain_te.sizePolicy().hasHeightForWidth())
        self.logging_plain_te.setSizePolicy(sizePolicy10)
        self.logging_plain_te.setMinimumSize(QSize(0, 40))
        self.logging_plain_te.setMaximumSize(QSize(16777215, 200))
        self.logging_plain_te.setReadOnly(True)
        self.logging_plain_te.setMaximumBlockCount(20000)

        self.verticalLayout_6.addWidget(self.logging_plain_te)

        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1160, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuConsole = QMenu(self.menubar)
        self.menuConsole.setObjectName(u"menuConsole")
        self.menu_set_level = QMenu(self.menuConsole)
        self.menu_set_level.setObjectName(u"menu_set_level")
        self.menu_set_level.setInputMethodHints(Qt.ImhNone)
        MainWindow.setMenuBar(self.menubar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)
        QWidget.setTabOrder(self.main_tab_widget, self.prepare_widget)
        QWidget.setTabOrder(self.prepare_widget, self.top_file_le)
        QWidget.setTabOrder(self.top_file_le, self.top_load_pb)
        QWidget.setTabOrder(self.top_load_pb, self.top_view_chb)
        QWidget.setTabOrder(self.top_view_chb, self.bottom_file_le)
        QWidget.setTabOrder(self.bottom_file_le, self.bottom_load_pb)
        QWidget.setTabOrder(self.bottom_load_pb, self.bottom_view_chb)
        QWidget.setTabOrder(self.bottom_view_chb, self.profile_file_le)
        QWidget.setTabOrder(self.profile_file_le, self.profile_load_pb)
        QWidget.setTabOrder(self.profile_load_pb, self.profile_view_chb)
        QWidget.setTabOrder(self.profile_view_chb, self.drill_file_le)
        QWidget.setTabOrder(self.drill_file_le, self.drill_load_pb)
        QWidget.setTabOrder(self.drill_load_pb, self.drill_view_chb)
        QWidget.setTabOrder(self.drill_view_chb, self.no_copper_1_le)
        QWidget.setTabOrder(self.no_copper_1_le, self.no_copper_1_pb)
        QWidget.setTabOrder(self.no_copper_1_pb, self.no_copper_1_chb)
        QWidget.setTabOrder(self.no_copper_1_chb, self.no_copper_2_le)
        QWidget.setTabOrder(self.no_copper_2_le, self.no_copper_2_pb)
        QWidget.setTabOrder(self.no_copper_2_pb, self.no_copper_2_chb)
        QWidget.setTabOrder(self.no_copper_2_chb, self.clear_views_pb)
        QWidget.setTabOrder(self.clear_views_pb, self.all_view_chb)
        QWidget.setTabOrder(self.all_view_chb, self.layer_choice_cb)
        QWidget.setTabOrder(self.layer_choice_cb, self.bottom_tool_diameter_dsb)
        QWidget.setTabOrder(self.bottom_tool_diameter_dsb, self.bottom_n_passes_sb)
        QWidget.setTabOrder(self.bottom_n_passes_sb, self.bottom_overlap_dsb)
        QWidget.setTabOrder(self.bottom_overlap_dsb, self.bottom_cut_z_dsb)
        QWidget.setTabOrder(self.bottom_cut_z_dsb, self.bottom_travel_z_dsb)
        QWidget.setTabOrder(self.bottom_travel_z_dsb, self.bottom_spindle_speed_dsb)
        QWidget.setTabOrder(self.bottom_spindle_speed_dsb, self.bottom_xy_feed_rate_dsb)
        QWidget.setTabOrder(self.bottom_xy_feed_rate_dsb, self.bottom_z_feed_rate_dsb)
        QWidget.setTabOrder(self.bottom_z_feed_rate_dsb, self.bottom_generate_job_pb)
        QWidget.setTabOrder(self.bottom_generate_job_pb, self.top_tool_diameter_dsb)
        QWidget.setTabOrder(self.top_tool_diameter_dsb, self.top_n_passes_sb)
        QWidget.setTabOrder(self.top_n_passes_sb, self.top_overlap_dsb)
        QWidget.setTabOrder(self.top_overlap_dsb, self.top_cut_z_dsb)
        QWidget.setTabOrder(self.top_cut_z_dsb, self.top_travel_z_dsb)
        QWidget.setTabOrder(self.top_travel_z_dsb, self.top_spindle_speed_dsb)
        QWidget.setTabOrder(self.top_spindle_speed_dsb, self.top_xy_feed_rate_dsb)
        QWidget.setTabOrder(self.top_xy_feed_rate_dsb, self.top_z_feed_rate_dsb)
        QWidget.setTabOrder(self.top_z_feed_rate_dsb, self.top_generate_job_pb)
        QWidget.setTabOrder(self.top_generate_job_pb, self.profile_tool_diameter_dsb)
        QWidget.setTabOrder(self.profile_tool_diameter_dsb, self.profile_margin_dsb)
        QWidget.setTabOrder(self.profile_margin_dsb, self.profile_multi_depth_chb)
        QWidget.setTabOrder(self.profile_multi_depth_chb, self.profile_depth_pass_dsb)
        QWidget.setTabOrder(self.profile_depth_pass_dsb, self.profile_cut_z_dsb)
        QWidget.setTabOrder(self.profile_cut_z_dsb, self.profile_travel_z_dsb)
        QWidget.setTabOrder(self.profile_travel_z_dsb, self.profile_spindle_speed_dsb)
        QWidget.setTabOrder(self.profile_spindle_speed_dsb, self.profile_xy_feed_rate_dsb)
        QWidget.setTabOrder(self.profile_xy_feed_rate_dsb, self.profile_z_feed_rate_dsb)
        QWidget.setTabOrder(self.profile_z_feed_rate_dsb, self.profile_taps_layout_cb)
        QWidget.setTabOrder(self.profile_taps_layout_cb, self.profile_tap_size_dsb)
        QWidget.setTabOrder(self.profile_tap_size_dsb, self.profile_generate_job_pb)
        QWidget.setTabOrder(self.profile_generate_job_pb, self.drill_tw)
        QWidget.setTabOrder(self.drill_tw, self.add_drill_tool_tb)
        QWidget.setTabOrder(self.add_drill_tool_tb, self.remove_drill_tool_tb)
        QWidget.setTabOrder(self.remove_drill_tool_tb, self.drill_milling_tool_chb)
        QWidget.setTabOrder(self.drill_milling_tool_chb, self.drill_milling_tool_diameter_dsb)
        QWidget.setTabOrder(self.drill_milling_tool_diameter_dsb, self.drill_cut_z_dsb)
        QWidget.setTabOrder(self.drill_cut_z_dsb, self.drill_travel_z_dsb)
        QWidget.setTabOrder(self.drill_travel_z_dsb, self.drill_spindle_speed_dsb)
        QWidget.setTabOrder(self.drill_spindle_speed_dsb, self.drill_xy_feed_rate_dsb)
        QWidget.setTabOrder(self.drill_xy_feed_rate_dsb, self.drill_z_feed_rate_dsb)
        QWidget.setTabOrder(self.drill_z_feed_rate_dsb, self.drill_generate_job_pb)
        QWidget.setTabOrder(self.drill_generate_job_pb, self.nc_top_tool_diameter_dsb)
        QWidget.setTabOrder(self.nc_top_tool_diameter_dsb, self.nc_top_overlap_dsb)
        QWidget.setTabOrder(self.nc_top_overlap_dsb, self.nc_top_cut_z_dsb)
        QWidget.setTabOrder(self.nc_top_cut_z_dsb, self.nc_top_travel_z_dsb)
        QWidget.setTabOrder(self.nc_top_travel_z_dsb, self.nc_top_spindle_speed_dsb)
        QWidget.setTabOrder(self.nc_top_spindle_speed_dsb, self.nc_top_xy_feed_rate_dsb)
        QWidget.setTabOrder(self.nc_top_xy_feed_rate_dsb, self.nc_top_z_feed_rate_dsb)
        QWidget.setTabOrder(self.nc_top_z_feed_rate_dsb, self.nc_top_generate_pb)
        QWidget.setTabOrder(self.nc_top_generate_pb, self.nc_bottom_tool_diameter_dsb)
        QWidget.setTabOrder(self.nc_bottom_tool_diameter_dsb, self.nc_bottom_overlap_dsb)
        QWidget.setTabOrder(self.nc_bottom_overlap_dsb, self.nc_bottom_cut_z_dsb)
        QWidget.setTabOrder(self.nc_bottom_cut_z_dsb, self.nc_bottom_travel_z_dsb)
        QWidget.setTabOrder(self.nc_bottom_travel_z_dsb, self.nc_bottom_spindle_speed_dsb)
        QWidget.setTabOrder(self.nc_bottom_spindle_speed_dsb, self.nc_bottom_xy_feed_rate_dsb)
        QWidget.setTabOrder(self.nc_bottom_xy_feed_rate_dsb, self.nc_bottom_z_feed_rate_dsb)
        QWidget.setTabOrder(self.nc_bottom_z_feed_rate_dsb, self.nc_bottom_generate_pb)
        QWidget.setTabOrder(self.nc_bottom_generate_pb, self.logging_plain_te)
        QWidget.setTabOrder(self.logging_plain_te, self.verticalSlider)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConsole.menuAction())
        self.menuFile.addAction(self.actionSettings_Preferences)
        self.menuFile.addAction(self.actionSave_Settings)
        self.menuConsole.addAction(self.actionHide_Show_Console)
        self.menuConsole.addAction(self.menu_set_level.menuAction())
        self.menu_set_level.addAction(self.action_critical)
        self.menu_set_level.addAction(self.action_error)
        self.menu_set_level.addAction(self.action_warning)
        self.menu_set_level.addAction(self.action_info)
        self.menu_set_level.addAction(self.action_debug)

        self.retranslateUi(MainWindow)

        self.main_tab_widget.setCurrentIndex(1)
        self.prepare_widget.setCurrentIndex(0)
        self.jobs_sw.setCurrentIndex(0)
        self.ctrl_tab_widget.setCurrentIndex(0)
        self.z_step_cb.setCurrentIndex(3)
        self.xy_step_cb.setCurrentIndex(3)
        self.settings_sub_tab.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TheAntFarm", None))
        self.actionHide_Show_Console.setText(QCoreApplication.translate("MainWindow", u"Hide/Show Console", None))
#if QT_CONFIG(shortcut)
        self.actionHide_Show_Console.setShortcut(QCoreApplication.translate("MainWindow", u"F4", None))
#endif // QT_CONFIG(shortcut)
        self.actionSettings_Preferences.setText(QCoreApplication.translate("MainWindow", u"Settings/Preferences", None))
#if QT_CONFIG(tooltip)
        self.actionSettings_Preferences.setToolTip(QCoreApplication.translate("MainWindow", u"Hide/Show Settings Tab", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionSettings_Preferences.setStatusTip(QCoreApplication.translate("MainWindow", u"Hide/Show Settings Tab", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionSettings_Preferences.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_Settings.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
#if QT_CONFIG(shortcut)
        self.actionSave_Settings.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_critical.setText(QCoreApplication.translate("MainWindow", u"CRITICAL", None))
        self.action_error.setText(QCoreApplication.translate("MainWindow", u"ERROR", None))
        self.action_warning.setText(QCoreApplication.translate("MainWindow", u"WARNING", None))
        self.action_info.setText(QCoreApplication.translate("MainWindow", u"INFO", None))
        self.action_debug.setText(QCoreApplication.translate("MainWindow", u"DEBUG", None))
#if QT_CONFIG(tooltip)
        self.no_copper_2_pb.setToolTip(QCoreApplication.translate("MainWindow", u"NO-COPPER BOTTOM load layer button", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.no_copper_2_pb.setStatusTip(QCoreApplication.translate("MainWindow", u"NO-COPPER BOTTOM load layer button", None))
#endif // QT_CONFIG(statustip)
        self.no_copper_2_pb.setText(QCoreApplication.translate("MainWindow", u"NC BOTTOM", None))
        self.no_copper_2_chb.setText("")
        self.view_label.setText(QCoreApplication.translate("MainWindow", u"View", None))
#if QT_CONFIG(tooltip)
        self.no_copper_1_pb.setToolTip(QCoreApplication.translate("MainWindow", u"NO-COPPER TOP load layer button", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.no_copper_1_pb.setStatusTip(QCoreApplication.translate("MainWindow", u"NO-COPPER TOP load layer button", None))
#endif // QT_CONFIG(statustip)
        self.no_copper_1_pb.setText(QCoreApplication.translate("MainWindow", u"NC TOP", None))
        self.bottom_view_chb.setText("")
        self.profile_load_pb.setText(QCoreApplication.translate("MainWindow", u"PROFILE", None))
        self.no_copper_1_chb.setText("")
        self.clear_views_pb.setText(QCoreApplication.translate("MainWindow", u"CLEAR ALL", None))
        self.drill_load_pb.setText(QCoreApplication.translate("MainWindow", u"DRILL", None))
        self.top_load_pb.setText(QCoreApplication.translate("MainWindow", u"TOP", None))
        self.bottom_load_pb.setText(QCoreApplication.translate("MainWindow", u"BOTTOM", None))
        self.drill_view_chb.setText("")
        self.file_path_l.setText(QCoreApplication.translate("MainWindow", u"File Path", None))
        self.all_view_chb.setText("")
        self.profile_view_chb.setText("")
        self.prepare_widget.setTabText(self.prepare_widget.indexOf(self.load_layers_tab), QCoreApplication.translate("MainWindow", u"LOAD LAYERS", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Load a valid Layer", None))
        self.top_tool_diameter_la.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.top_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.top_n_passes_la.setText(QCoreApplication.translate("MainWindow", u"Number of Passes", None))
        self.top_travel_z_la.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.top_cut_z_la.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.top_overlap_la.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.top_spindle_speed_la.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.top_xy_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.top_z_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.bottom_z_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.bottom_overlap_la.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.bottom_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.bottom_tool_diameter_la.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.bottom_n_passes_la.setText(QCoreApplication.translate("MainWindow", u"Number of Passes", None))
        self.bottom_travel_z_la.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.bottom_cut_z_la.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.bottom_xy_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.bottom_spindle_speed_la.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.profile_depth_pass_la.setText(QCoreApplication.translate("MainWindow", u"Depth per Pass [mm]", None))
        self.profile_taps_layout_la.setText(QCoreApplication.translate("MainWindow", u"Taps layout", None))
        self.profile_margin_la.setText(QCoreApplication.translate("MainWindow", u"Margin [mm]", None))
        self.profile_cut_z_la.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.profile_xy_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.profile_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.profile_tool_diameter_la.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.profile_multi_depth_chb.setText("")
        self.profile_z_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.profile_tap_size_la.setText(QCoreApplication.translate("MainWindow", u"Tap size [mm]", None))
        self.profile_travel_z_la.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.profile_multi_depth_la.setText(QCoreApplication.translate("MainWindow", u"Multi-depth", None))
        self.profile_spindle_speed_la.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.profile_mirror_la.setText(QCoreApplication.translate("MainWindow", u"Mirror", None))
        self.profile_mirror_chb.setText("")
        self.drill_travel_z_la.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.add_drill_tool_tb.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.drill_z_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.drill_xy_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.drill_cut_z_la.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.drill_milling_tool_la.setText(QCoreApplication.translate("MainWindow", u"Milling Tool", None))
        self.remove_drill_tool_tb.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.drill_milling_tool_chb.setText("")
        self.drill_optimization_la.setText(QCoreApplication.translate("MainWindow", u"Optimization", None))
        ___qtablewidgetitem = self.drill_tw.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Bit", None));
        ___qtablewidgetitem1 = self.drill_tw.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Diameter [mm]", None));
        self.drill_optimization_chb.setText("")
        self.drill_spindle_speed_la.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.drill_milling_tool_diameter_la.setText(QCoreApplication.translate("MainWindow", u"Mill Tool Diameter [mm]", None))
        self.drill_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.drill_mirror_la.setText(QCoreApplication.translate("MainWindow", u"Mirror", None))
        self.drill_mirror_chb.setText("")
        self.nc_top_overlap_la.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.nc_top_cut_z_la.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.nc_top_spindle_speed_la.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.nc_top_tool_diameter_la.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.nc_top_travel_z_la.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.nc_top_z_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.nc_top_xy_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.nc_top_generate_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.nc_bottom_travel_z_la.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.nc_bottom_generate_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.nc_bottom_spindle_speed_la.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.nc_bottom_cut_z_la.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.nc_bottom_overlap_la.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.nc_bottom_tool_diameter_la.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.nc_bottom_z_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.nc_bottom_xy_feed_rate_la.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.prepare_widget.setTabText(self.prepare_widget.indexOf(self.create_job_tab), QCoreApplication.translate("MainWindow", u"CREATE JOB", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Top View", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Bottom View", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.view_tab), QCoreApplication.translate("MainWindow", u"VIEW", None))
        ___qtablewidgetitem2 = self.gcode_tw.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"File Path", None));
        ___qtablewidgetitem3 = self.gcode_tw.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Select", None));
#if QT_CONFIG(statustip)
        self.upload_temp_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Reload gcode files generated.", None))
#endif // QT_CONFIG(statustip)
        self.upload_temp_tb.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(statustip)
        self.open_gcode_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Load gcode files.", None))
#endif // QT_CONFIG(statustip)
        self.open_gcode_tb.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(shortcut)
        self.open_gcode_tb.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+G", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(statustip)
        self.remove_gcode_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Remove gcode files.", None))
#endif // QT_CONFIG(statustip)
        self.remove_gcode_tb.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.ctrl_tab_widget.setTabText(self.ctrl_tab_widget.indexOf(self.gcode_load), QCoreApplication.translate("MainWindow", u"GCode", None))
        self.zero_xy_pb.setText(QCoreApplication.translate("MainWindow", u"XY = 0", None))
        self.zero_y_pb.setText(QCoreApplication.translate("MainWindow", u"Y = 0", None))
        self.z_axis_l.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.wpos_y_l.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.wpos_l.setText(QCoreApplication.translate("MainWindow", u"WPos", None))
        self.zero_z_pb.setText(QCoreApplication.translate("MainWindow", u"Z = 0", None))
        self.mpos_y_l.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mpos_z_l.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.x_axis_l.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.wpos_x_l.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.axis_l.setText(QCoreApplication.translate("MainWindow", u"Axis:", None))
        self.mpos_l.setText(QCoreApplication.translate("MainWindow", u"MPos", None))
        self.wpos_z_l.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.zero_x_pb.setText(QCoreApplication.translate("MainWindow", u"X = 0", None))
        self.y_axis_l.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.mpos_x_l.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.probe_pb.setText(QCoreApplication.translate("MainWindow", u"PROBE", None))
        self.get_bbox_pb.setText(QCoreApplication.translate("MainWindow", u"GET BBOX", None))
        self.ABL_pb.setText(QCoreApplication.translate("MainWindow", u"ABL", None))
#if QT_CONFIG(tooltip)
        self.abl_active_chb.setToolTip(QCoreApplication.translate("MainWindow", u"Apply ABL if checked", None))
#endif // QT_CONFIG(tooltip)
        self.abl_active_chb.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Min", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Max", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"N", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.z_plus_pb.setText(QCoreApplication.translate("MainWindow", u"Z+", None))
        self.z_minus_pb.setText(QCoreApplication.translate("MainWindow", u"Z-", None))
        self.xYMinusPlusButton.setText(QCoreApplication.translate("MainWindow", u"X- Y+", None))
        self.xYPlusMinuButton.setText(QCoreApplication.translate("MainWindow", u"X+ Y-", None))
        self.xMinusButton.setText(QCoreApplication.translate("MainWindow", u"X-", None))
        self.xYMinusButton.setText(QCoreApplication.translate("MainWindow", u"X- Y-", None))
        self.yPlusButton.setText(QCoreApplication.translate("MainWindow", u"Y+", None))
        self.center_tb.setText(QCoreApplication.translate("MainWindow", u"Center", None))
        self.yMinusButton.setText(QCoreApplication.translate("MainWindow", u"Y-", None))
        self.xYPlusButton.setText(QCoreApplication.translate("MainWindow", u"X+ Y+", None))
        self.xPlusButton.setText(QCoreApplication.translate("MainWindow", u"X+", None))
        self.z_jog_l_2.setText(QCoreApplication.translate("MainWindow", u"Z step [mm]", None))
        self.z_step_cb.setItemText(0, QCoreApplication.translate("MainWindow", u"100.0", None))
        self.z_step_cb.setItemText(1, QCoreApplication.translate("MainWindow", u"10.0", None))
        self.z_step_cb.setItemText(2, QCoreApplication.translate("MainWindow", u"5.0", None))
        self.z_step_cb.setItemText(3, QCoreApplication.translate("MainWindow", u"1.0", None))
        self.z_step_cb.setItemText(4, QCoreApplication.translate("MainWindow", u"0.5", None))
        self.z_step_cb.setItemText(5, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.z_step_cb.setItemText(6, QCoreApplication.translate("MainWindow", u"0.05", None))
        self.z_step_cb.setItemText(7, QCoreApplication.translate("MainWindow", u"0.01", None))

        self.z_mul_10_pb.setText(QCoreApplication.translate("MainWindow", u"x10", None))
        self.z_div_10_pb.setText(QCoreApplication.translate("MainWindow", u"\u00f710", None))
        self.z_minus_1_pb.setText(QCoreApplication.translate("MainWindow", u"-1.0", None))
        self.z_plus_1_pb.setText(QCoreApplication.translate("MainWindow", u"+1.0", None))
        self.xy_jog_l.setText(QCoreApplication.translate("MainWindow", u"XY step [mm]", None))
        self.xy_step_cb.setItemText(0, QCoreApplication.translate("MainWindow", u"100.0", None))
        self.xy_step_cb.setItemText(1, QCoreApplication.translate("MainWindow", u"10.0", None))
        self.xy_step_cb.setItemText(2, QCoreApplication.translate("MainWindow", u"5.0", None))
        self.xy_step_cb.setItemText(3, QCoreApplication.translate("MainWindow", u"1.0", None))
        self.xy_step_cb.setItemText(4, QCoreApplication.translate("MainWindow", u"0.5", None))
        self.xy_step_cb.setItemText(5, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.xy_step_cb.setItemText(6, QCoreApplication.translate("MainWindow", u"0.05", None))
        self.xy_step_cb.setItemText(7, QCoreApplication.translate("MainWindow", u"0.01", None))

        self.xy_plus_1_pb.setText(QCoreApplication.translate("MainWindow", u"+1.0", None))
        self.xy_div_10_pb.setText(QCoreApplication.translate("MainWindow", u"\u00f710", None))
        self.xy_mul_10_pb.setText(QCoreApplication.translate("MainWindow", u"x10", None))
        self.xy_minus_1_pb.setText(QCoreApplication.translate("MainWindow", u"-1.0", None))
        self.send_pb.setText(QCoreApplication.translate("MainWindow", u"Send", None))
#if QT_CONFIG(tooltip)
        self.serial_ports_cb.setToolTip(QCoreApplication.translate("MainWindow", u"Available serial ports.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.serial_ports_cb.setStatusTip(QCoreApplication.translate("MainWindow", u"Available serial ports.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.serial_baud_cb.setToolTip(QCoreApplication.translate("MainWindow", u"Serial port baudrate [bps]", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.serial_baud_cb.setStatusTip(QCoreApplication.translate("MainWindow", u"Serial port baudrate [bps]", None))
#endif // QT_CONFIG(statustip)
        self.serial_baud_cb.setCurrentText("")
#if QT_CONFIG(statustip)
        self.refresh_pb.setStatusTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(statustip)
        self.refresh_pb.setText(QCoreApplication.translate("MainWindow", u"Serial Ports Refresh", None))
        self.clear_terminal_pb.setText(QCoreApplication.translate("MainWindow", u"Clear Terminal", None))
#if QT_CONFIG(statustip)
        self.connect_pb.setStatusTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(statustip)
        self.connect_pb.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.ctrl_tab_widget.setTabText(self.ctrl_tab_widget.indexOf(self.sender_tab), QCoreApplication.translate("MainWindow", u"Sender", None))
#if QT_CONFIG(statustip)
        self.soft_reset_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Send a soft reset command to the machine.", None))
#endif // QT_CONFIG(statustip)
        self.soft_reset_tb.setText(QCoreApplication.translate("MainWindow", u"SOFT RESET", None))
        self.status_l.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
#if QT_CONFIG(statustip)
        self.unlock_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Send the unlock command to the machine.", None))
#endif // QT_CONFIG(statustip)
        self.unlock_tb.setText(QCoreApplication.translate("MainWindow", u"UNLOCK", None))
#if QT_CONFIG(statustip)
        self.homing_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Execute homing procedure.", None))
#endif // QT_CONFIG(statustip)
        self.homing_tb.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
#if QT_CONFIG(statustip)
        self.play_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Send the selected gcode file.", None))
#endif // QT_CONFIG(statustip)
        self.play_tb.setText(QCoreApplication.translate("MainWindow", u"PLAY", None))
#if QT_CONFIG(statustip)
        self.pause_resume_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Pause/Hold the machine.", None))
#endif // QT_CONFIG(statustip)
        self.pause_resume_tb.setText(QCoreApplication.translate("MainWindow", u"PAUSE/RESUME", None))
#if QT_CONFIG(statustip)
        self.stop_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Stop sending the gcode file.", None))
#endif // QT_CONFIG(statustip)
        self.stop_tb.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
#if QT_CONFIG(statustip)
        self.tool_change_tb.setStatusTip(QCoreApplication.translate("MainWindow", u"Execute a tool change procedure.", None))
#endif // QT_CONFIG(statustip)
        self.tool_change_tb.setText(QCoreApplication.translate("MainWindow", u"TOOL CHANGE", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.control_tab), QCoreApplication.translate("MainWindow", u"CONTROL", None))
        self.label_2.setText("")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.align_tab), QCoreApplication.translate("MainWindow", u"ALIGN", None))
        self.top_layer_color_pb.setText(QCoreApplication.translate("MainWindow", u"TOP LAYER COLOR", None))
        self.bottom_layer_color_pb.setText(QCoreApplication.translate("MainWindow", u"BOTTOM LAYER COLOR", None))
        self.bottom_layer_color_la.setText("")
        self.drill_layer_color_pb.setText(QCoreApplication.translate("MainWindow", u"DRILL LAYER COLOR", None))
        self.nc_top_layer_color_pb.setText(QCoreApplication.translate("MainWindow", u"NC TOP LAYER COLOR", None))
        self.top_layer_color_la.setText("")
        self.profile_layer_color_pb.setText(QCoreApplication.translate("MainWindow", u"PROFILE LAYER COLOR", None))
        self.nc_bottom_layer_color_pb.setText(QCoreApplication.translate("MainWindow", u"NC BOTTOM LAYER COLOR", None))
        self.profile_layer_color_la.setText("")
        self.drill_layer_color_la.setText("")
        self.nc_top_layer_color_la.setText("")
        self.nc_bottom_layer_color_la.setText("")
        self.settings_sub_tab.setTabText(self.settings_sub_tab.indexOf(self.application_settings_tab), QCoreApplication.translate("MainWindow", u"Application Settings", None))
        self.probe_settings_section_la.setText(QCoreApplication.translate("MainWindow", u"PROBE SETTINGS", None))
        self.hold_on_probe_chb.setText(QCoreApplication.translate("MainWindow", u"Hold On Probe", None))
        self.zeroing_after_probe_chb.setText(QCoreApplication.translate("MainWindow", u"Z=0 After Probe", None))
        self.x_la.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.y_la.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.z_la.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.tool_probe_wpos_la.setText(QCoreApplication.translate("MainWindow", u"Tool Probe WPos", None))
        self.tool_probe_mpos_la.setText(QCoreApplication.translate("MainWindow", u"Tool Probe MPos", None))
        self.tool_probe_z_limit_la.setText(QCoreApplication.translate("MainWindow", u"Tool Probe Z Limit", None))
        self.tool_probe_wm_pos_chb.setText(QCoreApplication.translate("MainWindow", u"Working Position", None))
        self.get_tool_probe_pb.setText(QCoreApplication.translate("MainWindow", u"Get Tool Probe Position", None))
        self.tool_change_la.setText(QCoreApplication.translate("MainWindow", u"Tool Change MPos", None))
        self.get_tool_change_pb.setText(QCoreApplication.translate("MainWindow", u"Get Tool Change Position", None))
        self.x_axis_la.setText(QCoreApplication.translate("MainWindow", u"X (top-down mirror)", None))
        self.x_la_2.setText(QCoreApplication.translate("MainWindow", u"Y (left-right mirror)", None))
        self.mirroring_axis_la.setText(QCoreApplication.translate("MainWindow", u"Mirroring axis", None))
        self.x_mirror_rb.setText("")
        self.y_mirror_rb.setText("")
        self.z_feedrate_la.setText(QCoreApplication.translate("MainWindow", u"Z FEEDRATE", None))
        self.xy_feedrate_la.setText(QCoreApplication.translate("MainWindow", u"XY FEEDRATE", None))
        self.probe_feedrate_la.setText(QCoreApplication.translate("MainWindow", u"PROBE FEEDRATE", None))
        self.feedrates_section_la.setText(QCoreApplication.translate("MainWindow", u"FEEDRATES [mm/min]", None))
        self.jobs_common_settings_section_la.setText(QCoreApplication.translate("MainWindow", u"JOBS COMMON SETTINGS", None))
        self.tool_change_section_la.setText(QCoreApplication.translate("MainWindow", u"TOOL CHANGE", None))
        self.settings_sub_tab.setTabText(self.settings_sub_tab.indexOf(self.jobs_machine_settings_tab), QCoreApplication.translate("MainWindow", u"Jobs/Machine Settings", None))
        self.restore_settings_preferences_pb.setText(QCoreApplication.translate("MainWindow", u"Restore Settings/Preferences", None))
        self.save_settings_preferences_pb.setText(QCoreApplication.translate("MainWindow", u"Save Settings/Preferences", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.settings_tab), QCoreApplication.translate("MainWindow", u"Settings/Preferences", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuConsole.setTitle(QCoreApplication.translate("MainWindow", u"Console", None))
        self.menu_set_level.setTitle(QCoreApplication.translate("MainWindow", u"Set Level", None))
    # retranslateUi

