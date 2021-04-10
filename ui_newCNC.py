# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newCNC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from vispy_qt_widget import VispyCanvas


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1039, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(926, 720))
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionLoad.setFont(font)
        self.actionHide_Show_Console = QAction(MainWindow)
        self.actionHide_Show_Console.setObjectName(u"actionHide_Show_Console")
        self.actionHide_Show_Console.setCheckable(True)
        self.actionHide_Show_Console.setChecked(True)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.central_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.main_tab_widget = QTabWidget(self.central_widget)
        self.main_tab_widget.setObjectName(u"main_tab_widget")
        self.main_tab_widget.setFont(font)
        self.main_tab_widget.setTabShape(QTabWidget.Rounded)
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

        self.top_tool_diameter_l = QLabel(self.top_page)
        self.top_tool_diameter_l.setObjectName(u"top_tool_diameter_l")

        self.gridLayout_2.addWidget(self.top_tool_diameter_l, 0, 0, 1, 1)

        self.top_generate_job_pb = QPushButton(self.top_page)
        self.top_generate_job_pb.setObjectName(u"top_generate_job_pb")

        self.gridLayout_2.addWidget(self.top_generate_job_pb, 11, 0, 1, 2)

        self.top_n_passes_l = QLabel(self.top_page)
        self.top_n_passes_l.setObjectName(u"top_n_passes_l")

        self.gridLayout_2.addWidget(self.top_n_passes_l, 1, 0, 1, 1)

        self.top_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.top_vertical_spacer, 10, 0, 1, 2)

        self.top_travel_z_l = QLabel(self.top_page)
        self.top_travel_z_l.setObjectName(u"top_travel_z_l")

        self.gridLayout_2.addWidget(self.top_travel_z_l, 4, 0, 1, 1)

        self.top_travel_z_dsb = QDoubleSpinBox(self.top_page)
        self.top_travel_z_dsb.setObjectName(u"top_travel_z_dsb")
        self.top_travel_z_dsb.setDecimals(2)
        self.top_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.top_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.top_travel_z_dsb, 4, 1, 1, 1)

        self.top_cut_z_l = QLabel(self.top_page)
        self.top_cut_z_l.setObjectName(u"top_cut_z_l")

        self.gridLayout_2.addWidget(self.top_cut_z_l, 3, 0, 1, 1)

        self.top_overlap_l = QLabel(self.top_page)
        self.top_overlap_l.setObjectName(u"top_overlap_l")

        self.gridLayout_2.addWidget(self.top_overlap_l, 2, 0, 1, 1)

        self.top_spindle_speed_l = QLabel(self.top_page)
        self.top_spindle_speed_l.setObjectName(u"top_spindle_speed_l")

        self.gridLayout_2.addWidget(self.top_spindle_speed_l, 6, 0, 1, 1)

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

        self.top_xy_feed_rate_l = QLabel(self.top_page)
        self.top_xy_feed_rate_l.setObjectName(u"top_xy_feed_rate_l")

        self.gridLayout_2.addWidget(self.top_xy_feed_rate_l, 7, 0, 1, 1)

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

        self.top_z_feed_rate_l = QLabel(self.top_page)
        self.top_z_feed_rate_l.setObjectName(u"top_z_feed_rate_l")

        self.gridLayout_2.addWidget(self.top_z_feed_rate_l, 9, 0, 1, 1)

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
        self.bottom_z_feed_rate_l = QLabel(self.bottom_page)
        self.bottom_z_feed_rate_l.setObjectName(u"bottom_z_feed_rate_l")

        self.gridLayout_3.addWidget(self.bottom_z_feed_rate_l, 9, 0, 1, 1)

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

        self.bottom_overlap_l = QLabel(self.bottom_page)
        self.bottom_overlap_l.setObjectName(u"bottom_overlap_l")

        self.gridLayout_3.addWidget(self.bottom_overlap_l, 3, 0, 1, 1)

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

        self.bottom_tool_diameter_l = QLabel(self.bottom_page)
        self.bottom_tool_diameter_l.setObjectName(u"bottom_tool_diameter_l")

        self.gridLayout_3.addWidget(self.bottom_tool_diameter_l, 1, 0, 1, 1)

        self.bottom_n_passes_l = QLabel(self.bottom_page)
        self.bottom_n_passes_l.setObjectName(u"bottom_n_passes_l")

        self.gridLayout_3.addWidget(self.bottom_n_passes_l, 2, 0, 1, 1)

        self.bottom_travel_z_l = QLabel(self.bottom_page)
        self.bottom_travel_z_l.setObjectName(u"bottom_travel_z_l")

        self.gridLayout_3.addWidget(self.bottom_travel_z_l, 5, 0, 1, 1)

        self.bottom_cut_z_l = QLabel(self.bottom_page)
        self.bottom_cut_z_l.setObjectName(u"bottom_cut_z_l")

        self.gridLayout_3.addWidget(self.bottom_cut_z_l, 4, 0, 1, 1)

        self.bottom_travel_z_dsb = QDoubleSpinBox(self.bottom_page)
        self.bottom_travel_z_dsb.setObjectName(u"bottom_travel_z_dsb")
        self.bottom_travel_z_dsb.setDecimals(2)
        self.bottom_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.bottom_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.bottom_travel_z_dsb, 5, 1, 1, 1)

        self.bottom_xy_feed_rate_l = QLabel(self.bottom_page)
        self.bottom_xy_feed_rate_l.setObjectName(u"bottom_xy_feed_rate_l")

        self.gridLayout_3.addWidget(self.bottom_xy_feed_rate_l, 8, 0, 1, 1)

        self.bottom_spindle_speed_l = QLabel(self.bottom_page)
        self.bottom_spindle_speed_l.setObjectName(u"bottom_spindle_speed_l")

        self.gridLayout_3.addWidget(self.bottom_spindle_speed_l, 6, 0, 1, 1)

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
        self.profile_depth_pass_l = QLabel(self.profile_page)
        self.profile_depth_pass_l.setObjectName(u"profile_depth_pass_l")

        self.gridLayout_4.addWidget(self.profile_depth_pass_l, 3, 1, 1, 1)

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

        self.profile_taps_layout_l = QLabel(self.profile_page)
        self.profile_taps_layout_l.setObjectName(u"profile_taps_layout_l")

        self.gridLayout_4.addWidget(self.profile_taps_layout_l, 11, 1, 1, 1)

        self.profile_margin_l = QLabel(self.profile_page)
        self.profile_margin_l.setObjectName(u"profile_margin_l")

        self.gridLayout_4.addWidget(self.profile_margin_l, 1, 1, 1, 1)

        self.profile_tap_size_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_tap_size_dsb.setObjectName(u"profile_tap_size_dsb")
        self.profile_tap_size_dsb.setDecimals(2)
        self.profile_tap_size_dsb.setMinimum(-9999.000000000000000)
        self.profile_tap_size_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_tap_size_dsb, 12, 3, 1, 1)

        self.profile_cut_z_l = QLabel(self.profile_page)
        self.profile_cut_z_l.setObjectName(u"profile_cut_z_l")

        self.gridLayout_4.addWidget(self.profile_cut_z_l, 5, 1, 1, 1)

        self.profile_xy_feed_rate_l = QLabel(self.profile_page)
        self.profile_xy_feed_rate_l.setObjectName(u"profile_xy_feed_rate_l")

        self.gridLayout_4.addWidget(self.profile_xy_feed_rate_l, 9, 1, 1, 1)

        self.profile_z_feed_rate_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_z_feed_rate_dsb.setObjectName(u"profile_z_feed_rate_dsb")
        self.profile_z_feed_rate_dsb.setDecimals(2)
        self.profile_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.profile_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_z_feed_rate_dsb, 10, 3, 1, 1)

        self.profile_generate_job_pb = QPushButton(self.profile_page)
        self.profile_generate_job_pb.setObjectName(u"profile_generate_job_pb")

        self.gridLayout_4.addWidget(self.profile_generate_job_pb, 16, 1, 1, 3)

        self.profile_tool_diameter_l = QLabel(self.profile_page)
        self.profile_tool_diameter_l.setObjectName(u"profile_tool_diameter_l")

        self.gridLayout_4.addWidget(self.profile_tool_diameter_l, 0, 1, 1, 1)

        self.profile_multi_depth_chb = QCheckBox(self.profile_page)
        self.profile_multi_depth_chb.setObjectName(u"profile_multi_depth_chb")
        sizePolicy2.setHeightForWidth(self.profile_multi_depth_chb.sizePolicy().hasHeightForWidth())
        self.profile_multi_depth_chb.setSizePolicy(sizePolicy2)
        self.profile_multi_depth_chb.setMinimumSize(QSize(123, 0))

        self.gridLayout_4.addWidget(self.profile_multi_depth_chb, 2, 3, 1, 1, Qt.AlignHCenter)

        self.profile_z_feed_rate_l = QLabel(self.profile_page)
        self.profile_z_feed_rate_l.setObjectName(u"profile_z_feed_rate_l")

        self.gridLayout_4.addWidget(self.profile_z_feed_rate_l, 10, 1, 1, 1)

        self.profile_tool_diameter_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_tool_diameter_dsb.setObjectName(u"profile_tool_diameter_dsb")
        self.profile_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_4.addWidget(self.profile_tool_diameter_dsb, 0, 3, 1, 1)

        self.profile_tap_size_l = QLabel(self.profile_page)
        self.profile_tap_size_l.setObjectName(u"profile_tap_size_l")

        self.gridLayout_4.addWidget(self.profile_tap_size_l, 12, 1, 1, 1)

        self.profile_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.profile_vertical_spacer, 15, 1, 1, 3)

        self.profile_travel_z_l = QLabel(self.profile_page)
        self.profile_travel_z_l.setObjectName(u"profile_travel_z_l")

        self.gridLayout_4.addWidget(self.profile_travel_z_l, 6, 1, 1, 1)

        self.profile_travel_z_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_travel_z_dsb.setObjectName(u"profile_travel_z_dsb")
        self.profile_travel_z_dsb.setDecimals(2)
        self.profile_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.profile_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_travel_z_dsb, 6, 3, 1, 1)

        self.profile_taps_layout_cb = QComboBox(self.profile_page)
        self.profile_taps_layout_cb.setObjectName(u"profile_taps_layout_cb")

        self.gridLayout_4.addWidget(self.profile_taps_layout_cb, 11, 3, 1, 1)

        self.profile_multi_depth_l = QLabel(self.profile_page)
        self.profile_multi_depth_l.setObjectName(u"profile_multi_depth_l")

        self.gridLayout_4.addWidget(self.profile_multi_depth_l, 2, 1, 1, 1)

        self.profile_spindle_speed_l = QLabel(self.profile_page)
        self.profile_spindle_speed_l.setObjectName(u"profile_spindle_speed_l")

        self.gridLayout_4.addWidget(self.profile_spindle_speed_l, 7, 1, 1, 1)

        self.profile_spindle_speed_dsb = QDoubleSpinBox(self.profile_page)
        self.profile_spindle_speed_dsb.setObjectName(u"profile_spindle_speed_dsb")
        self.profile_spindle_speed_dsb.setDecimals(2)
        self.profile_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.profile_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.profile_spindle_speed_dsb, 7, 3, 1, 1)

        self.jobs_sw.addWidget(self.profile_page)
        self.drill_page = QWidget()
        self.drill_page.setObjectName(u"drill_page")
        self.gridLayout_5 = QGridLayout(self.drill_page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.drill_tw = QTableWidget(self.drill_page)
        if (self.drill_tw.columnCount() < 2):
            self.drill_tw.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.drill_tw.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.drill_tw.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.drill_tw.setObjectName(u"drill_tw")

        self.gridLayout_5.addWidget(self.drill_tw, 0, 1, 1, 2)

        self.drill_travel_z_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_travel_z_dsb.setObjectName(u"drill_travel_z_dsb")
        self.drill_travel_z_dsb.setDecimals(2)
        self.drill_travel_z_dsb.setMinimum(-9999.000000000000000)
        self.drill_travel_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_travel_z_dsb, 5, 2, 1, 1)

        self.drill_cut_z_l = QLabel(self.drill_page)
        self.drill_cut_z_l.setObjectName(u"drill_cut_z_l")

        self.gridLayout_5.addWidget(self.drill_cut_z_l, 4, 1, 1, 1)

        self.drill_tool_diameter_l = QLabel(self.drill_page)
        self.drill_tool_diameter_l.setObjectName(u"drill_tool_diameter_l")

        self.gridLayout_5.addWidget(self.drill_tool_diameter_l, 2, 1, 1, 1)

        self.drill_generate_job_pb = QPushButton(self.drill_page)
        self.drill_generate_job_pb.setObjectName(u"drill_generate_job_pb")

        self.gridLayout_5.addWidget(self.drill_generate_job_pb, 13, 1, 1, 2)

        self.drill_xy_feed_rate_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_xy_feed_rate_dsb.setObjectName(u"drill_xy_feed_rate_dsb")
        self.drill_xy_feed_rate_dsb.setDecimals(2)
        self.drill_xy_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.drill_xy_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_xy_feed_rate_dsb, 8, 2, 1, 1)

        self.drill_z_feed_rate_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_z_feed_rate_dsb.setObjectName(u"drill_z_feed_rate_dsb")
        self.drill_z_feed_rate_dsb.setDecimals(2)
        self.drill_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.drill_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_z_feed_rate_dsb, 10, 2, 1, 1)

        self.drill_travel_z_l = QLabel(self.drill_page)
        self.drill_travel_z_l.setObjectName(u"drill_travel_z_l")

        self.gridLayout_5.addWidget(self.drill_travel_z_l, 5, 1, 1, 1)

        self.drill_milling_tool_ = QLabel(self.drill_page)
        self.drill_milling_tool_.setObjectName(u"drill_milling_tool_")

        self.gridLayout_5.addWidget(self.drill_milling_tool_, 1, 1, 1, 1)

        self.drill_tool_diameter_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_tool_diameter_dsb.setObjectName(u"drill_tool_diameter_dsb")
        self.drill_tool_diameter_dsb.setMinimum(0.010000000000000)

        self.gridLayout_5.addWidget(self.drill_tool_diameter_dsb, 2, 2, 1, 1)

        self.drill_xy_feed_rate_l = QLabel(self.drill_page)
        self.drill_xy_feed_rate_l.setObjectName(u"drill_xy_feed_rate_l")

        self.gridLayout_5.addWidget(self.drill_xy_feed_rate_l, 8, 1, 1, 1)

        self.drill_z_feed_rate_l = QLabel(self.drill_page)
        self.drill_z_feed_rate_l.setObjectName(u"drill_z_feed_rate_l")

        self.gridLayout_5.addWidget(self.drill_z_feed_rate_l, 10, 1, 1, 1)

        self.drill_milling_tool_chb = QCheckBox(self.drill_page)
        self.drill_milling_tool_chb.setObjectName(u"drill_milling_tool_chb")

        self.gridLayout_5.addWidget(self.drill_milling_tool_chb, 1, 2, 1, 1)

        self.drill_cut_z_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_cut_z_dsb.setObjectName(u"drill_cut_z_dsb")
        self.drill_cut_z_dsb.setDecimals(2)
        self.drill_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.drill_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_cut_z_dsb, 4, 2, 1, 1)

        self.drill_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.drill_vertical_spacer, 12, 1, 1, 2)

        self.drill_spindle_speed_l = QLabel(self.drill_page)
        self.drill_spindle_speed_l.setObjectName(u"drill_spindle_speed_l")

        self.gridLayout_5.addWidget(self.drill_spindle_speed_l, 6, 1, 1, 1)

        self.drill_spindle_speed_dsb = QDoubleSpinBox(self.drill_page)
        self.drill_spindle_speed_dsb.setObjectName(u"drill_spindle_speed_dsb")
        self.drill_spindle_speed_dsb.setDecimals(2)
        self.drill_spindle_speed_dsb.setMinimum(-9999.000000000000000)
        self.drill_spindle_speed_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.drill_spindle_speed_dsb, 6, 2, 1, 1)

        self.jobs_sw.addWidget(self.drill_page)
        self.nc_area_top_page = QWidget()
        self.nc_area_top_page.setObjectName(u"nc_area_top_page")
        self.gridLayout_6 = QGridLayout(self.nc_area_top_page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.nc_top_overlap_l = QLabel(self.nc_area_top_page)
        self.nc_top_overlap_l.setObjectName(u"nc_top_overlap_l")

        self.gridLayout_6.addWidget(self.nc_top_overlap_l, 1, 0, 1, 1)

        self.nc_top_cut_z_l = QLabel(self.nc_area_top_page)
        self.nc_top_cut_z_l.setObjectName(u"nc_top_cut_z_l")

        self.gridLayout_6.addWidget(self.nc_top_cut_z_l, 2, 0, 1, 1)

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

        self.nc_top_spindle_speed_l = QLabel(self.nc_area_top_page)
        self.nc_top_spindle_speed_l.setObjectName(u"nc_top_spindle_speed_l")

        self.gridLayout_6.addWidget(self.nc_top_spindle_speed_l, 4, 0, 1, 1)

        self.nc_top_tool_diameter_l = QLabel(self.nc_area_top_page)
        self.nc_top_tool_diameter_l.setObjectName(u"nc_top_tool_diameter_l")

        self.gridLayout_6.addWidget(self.nc_top_tool_diameter_l, 0, 0, 1, 1)

        self.nc_top_cut_z_dsb = QDoubleSpinBox(self.nc_area_top_page)
        self.nc_top_cut_z_dsb.setObjectName(u"nc_top_cut_z_dsb")
        self.nc_top_cut_z_dsb.setDecimals(2)
        self.nc_top_cut_z_dsb.setMinimum(-9999.000000000000000)
        self.nc_top_cut_z_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.nc_top_cut_z_dsb, 2, 1, 1, 1)

        self.nc_top_travel_z_l = QLabel(self.nc_area_top_page)
        self.nc_top_travel_z_l.setObjectName(u"nc_top_travel_z_l")

        self.gridLayout_6.addWidget(self.nc_top_travel_z_l, 3, 0, 1, 1)

        self.nc_top_z_feed_rate_l = QLabel(self.nc_area_top_page)
        self.nc_top_z_feed_rate_l.setObjectName(u"nc_top_z_feed_rate_l")

        self.gridLayout_6.addWidget(self.nc_top_z_feed_rate_l, 6, 0, 1, 1)

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

        self.nc_top_xy_feed_rate_l = QLabel(self.nc_area_top_page)
        self.nc_top_xy_feed_rate_l.setObjectName(u"nc_top_xy_feed_rate_l")

        self.gridLayout_6.addWidget(self.nc_top_xy_feed_rate_l, 5, 0, 1, 1)

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
        self.nc_bottom_travel_z_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_travel_z_l.setObjectName(u"nc_bottom_travel_z_l")

        self.gridLayout_7.addWidget(self.nc_bottom_travel_z_l, 3, 0, 1, 1)

        self.nc_bottom_generate_pb = QPushButton(self.nc_area_bottom_page)
        self.nc_bottom_generate_pb.setObjectName(u"nc_bottom_generate_pb")

        self.gridLayout_7.addWidget(self.nc_bottom_generate_pb, 9, 0, 1, 2)

        self.nc_bottom_spindle_speed_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_spindle_speed_l.setObjectName(u"nc_bottom_spindle_speed_l")

        self.gridLayout_7.addWidget(self.nc_bottom_spindle_speed_l, 4, 0, 1, 1)

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

        self.nc_bottom_cut_z_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_cut_z_l.setObjectName(u"nc_bottom_cut_z_l")

        self.gridLayout_7.addWidget(self.nc_bottom_cut_z_l, 2, 0, 1, 1)

        self.nc_bottom_z_feed_rate_dsb = QDoubleSpinBox(self.nc_area_bottom_page)
        self.nc_bottom_z_feed_rate_dsb.setObjectName(u"nc_bottom_z_feed_rate_dsb")
        self.nc_bottom_z_feed_rate_dsb.setDecimals(2)
        self.nc_bottom_z_feed_rate_dsb.setMinimum(-9999.000000000000000)
        self.nc_bottom_z_feed_rate_dsb.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.nc_bottom_z_feed_rate_dsb, 7, 1, 1, 1)

        self.nc_bottom_overlap_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_overlap_l.setObjectName(u"nc_bottom_overlap_l")

        self.gridLayout_7.addWidget(self.nc_bottom_overlap_l, 1, 0, 1, 1)

        self.nc_bottom_tool_diameter_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_tool_diameter_l.setObjectName(u"nc_bottom_tool_diameter_l")

        self.gridLayout_7.addWidget(self.nc_bottom_tool_diameter_l, 0, 0, 1, 1)

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

        self.nc_bottom_z_feed_rate_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_z_feed_rate_l.setObjectName(u"nc_bottom_z_feed_rate_l")

        self.gridLayout_7.addWidget(self.nc_bottom_z_feed_rate_l, 7, 0, 1, 1)

        self.nc_bottom_xy_feed_rate_l = QLabel(self.nc_area_bottom_page)
        self.nc_bottom_xy_feed_rate_l.setObjectName(u"nc_bottom_xy_feed_rate_l")

        self.gridLayout_7.addWidget(self.nc_bottom_xy_feed_rate_l, 6, 0, 1, 1)

        self.jobs_sw.addWidget(self.nc_area_bottom_page)

        self.verticalLayout_8.addWidget(self.jobs_sw)

        self.prepare_widget.addTab(self.create_job_tab, "")

        self.verticalLayout_2.addWidget(self.prepare_widget)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.viewCanvasWidget = VispyCanvas(self.view_tab)
        self.viewCanvasWidget.setObjectName(u"viewCanvasWidget")
        sizePolicy.setHeightForWidth(self.viewCanvasWidget.sizePolicy().hasHeightForWidth())
        self.viewCanvasWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.viewCanvasWidget)


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
        self.controlsVerticalLayout = QVBoxLayout()
        self.controlsVerticalLayout.setObjectName(u"controlsVerticalLayout")
        self.controlsVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.statusLabel = QLabel(self.control_tab)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy5)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.statusLabel.setFont(font1)
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.controlsVerticalLayout.addWidget(self.statusLabel)

        self.droGridLayout = QGridLayout()
        self.droGridLayout.setObjectName(u"droGridLayout")
        self.droGridLayout.setHorizontalSpacing(0)
        self.droGridLayout.setVerticalSpacing(6)
        self.zAxisLabel = QLabel(self.control_tab)
        self.zAxisLabel.setObjectName(u"zAxisLabel")
        sizePolicy5.setHeightForWidth(self.zAxisLabel.sizePolicy().hasHeightForWidth())
        self.zAxisLabel.setSizePolicy(sizePolicy5)
        self.zAxisLabel.setFont(font)
        self.zAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.zAxisLabel.setFrameShape(QFrame.NoFrame)
        self.zAxisLabel.setFrameShadow(QFrame.Plain)
        self.zAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.zAxisLabel, 0, 3, 1, 1)

        self.label_10 = QLabel(self.control_tab)
        self.label_10.setObjectName(u"label_10")
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setFrameShape(QFrame.NoFrame)
        self.label_10.setFrameShadow(QFrame.Plain)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_10, 2, 1, 1, 1)

        self.zero_z_pushButton = QPushButton(self.control_tab)
        self.zero_z_pushButton.setObjectName(u"zero_z_pushButton")
        self.zero_z_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_z_pushButton, 3, 3, 1, 1)

        self.zero_xyz_pushButton = QPushButton(self.control_tab)
        self.zero_xyz_pushButton.setObjectName(u"zero_xyz_pushButton")
        self.zero_xyz_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_xyz_pushButton, 3, 0, 1, 1)

        self.label_9 = QLabel(self.control_tab)
        self.label_9.setObjectName(u"label_9")
        sizePolicy5.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy5)
        self.label_9.setLayoutDirection(Qt.LeftToRight)
        self.label_9.setFrameShape(QFrame.NoFrame)
        self.label_9.setFrameShadow(QFrame.Plain)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.label_11 = QLabel(self.control_tab)
        self.label_11.setObjectName(u"label_11")
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setLayoutDirection(Qt.LeftToRight)
        self.label_11.setFrameShape(QFrame.NoFrame)
        self.label_11.setFrameShadow(QFrame.Plain)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_11, 2, 3, 1, 1)

        self.zero_y_pushButton = QPushButton(self.control_tab)
        self.zero_y_pushButton.setObjectName(u"zero_y_pushButton")
        self.zero_y_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_y_pushButton, 3, 2, 1, 1)

        self.xAxisLabel = QLabel(self.control_tab)
        self.xAxisLabel.setObjectName(u"xAxisLabel")
        sizePolicy5.setHeightForWidth(self.xAxisLabel.sizePolicy().hasHeightForWidth())
        self.xAxisLabel.setSizePolicy(sizePolicy5)
        self.xAxisLabel.setFont(font)
        self.xAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.xAxisLabel.setFrameShape(QFrame.NoFrame)
        self.xAxisLabel.setFrameShadow(QFrame.Plain)
        self.xAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.xAxisLabel, 0, 1, 1, 1)

        self.zero_x_pushButton = QPushButton(self.control_tab)
        self.zero_x_pushButton.setObjectName(u"zero_x_pushButton")
        self.zero_x_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_x_pushButton, 3, 1, 1, 1)

        self.xAxisLabel_2 = QLabel(self.control_tab)
        self.xAxisLabel_2.setObjectName(u"xAxisLabel_2")
        sizePolicy5.setHeightForWidth(self.xAxisLabel_2.sizePolicy().hasHeightForWidth())
        self.xAxisLabel_2.setSizePolicy(sizePolicy5)
        self.xAxisLabel_2.setFont(font)
        self.xAxisLabel_2.setLayoutDirection(Qt.LeftToRight)
        self.xAxisLabel_2.setFrameShape(QFrame.NoFrame)
        self.xAxisLabel_2.setFrameShadow(QFrame.Plain)
        self.xAxisLabel_2.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.xAxisLabel_2, 0, 0, 1, 1)

        self.yAxisLabel = QLabel(self.control_tab)
        self.yAxisLabel.setObjectName(u"yAxisLabel")
        sizePolicy5.setHeightForWidth(self.yAxisLabel.sizePolicy().hasHeightForWidth())
        self.yAxisLabel.setSizePolicy(sizePolicy5)
        self.yAxisLabel.setFont(font)
        self.yAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.yAxisLabel.setFrameShape(QFrame.NoFrame)
        self.yAxisLabel.setFrameShadow(QFrame.Plain)
        self.yAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.yAxisLabel, 0, 2, 1, 1)

        self.label_12 = QLabel(self.control_tab)
        self.label_12.setObjectName(u"label_12")
        sizePolicy5.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy5)
        self.label_12.setFont(font)
        self.label_12.setLayoutDirection(Qt.LeftToRight)
        self.label_12.setFrameShape(QFrame.NoFrame)
        self.label_12.setFrameShadow(QFrame.Plain)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_12, 2, 0, 1, 1)

        self.mpos_y_label = QLabel(self.control_tab)
        self.mpos_y_label.setObjectName(u"mpos_y_label")
        sizePolicy5.setHeightForWidth(self.mpos_y_label.sizePolicy().hasHeightForWidth())
        self.mpos_y_label.setSizePolicy(sizePolicy5)
        self.mpos_y_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_y_label.setFrameShape(QFrame.NoFrame)
        self.mpos_y_label.setFrameShadow(QFrame.Plain)
        self.mpos_y_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_y_label, 1, 2, 1, 1)

        self.mpos_x_label = QLabel(self.control_tab)
        self.mpos_x_label.setObjectName(u"mpos_x_label")
        sizePolicy5.setHeightForWidth(self.mpos_x_label.sizePolicy().hasHeightForWidth())
        self.mpos_x_label.setSizePolicy(sizePolicy5)
        self.mpos_x_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_x_label.setFrameShape(QFrame.NoFrame)
        self.mpos_x_label.setFrameShadow(QFrame.Plain)
        self.mpos_x_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_x_label, 1, 1, 1, 1)

        self.mpos_z_label = QLabel(self.control_tab)
        self.mpos_z_label.setObjectName(u"mpos_z_label")
        sizePolicy5.setHeightForWidth(self.mpos_z_label.sizePolicy().hasHeightForWidth())
        self.mpos_z_label.setSizePolicy(sizePolicy5)
        self.mpos_z_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_z_label.setFrameShape(QFrame.NoFrame)
        self.mpos_z_label.setFrameShadow(QFrame.Plain)
        self.mpos_z_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_z_label, 1, 3, 1, 1)

        self.label_5 = QLabel(self.control_tab)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(Qt.LeftToRight)
        self.label_5.setFrameShape(QFrame.NoFrame)
        self.label_5.setFrameShadow(QFrame.Plain)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_5, 1, 0, 1, 1)


        self.controlsVerticalLayout.addLayout(self.droGridLayout)

        self.unlockHomingHorizontalLayout = QHBoxLayout()
        self.unlockHomingHorizontalLayout.setObjectName(u"unlockHomingHorizontalLayout")
        self.unlockHomingHorizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.unlockButton = QPushButton(self.control_tab)
        self.unlockButton.setObjectName(u"unlockButton")
        sizePolicy3.setHeightForWidth(self.unlockButton.sizePolicy().hasHeightForWidth())
        self.unlockButton.setSizePolicy(sizePolicy3)
        self.unlockButton.setFont(font)

        self.unlockHomingHorizontalLayout.addWidget(self.unlockButton)

        self.homingButton = QPushButton(self.control_tab)
        self.homingButton.setObjectName(u"homingButton")
        sizePolicy3.setHeightForWidth(self.homingButton.sizePolicy().hasHeightForWidth())
        self.homingButton.setSizePolicy(sizePolicy3)
        self.homingButton.setFont(font)

        self.unlockHomingHorizontalLayout.addWidget(self.homingButton)


        self.controlsVerticalLayout.addLayout(self.unlockHomingHorizontalLayout)

        self.gridLayoutDirections = QGridLayout()
        self.gridLayoutDirections.setObjectName(u"gridLayoutDirections")
        self.gridLayoutDirections.setContentsMargins(5, 5, 5, 5)
        self.xYMinusPlusButton = QPushButton(self.control_tab)
        self.xYMinusPlusButton.setObjectName(u"xYMinusPlusButton")
        sizePolicy3.setHeightForWidth(self.xYMinusPlusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYMinusPlusButton, 0, 0, 1, 1)

        self.yPlusButton = QPushButton(self.control_tab)
        self.yPlusButton.setObjectName(u"yPlusButton")
        sizePolicy3.setHeightForWidth(self.yPlusButton.sizePolicy().hasHeightForWidth())
        self.yPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.yPlusButton, 0, 1, 1, 1)

        self.xYPlusButton = QPushButton(self.control_tab)
        self.xYPlusButton.setObjectName(u"xYPlusButton")
        sizePolicy3.setHeightForWidth(self.xYPlusButton.sizePolicy().hasHeightForWidth())
        self.xYPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYPlusButton, 0, 2, 1, 1)

        self.xMinusButton = QPushButton(self.control_tab)
        self.xMinusButton.setObjectName(u"xMinusButton")
        sizePolicy3.setHeightForWidth(self.xMinusButton.sizePolicy().hasHeightForWidth())
        self.xMinusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xMinusButton, 1, 0, 1, 1)

        self.centerButton = QPushButton(self.control_tab)
        self.centerButton.setObjectName(u"centerButton")
        sizePolicy3.setHeightForWidth(self.centerButton.sizePolicy().hasHeightForWidth())
        self.centerButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.centerButton, 1, 1, 1, 1)

        self.xPlusButton = QPushButton(self.control_tab)
        self.xPlusButton.setObjectName(u"xPlusButton")
        sizePolicy3.setHeightForWidth(self.xPlusButton.sizePolicy().hasHeightForWidth())
        self.xPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xPlusButton, 1, 2, 1, 1)

        self.xYMinusButton = QPushButton(self.control_tab)
        self.xYMinusButton.setObjectName(u"xYMinusButton")
        sizePolicy3.setHeightForWidth(self.xYMinusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYMinusButton, 2, 0, 1, 1)

        self.yMinusButton = QPushButton(self.control_tab)
        self.yMinusButton.setObjectName(u"yMinusButton")
        sizePolicy3.setHeightForWidth(self.yMinusButton.sizePolicy().hasHeightForWidth())
        self.yMinusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.yMinusButton, 2, 1, 1, 1)

        self.xYPlusMinuButton = QPushButton(self.control_tab)
        self.xYPlusMinuButton.setObjectName(u"xYPlusMinuButton")
        sizePolicy3.setHeightForWidth(self.xYPlusMinuButton.sizePolicy().hasHeightForWidth())
        self.xYPlusMinuButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYPlusMinuButton, 2, 2, 1, 1)


        self.controlsVerticalLayout.addLayout(self.gridLayoutDirections)

        self.xyzIncrementsHorizontalLayout = QHBoxLayout()
        self.xyzIncrementsHorizontalLayout.setObjectName(u"xyzIncrementsHorizontalLayout")
        self.xyzIncrementsHorizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_3 = QLabel(self.control_tab)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_3, 0, Qt.AlignHCenter)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.control_tab)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy3.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy3)

        self.verticalLayout_5.addWidget(self.doubleSpinBox_2, 0, Qt.AlignHCenter)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.control_tab)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_4, 0, Qt.AlignHCenter)

        self.doubleSpinBox = QDoubleSpinBox(self.control_tab)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        sizePolicy3.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.doubleSpinBox, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.zPlusButton = QPushButton(self.control_tab)
        self.zPlusButton.setObjectName(u"zPlusButton")
        sizePolicy3.setHeightForWidth(self.zPlusButton.sizePolicy().hasHeightForWidth())
        self.zPlusButton.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.zPlusButton)

        self.zMinusButton = QPushButton(self.control_tab)
        self.zMinusButton.setObjectName(u"zMinusButton")
        sizePolicy3.setHeightForWidth(self.zMinusButton.sizePolicy().hasHeightForWidth())
        self.zMinusButton.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.zMinusButton)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_3)

        self.xyzIncrementsHorizontalLayout.setStretch(0, 3)
        self.xyzIncrementsHorizontalLayout.setStretch(1, 3)
        self.xyzIncrementsHorizontalLayout.setStretch(2, 1)

        self.controlsVerticalLayout.addLayout(self.xyzIncrementsHorizontalLayout)

        self.terminalVerticalLayout = QVBoxLayout()
        self.terminalVerticalLayout.setObjectName(u"terminalVerticalLayout")
        self.serial_te = QTextEdit(self.control_tab)
        self.serial_te.setObjectName(u"serial_te")
        self.serial_te.setEnabled(True)
        self.serial_te.setFrameShadow(QFrame.Sunken)
        self.serial_te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.terminalVerticalLayout.addWidget(self.serial_te)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.send_text_edit = QLineEdit(self.control_tab)
        self.send_text_edit.setObjectName(u"send_text_edit")

        self.horizontalLayout_2.addWidget(self.send_text_edit)

        self.send_push_button = QPushButton(self.control_tab)
        self.send_push_button.setObjectName(u"send_push_button")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.send_push_button.sizePolicy().hasHeightForWidth())
        self.send_push_button.setSizePolicy(sizePolicy6)
        self.send_push_button.setFont(font)

        self.horizontalLayout_2.addWidget(self.send_push_button)


        self.terminalVerticalLayout.addLayout(self.horizontalLayout_2)

        self.connectVerticalLayout = QVBoxLayout()
        self.connectVerticalLayout.setSpacing(6)
        self.connectVerticalLayout.setObjectName(u"connectVerticalLayout")
        self.connectVerticalLayout.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serial_ports_cb = QComboBox(self.control_tab)
        self.serial_ports_cb.setObjectName(u"serial_ports_cb")
        sizePolicy2.setHeightForWidth(self.serial_ports_cb.sizePolicy().hasHeightForWidth())
        self.serial_ports_cb.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.serial_ports_cb)

        self.serial_baud_cb = QComboBox(self.control_tab)
        self.serial_baud_cb.setObjectName(u"serial_baud_cb")
        sizePolicy2.setHeightForWidth(self.serial_baud_cb.sizePolicy().hasHeightForWidth())
        self.serial_baud_cb.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.serial_baud_cb)

        self.refresh_button = QPushButton(self.control_tab)
        self.refresh_button.setObjectName(u"refresh_button")
        sizePolicy6.setHeightForWidth(self.refresh_button.sizePolicy().hasHeightForWidth())
        self.refresh_button.setSizePolicy(sizePolicy6)
        self.refresh_button.setFont(font)
        self.refresh_button.setCheckable(False)

        self.horizontalLayout.addWidget(self.refresh_button)


        self.connectVerticalLayout.addLayout(self.horizontalLayout)


        self.terminalVerticalLayout.addLayout(self.connectVerticalLayout)

        self.splitter_2 = QSplitter(self.control_tab)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.autoscroll_chb = QCheckBox(self.splitter_2)
        self.autoscroll_chb.setObjectName(u"autoscroll_chb")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.autoscroll_chb.sizePolicy().hasHeightForWidth())
        self.autoscroll_chb.setSizePolicy(sizePolicy7)
        self.autoscroll_chb.setFont(font)
        self.autoscroll_chb.setChecked(True)
        self.splitter_2.addWidget(self.autoscroll_chb)
        self.clear_terminal_button = QPushButton(self.splitter_2)
        self.clear_terminal_button.setObjectName(u"clear_terminal_button")
        self.clear_terminal_button.setEnabled(True)
        sizePolicy7.setHeightForWidth(self.clear_terminal_button.sizePolicy().hasHeightForWidth())
        self.clear_terminal_button.setSizePolicy(sizePolicy7)
        self.clear_terminal_button.setFont(font)
        self.splitter_2.addWidget(self.clear_terminal_button)
        self.connect_button = QPushButton(self.splitter_2)
        self.connect_button.setObjectName(u"connect_button")
        sizePolicy3.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy3)
        self.connect_button.setFont(font)
        self.splitter_2.addWidget(self.connect_button)

        self.terminalVerticalLayout.addWidget(self.splitter_2)


        self.controlsVerticalLayout.addLayout(self.terminalVerticalLayout)


        self.horizontalLayout_4.addLayout(self.controlsVerticalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.openGLWidget = QOpenGLWidget(self.control_tab)
        self.openGLWidget.setObjectName(u"openGLWidget")
        sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.openGLWidget)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 10)

        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)

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

        self.verticalLayout_6.addWidget(self.main_tab_widget)

        self.logging_plain_te = QPlainTextEdit(self.central_widget)
        self.logging_plain_te.setObjectName(u"logging_plain_te")
        sizePolicy5.setHeightForWidth(self.logging_plain_te.sizePolicy().hasHeightForWidth())
        self.logging_plain_te.setSizePolicy(sizePolicy5)
        self.logging_plain_te.setMaximumSize(QSize(16777215, 100))
        self.logging_plain_te.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.logging_plain_te)

        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1039, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuConsole = QMenu(self.menubar)
        self.menuConsole.setObjectName(u"menuConsole")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConsole.menuAction())
        self.menuFile.addAction(self.actionLoad)
        self.menuConsole.addAction(self.actionHide_Show_Console)

        self.retranslateUi(MainWindow)

        self.main_tab_widget.setCurrentIndex(0)
        self.prepare_widget.setCurrentIndex(0)
        self.jobs_sw.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"newCNC", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionLoad.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionHide_Show_Console.setText(QCoreApplication.translate("MainWindow", u"Hide/Show Console", None))
#if QT_CONFIG(shortcut)
        self.actionHide_Show_Console.setShortcut(QCoreApplication.translate("MainWindow", u"F4", None))
#endif // QT_CONFIG(shortcut)
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
        self.top_tool_diameter_l.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.top_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.top_n_passes_l.setText(QCoreApplication.translate("MainWindow", u"Number of Passes", None))
        self.top_travel_z_l.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.top_cut_z_l.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.top_overlap_l.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.top_spindle_speed_l.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.top_xy_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.top_z_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.bottom_z_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.bottom_overlap_l.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.bottom_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.bottom_tool_diameter_l.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.bottom_n_passes_l.setText(QCoreApplication.translate("MainWindow", u"Number of Passes", None))
        self.bottom_travel_z_l.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.bottom_cut_z_l.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.bottom_xy_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.bottom_spindle_speed_l.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.profile_depth_pass_l.setText(QCoreApplication.translate("MainWindow", u"Depth per Pass [mm]", None))
        self.profile_taps_layout_l.setText(QCoreApplication.translate("MainWindow", u"Taps layout", None))
        self.profile_margin_l.setText(QCoreApplication.translate("MainWindow", u"Margin [mm]", None))
        self.profile_cut_z_l.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.profile_xy_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.profile_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.profile_tool_diameter_l.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.profile_multi_depth_chb.setText("")
        self.profile_z_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.profile_tap_size_l.setText(QCoreApplication.translate("MainWindow", u"Tap size [mm]", None))
        self.profile_travel_z_l.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.profile_multi_depth_l.setText(QCoreApplication.translate("MainWindow", u"Multi-depth", None))
        self.profile_spindle_speed_l.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        ___qtablewidgetitem = self.drill_tw.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Bit", None));
        ___qtablewidgetitem1 = self.drill_tw.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Diameter [mm]", None));
        self.drill_cut_z_l.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.drill_tool_diameter_l.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.drill_generate_job_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.drill_travel_z_l.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.drill_milling_tool_.setText(QCoreApplication.translate("MainWindow", u"Milling Tool", None))
        self.drill_xy_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.drill_z_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.drill_milling_tool_chb.setText("")
        self.drill_spindle_speed_l.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.nc_top_overlap_l.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.nc_top_cut_z_l.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.nc_top_spindle_speed_l.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.nc_top_tool_diameter_l.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.nc_top_travel_z_l.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.nc_top_z_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.nc_top_xy_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.nc_top_generate_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.nc_bottom_travel_z_l.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.nc_bottom_generate_pb.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.nc_bottom_spindle_speed_l.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.nc_bottom_cut_z_l.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.nc_bottom_overlap_l.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.nc_bottom_tool_diameter_l.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.nc_bottom_z_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.nc_bottom_xy_feed_rate_l.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.prepare_widget.setTabText(self.prepare_widget.indexOf(self.create_job_tab), QCoreApplication.translate("MainWindow", u"CREATE JOB", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.view_tab), QCoreApplication.translate("MainWindow", u"VIEW", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.zAxisLabel.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.zero_z_pushButton.setText(QCoreApplication.translate("MainWindow", u"Z = 0", None))
        self.zero_xyz_pushButton.setText(QCoreApplication.translate("MainWindow", u"XYZ = 0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.zero_y_pushButton.setText(QCoreApplication.translate("MainWindow", u"Y = 0", None))
        self.xAxisLabel.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.zero_x_pushButton.setText(QCoreApplication.translate("MainWindow", u"X = 0", None))
        self.xAxisLabel_2.setText(QCoreApplication.translate("MainWindow", u"Axis:", None))
        self.yAxisLabel.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"WPos", None))
        self.mpos_y_label.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mpos_x_label.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mpos_z_label.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"MPos", None))
        self.unlockButton.setText(QCoreApplication.translate("MainWindow", u"Unlock", None))
        self.homingButton.setText(QCoreApplication.translate("MainWindow", u"Homing", None))
        self.xYMinusPlusButton.setText(QCoreApplication.translate("MainWindow", u"X- Y+", None))
        self.yPlusButton.setText(QCoreApplication.translate("MainWindow", u"Y+", None))
        self.xYPlusButton.setText(QCoreApplication.translate("MainWindow", u"X+ Y+", None))
        self.xMinusButton.setText(QCoreApplication.translate("MainWindow", u"X-", None))
        self.centerButton.setText(QCoreApplication.translate("MainWindow", u"Center", None))
        self.xPlusButton.setText(QCoreApplication.translate("MainWindow", u"X+", None))
        self.xYMinusButton.setText(QCoreApplication.translate("MainWindow", u"X- Y-", None))
        self.yMinusButton.setText(QCoreApplication.translate("MainWindow", u"Y-", None))
        self.xYPlusMinuButton.setText(QCoreApplication.translate("MainWindow", u"X+ Y-", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"XY", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.zPlusButton.setText(QCoreApplication.translate("MainWindow", u"Z+", None))
        self.zMinusButton.setText(QCoreApplication.translate("MainWindow", u"Z-", None))
        self.send_push_button.setText(QCoreApplication.translate("MainWindow", u"Send", None))
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
#if QT_CONFIG(tooltip)
        self.refresh_button.setToolTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.refresh_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(statustip)
        self.refresh_button.setText(QCoreApplication.translate("MainWindow", u"Serial Ports Refresh", None))
        self.autoscroll_chb.setText(QCoreApplication.translate("MainWindow", u"Autoscroll", None))
        self.clear_terminal_button.setText(QCoreApplication.translate("MainWindow", u"Clear Terminal", None))
#if QT_CONFIG(tooltip)
        self.connect_button.setToolTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.connect_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(statustip)
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.control_tab), QCoreApplication.translate("MainWindow", u"CONTROL", None))
        self.label_2.setText("")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.align_tab), QCoreApplication.translate("MainWindow", u"ALIGN", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuConsole.setTitle(QCoreApplication.translate("MainWindow", u"Console", None))
    # retranslateUi

