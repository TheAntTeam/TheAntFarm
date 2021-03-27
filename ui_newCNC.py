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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.viewTab = QWidget()
        self.viewTab.setObjectName(u"viewTab")
        self.viewTab.setFont(font)
        self.horizontalLayout_8 = QHBoxLayout(self.viewTab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget_2 = QTabWidget(self.viewTab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy1)
        self.tabWidget_2.setTabPosition(QTabWidget.South)
        self.tabWidget_2.setTabShape(QTabWidget.Triangular)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_7 = QVBoxLayout(self.tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.no_copper_1_le = QLineEdit(self.tab)
        self.no_copper_1_le.setObjectName(u"no_copper_1_le")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.no_copper_1_le.sizePolicy().hasHeightForWidth())
        self.no_copper_1_le.setSizePolicy(sizePolicy2)
        self.no_copper_1_le.setReadOnly(True)

        self.gridLayout.addWidget(self.no_copper_1_le, 5, 0, 1, 1)

        self.no_copper_2_pb = QPushButton(self.tab)
        self.no_copper_2_pb.setObjectName(u"no_copper_2_pb")
        sizePolicy2.setHeightForWidth(self.no_copper_2_pb.sizePolicy().hasHeightForWidth())
        self.no_copper_2_pb.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.no_copper_2_pb, 6, 1, 1, 1)

        self.no_copper_2_chb = QCheckBox(self.tab)
        self.no_copper_2_chb.setObjectName(u"no_copper_2_chb")
        sizePolicy2.setHeightForWidth(self.no_copper_2_chb.sizePolicy().hasHeightForWidth())
        self.no_copper_2_chb.setSizePolicy(sizePolicy2)
        self.no_copper_2_chb.setChecked(True)

        self.gridLayout.addWidget(self.no_copper_2_chb, 6, 2, 1, 1, Qt.AlignHCenter)

        self.profileFileLineEdit = QLineEdit(self.tab)
        self.profileFileLineEdit.setObjectName(u"profileFileLineEdit")
        sizePolicy2.setHeightForWidth(self.profileFileLineEdit.sizePolicy().hasHeightForWidth())
        self.profileFileLineEdit.setSizePolicy(sizePolicy2)
        self.profileFileLineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.profileFileLineEdit, 3, 0, 1, 1)

        self.viewLabel = QLabel(self.tab)
        self.viewLabel.setObjectName(u"viewLabel")
        sizePolicy2.setHeightForWidth(self.viewLabel.sizePolicy().hasHeightForWidth())
        self.viewLabel.setSizePolicy(sizePolicy2)
        self.viewLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.viewLabel, 0, 2, 1, 1, Qt.AlignHCenter)

        self.topViewCheckBox = QCheckBox(self.tab)
        self.topViewCheckBox.setObjectName(u"topViewCheckBox")
        sizePolicy2.setHeightForWidth(self.topViewCheckBox.sizePolicy().hasHeightForWidth())
        self.topViewCheckBox.setSizePolicy(sizePolicy2)
        self.topViewCheckBox.setChecked(True)
        self.topViewCheckBox.setTristate(False)

        self.gridLayout.addWidget(self.topViewCheckBox, 1, 2, 1, 1, Qt.AlignHCenter)

        self.drillFileLineEdit = QLineEdit(self.tab)
        self.drillFileLineEdit.setObjectName(u"drillFileLineEdit")
        sizePolicy2.setHeightForWidth(self.drillFileLineEdit.sizePolicy().hasHeightForWidth())
        self.drillFileLineEdit.setSizePolicy(sizePolicy2)
        self.drillFileLineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.drillFileLineEdit, 4, 0, 1, 1)

        self.no_copper_1_pb = QPushButton(self.tab)
        self.no_copper_1_pb.setObjectName(u"no_copper_1_pb")
        sizePolicy2.setHeightForWidth(self.no_copper_1_pb.sizePolicy().hasHeightForWidth())
        self.no_copper_1_pb.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.no_copper_1_pb, 5, 1, 1, 1)

        self.bottomViewCheckBox = QCheckBox(self.tab)
        self.bottomViewCheckBox.setObjectName(u"bottomViewCheckBox")
        sizePolicy2.setHeightForWidth(self.bottomViewCheckBox.sizePolicy().hasHeightForWidth())
        self.bottomViewCheckBox.setSizePolicy(sizePolicy2)
        self.bottomViewCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.bottomViewCheckBox, 2, 2, 1, 1, Qt.AlignHCenter)

        self.profileLoadButton = QPushButton(self.tab)
        self.profileLoadButton.setObjectName(u"profileLoadButton")
        sizePolicy2.setHeightForWidth(self.profileLoadButton.sizePolicy().hasHeightForWidth())
        self.profileLoadButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.profileLoadButton, 3, 1, 1, 1)

        self.no_copper_2_le = QLineEdit(self.tab)
        self.no_copper_2_le.setObjectName(u"no_copper_2_le")
        sizePolicy2.setHeightForWidth(self.no_copper_2_le.sizePolicy().hasHeightForWidth())
        self.no_copper_2_le.setSizePolicy(sizePolicy2)
        self.no_copper_2_le.setReadOnly(True)

        self.gridLayout.addWidget(self.no_copper_2_le, 6, 0, 1, 1)

        self.no_copper_1_chb = QCheckBox(self.tab)
        self.no_copper_1_chb.setObjectName(u"no_copper_1_chb")
        sizePolicy2.setHeightForWidth(self.no_copper_1_chb.sizePolicy().hasHeightForWidth())
        self.no_copper_1_chb.setSizePolicy(sizePolicy2)
        self.no_copper_1_chb.setChecked(True)

        self.gridLayout.addWidget(self.no_copper_1_chb, 5, 2, 1, 1, Qt.AlignHCenter)

        self.clear_views_push_button = QPushButton(self.tab)
        self.clear_views_push_button.setObjectName(u"clear_views_push_button")
        sizePolicy2.setHeightForWidth(self.clear_views_push_button.sizePolicy().hasHeightForWidth())
        self.clear_views_push_button.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.clear_views_push_button, 8, 1, 1, 1)

        self.drillLoadButton = QPushButton(self.tab)
        self.drillLoadButton.setObjectName(u"drillLoadButton")
        sizePolicy2.setHeightForWidth(self.drillLoadButton.sizePolicy().hasHeightForWidth())
        self.drillLoadButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.drillLoadButton, 4, 1, 1, 1)

        self.topLoadButton = QPushButton(self.tab)
        self.topLoadButton.setObjectName(u"topLoadButton")
        sizePolicy2.setHeightForWidth(self.topLoadButton.sizePolicy().hasHeightForWidth())
        self.topLoadButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.topLoadButton, 1, 1, 1, 1)

        self.bottomFileLineEdit = QLineEdit(self.tab)
        self.bottomFileLineEdit.setObjectName(u"bottomFileLineEdit")
        sizePolicy2.setHeightForWidth(self.bottomFileLineEdit.sizePolicy().hasHeightForWidth())
        self.bottomFileLineEdit.setSizePolicy(sizePolicy2)
        self.bottomFileLineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.bottomFileLineEdit, 2, 0, 1, 1)

        self.bottomLoadButton = QPushButton(self.tab)
        self.bottomLoadButton.setObjectName(u"bottomLoadButton")
        sizePolicy2.setHeightForWidth(self.bottomLoadButton.sizePolicy().hasHeightForWidth())
        self.bottomLoadButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.bottomLoadButton, 2, 1, 1, 1)

        self.drillViewCheckBox = QCheckBox(self.tab)
        self.drillViewCheckBox.setObjectName(u"drillViewCheckBox")
        sizePolicy2.setHeightForWidth(self.drillViewCheckBox.sizePolicy().hasHeightForWidth())
        self.drillViewCheckBox.setSizePolicy(sizePolicy2)
        self.drillViewCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.drillViewCheckBox, 4, 2, 1, 1, Qt.AlignHCenter)

        self.filePathLabel = QLabel(self.tab)
        self.filePathLabel.setObjectName(u"filePathLabel")
        sizePolicy2.setHeightForWidth(self.filePathLabel.sizePolicy().hasHeightForWidth())
        self.filePathLabel.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.filePathLabel, 0, 0, 1, 1, Qt.AlignHCenter)

        self.topFileLineEdit = QLineEdit(self.tab)
        self.topFileLineEdit.setObjectName(u"topFileLineEdit")
        sizePolicy2.setHeightForWidth(self.topFileLineEdit.sizePolicy().hasHeightForWidth())
        self.topFileLineEdit.setSizePolicy(sizePolicy2)
        self.topFileLineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.topFileLineEdit, 1, 0, 1, 1)

        self.all_view_checkbox = QCheckBox(self.tab)
        self.all_view_checkbox.setObjectName(u"all_view_checkbox")
        sizePolicy2.setHeightForWidth(self.all_view_checkbox.sizePolicy().hasHeightForWidth())
        self.all_view_checkbox.setSizePolicy(sizePolicy2)
        self.all_view_checkbox.setChecked(True)

        self.gridLayout.addWidget(self.all_view_checkbox, 8, 2, 1, 1, Qt.AlignHCenter)

        self.profileViewCheckBox = QCheckBox(self.tab)
        self.profileViewCheckBox.setObjectName(u"profileViewCheckBox")
        sizePolicy2.setHeightForWidth(self.profileViewCheckBox.sizePolicy().hasHeightForWidth())
        self.profileViewCheckBox.setSizePolicy(sizePolicy2)
        self.profileViewCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.profileViewCheckBox, 3, 2, 1, 1, Qt.AlignHCenter)

        self.horizontalSpacer = QSpacerItem(140, 17, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 8, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 7, 0, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.tabWidget_2.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_8 = QVBoxLayout(self.tab_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.layer_choice_cb = QComboBox(self.tab_2)
        self.layer_choice_cb.setObjectName(u"layer_choice_cb")

        self.verticalLayout_8.addWidget(self.layer_choice_cb)

        self.jobs_sw = QStackedWidget(self.tab_2)
        self.jobs_sw.setObjectName(u"jobs_sw")
        self.top_page = QWidget()
        self.top_page.setObjectName(u"top_page")
        self.gridLayout_2 = QGridLayout(self.top_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.doubleSpinBox_6 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        self.doubleSpinBox_6.setDecimals(2)
        self.doubleSpinBox_6.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_6.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_6, 3, 1, 1, 1)

        self.label_7 = QLabel(self.top_page)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.top_page)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 11, 0, 1, 2)

        self.label_8 = QLabel(self.top_page)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 10, 0, 1, 2)

        self.label_15 = QLabel(self.top_page)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 4, 0, 1, 1)

        self.doubleSpinBox_7 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_7.setObjectName(u"doubleSpinBox_7")
        self.doubleSpinBox_7.setDecimals(2)
        self.doubleSpinBox_7.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_7.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_7, 4, 1, 1, 1)

        self.label_14 = QLabel(self.top_page)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_13 = QLabel(self.top_page)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_29 = QLabel(self.top_page)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_2.addWidget(self.label_29, 6, 0, 1, 1)

        self.doubleSpinBox_21 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_21.setObjectName(u"doubleSpinBox_21")
        self.doubleSpinBox_21.setDecimals(2)
        self.doubleSpinBox_21.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_21.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_21, 7, 1, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setMinimum(0.010000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_4, 0, 1, 1, 1)

        self.label_30 = QLabel(self.top_page)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_2.addWidget(self.label_30, 7, 0, 1, 1)

        self.spinBox = QSpinBox(self.top_page)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)

        self.gridLayout_2.addWidget(self.spinBox, 1, 1, 1, 1)

        self.doubleSpinBox_20 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_20.setObjectName(u"doubleSpinBox_20")
        self.doubleSpinBox_20.setDecimals(2)
        self.doubleSpinBox_20.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_20.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_20, 6, 1, 1, 1)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        self.doubleSpinBox_5.setDecimals(1)
        self.doubleSpinBox_5.setMinimum(0.000000000000000)
        self.doubleSpinBox_5.setMaximum(1.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_5, 2, 1, 1, 1)

        self.label_31 = QLabel(self.top_page)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_2.addWidget(self.label_31, 9, 0, 1, 1)

        self.doubleSpinBox_22 = QDoubleSpinBox(self.top_page)
        self.doubleSpinBox_22.setObjectName(u"doubleSpinBox_22")
        self.doubleSpinBox_22.setDecimals(2)
        self.doubleSpinBox_22.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_22.setMaximum(9999.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_22, 9, 1, 1, 1)

        self.jobs_sw.addWidget(self.top_page)
        self.bottom_page = QWidget()
        self.bottom_page.setObjectName(u"bottom_page")
        self.gridLayout_3 = QGridLayout(self.bottom_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_32 = QLabel(self.bottom_page)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_3.addWidget(self.label_32, 9, 0, 1, 1)

        self.doubleSpinBox_10 = QDoubleSpinBox(self.bottom_page)
        self.doubleSpinBox_10.setObjectName(u"doubleSpinBox_10")
        self.doubleSpinBox_10.setDecimals(2)
        self.doubleSpinBox_10.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_10.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_10, 4, 1, 1, 1)

        self.doubleSpinBox_23 = QDoubleSpinBox(self.bottom_page)
        self.doubleSpinBox_23.setObjectName(u"doubleSpinBox_23")
        self.doubleSpinBox_23.setDecimals(2)
        self.doubleSpinBox_23.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_23.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_23, 9, 1, 1, 1)

        self.doubleSpinBox_8 = QDoubleSpinBox(self.bottom_page)
        self.doubleSpinBox_8.setObjectName(u"doubleSpinBox_8")
        self.doubleSpinBox_8.setMinimum(0.010000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_8, 1, 1, 1, 1)

        self.spinBox_2 = QSpinBox(self.bottom_page)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimum(1)

        self.gridLayout_3.addWidget(self.spinBox_2, 2, 1, 1, 1)

        self.label_18 = QLabel(self.bottom_page)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 3, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.bottom_page)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_3.addWidget(self.pushButton_2, 12, 0, 1, 2)

        self.doubleSpinBox_24 = QDoubleSpinBox(self.bottom_page)
        self.doubleSpinBox_24.setObjectName(u"doubleSpinBox_24")
        self.doubleSpinBox_24.setDecimals(2)
        self.doubleSpinBox_24.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_24.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_24, 8, 1, 1, 1)

        self.doubleSpinBox_9 = QDoubleSpinBox(self.bottom_page)
        self.doubleSpinBox_9.setObjectName(u"doubleSpinBox_9")
        self.doubleSpinBox_9.setDecimals(1)
        self.doubleSpinBox_9.setMinimum(0.000000000000000)
        self.doubleSpinBox_9.setMaximum(1.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_9, 3, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 11, 0, 1, 2)

        self.label_16 = QLabel(self.bottom_page)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 1, 0, 1, 1)

        self.label_17 = QLabel(self.bottom_page)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 2, 0, 1, 1)

        self.label_20 = QLabel(self.bottom_page)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_3.addWidget(self.label_20, 5, 0, 1, 1)

        self.label_19 = QLabel(self.bottom_page)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_3.addWidget(self.label_19, 4, 0, 1, 1)

        self.doubleSpinBox_11 = QDoubleSpinBox(self.bottom_page)
        self.doubleSpinBox_11.setObjectName(u"doubleSpinBox_11")
        self.doubleSpinBox_11.setDecimals(2)
        self.doubleSpinBox_11.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_11.setMaximum(9999.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_11, 5, 1, 1, 1)

        self.label_33 = QLabel(self.bottom_page)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_3.addWidget(self.label_33, 8, 0, 1, 1)

        self.jobs_sw.addWidget(self.bottom_page)
        self.profile_page = QWidget()
        self.profile_page.setObjectName(u"profile_page")
        self.gridLayout_4 = QGridLayout(self.profile_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_23 = QLabel(self.profile_page)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_4.addWidget(self.label_23, 3, 1, 1, 1)

        self.doubleSpinBox_25 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_25.setObjectName(u"doubleSpinBox_25")
        self.doubleSpinBox_25.setDecimals(2)
        self.doubleSpinBox_25.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_25.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_25, 7, 3, 1, 1)

        self.doubleSpinBox_16 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_16.setObjectName(u"doubleSpinBox_16")
        self.doubleSpinBox_16.setDecimals(2)
        self.doubleSpinBox_16.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_16.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_16, 5, 3, 1, 1)

        self.doubleSpinBox_13 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_13.setObjectName(u"doubleSpinBox_13")
        self.doubleSpinBox_13.setDecimals(2)
        self.doubleSpinBox_13.setMinimum(0.000000000000000)
        self.doubleSpinBox_13.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_13, 1, 3, 1, 1)

        self.doubleSpinBox_14 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_14.setObjectName(u"doubleSpinBox_14")
        self.doubleSpinBox_14.setDecimals(2)
        self.doubleSpinBox_14.setMinimum(0.000000000000000)
        self.doubleSpinBox_14.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_14, 3, 3, 1, 1)

        self.label_52 = QLabel(self.profile_page)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_4.addWidget(self.label_52, 9, 1, 1, 1)

        self.label_22 = QLabel(self.profile_page)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_4.addWidget(self.label_22, 1, 1, 1, 1)

        self.label_25 = QLabel(self.profile_page)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_4.addWidget(self.label_25, 5, 1, 1, 1)

        self.label_34 = QLabel(self.profile_page)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_4.addWidget(self.label_34, 7, 1, 1, 1)

        self.doubleSpinBox_26 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_26.setObjectName(u"doubleSpinBox_26")
        self.doubleSpinBox_26.setDecimals(2)
        self.doubleSpinBox_26.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_26.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_26, 8, 3, 1, 1)

        self.pushButton_3 = QPushButton(self.profile_page)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_4.addWidget(self.pushButton_3, 14, 1, 1, 3)

        self.label_21 = QLabel(self.profile_page)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_4.addWidget(self.label_21, 0, 1, 1, 1)

        self.checkBox = QCheckBox(self.profile_page)
        self.checkBox.setObjectName(u"checkBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy3)
        self.checkBox.setMinimumSize(QSize(123, 0))

        self.gridLayout_4.addWidget(self.checkBox, 2, 3, 1, 1, Qt.AlignHCenter)

        self.label_35 = QLabel(self.profile_page)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_4.addWidget(self.label_35, 8, 1, 1, 1)

        self.doubleSpinBox_12 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_12.setObjectName(u"doubleSpinBox_12")
        self.doubleSpinBox_12.setMinimum(0.010000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_12, 0, 3, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 13, 1, 1, 3)

        self.label_24 = QLabel(self.profile_page)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_4.addWidget(self.label_24, 6, 1, 1, 1)

        self.doubleSpinBox_15 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_15.setObjectName(u"doubleSpinBox_15")
        self.doubleSpinBox_15.setDecimals(2)
        self.doubleSpinBox_15.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_15.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_15, 6, 3, 1, 1)

        self.comboBox = QComboBox(self.profile_page)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_4.addWidget(self.comboBox, 9, 3, 1, 1)

        self.label = QLabel(self.profile_page)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 2, 1, 1, 1)

        self.label_53 = QLabel(self.profile_page)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_4.addWidget(self.label_53, 10, 1, 1, 1)

        self.doubleSpinBox_43 = QDoubleSpinBox(self.profile_page)
        self.doubleSpinBox_43.setObjectName(u"doubleSpinBox_43")
        self.doubleSpinBox_43.setDecimals(2)
        self.doubleSpinBox_43.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_43.setMaximum(9999.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_43, 10, 3, 1, 1)

        self.jobs_sw.addWidget(self.profile_page)
        self.drill_page = QWidget()
        self.drill_page.setObjectName(u"drill_page")
        self.gridLayout_5 = QGridLayout(self.drill_page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tableWidget = QTableWidget(self.drill_page)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout_5.addWidget(self.tableWidget, 0, 1, 1, 2)

        self.doubleSpinBox_19 = QDoubleSpinBox(self.drill_page)
        self.doubleSpinBox_19.setObjectName(u"doubleSpinBox_19")
        self.doubleSpinBox_19.setDecimals(2)
        self.doubleSpinBox_19.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_19.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.doubleSpinBox_19, 5, 2, 1, 1)

        self.label_27 = QLabel(self.drill_page)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_5.addWidget(self.label_27, 4, 1, 1, 1)

        self.label_26 = QLabel(self.drill_page)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_5.addWidget(self.label_26, 2, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.drill_page)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_5.addWidget(self.pushButton_4, 11, 1, 1, 2)

        self.doubleSpinBox_27 = QDoubleSpinBox(self.drill_page)
        self.doubleSpinBox_27.setObjectName(u"doubleSpinBox_27")
        self.doubleSpinBox_27.setDecimals(2)
        self.doubleSpinBox_27.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_27.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.doubleSpinBox_27, 6, 2, 1, 1)

        self.label_28 = QLabel(self.drill_page)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_5.addWidget(self.label_28, 5, 1, 1, 1)

        self.label_6 = QLabel(self.drill_page)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_5.addWidget(self.label_6, 1, 1, 1, 1)

        self.doubleSpinBox_17 = QDoubleSpinBox(self.drill_page)
        self.doubleSpinBox_17.setObjectName(u"doubleSpinBox_17")
        self.doubleSpinBox_17.setMinimum(0.010000000000000)

        self.gridLayout_5.addWidget(self.doubleSpinBox_17, 2, 2, 1, 1)

        self.label_36 = QLabel(self.drill_page)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_5.addWidget(self.label_36, 6, 1, 1, 1)

        self.checkBox_2 = QCheckBox(self.drill_page)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_5.addWidget(self.checkBox_2, 1, 2, 1, 1)

        self.doubleSpinBox_18 = QDoubleSpinBox(self.drill_page)
        self.doubleSpinBox_18.setObjectName(u"doubleSpinBox_18")
        self.doubleSpinBox_18.setDecimals(2)
        self.doubleSpinBox_18.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_18.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.doubleSpinBox_18, 4, 2, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_5, 10, 1, 1, 2)

        self.label_37 = QLabel(self.drill_page)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_5.addWidget(self.label_37, 8, 1, 1, 1)

        self.doubleSpinBox_28 = QDoubleSpinBox(self.drill_page)
        self.doubleSpinBox_28.setObjectName(u"doubleSpinBox_28")
        self.doubleSpinBox_28.setDecimals(2)
        self.doubleSpinBox_28.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_28.setMaximum(9999.000000000000000)

        self.gridLayout_5.addWidget(self.doubleSpinBox_28, 8, 2, 1, 1)

        self.jobs_sw.addWidget(self.drill_page)
        self.nc_area_top_page = QWidget()
        self.nc_area_top_page.setObjectName(u"nc_area_top_page")
        self.gridLayout_6 = QGridLayout(self.nc_area_top_page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_39 = QLabel(self.nc_area_top_page)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_6.addWidget(self.label_39, 1, 0, 1, 1)

        self.label_41 = QLabel(self.nc_area_top_page)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_6.addWidget(self.label_41, 2, 0, 1, 1)

        self.doubleSpinBox_34 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_34.setObjectName(u"doubleSpinBox_34")
        self.doubleSpinBox_34.setDecimals(2)
        self.doubleSpinBox_34.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_34.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_34, 5, 1, 1, 1)

        self.doubleSpinBox_32 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_32.setObjectName(u"doubleSpinBox_32")
        self.doubleSpinBox_32.setDecimals(2)
        self.doubleSpinBox_32.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_32.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_32, 3, 1, 1, 1)

        self.label_42 = QLabel(self.nc_area_top_page)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_6.addWidget(self.label_42, 4, 0, 1, 1)

        self.label_38 = QLabel(self.nc_area_top_page)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_6.addWidget(self.label_38, 0, 0, 1, 1)

        self.doubleSpinBox_31 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_31.setObjectName(u"doubleSpinBox_31")
        self.doubleSpinBox_31.setDecimals(2)
        self.doubleSpinBox_31.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_31.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_31, 2, 1, 1, 1)

        self.label_40 = QLabel(self.nc_area_top_page)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_6.addWidget(self.label_40, 3, 0, 1, 1)

        self.label_44 = QLabel(self.nc_area_top_page)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_6.addWidget(self.label_44, 6, 0, 1, 1)

        self.doubleSpinBox_30 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_30.setObjectName(u"doubleSpinBox_30")
        self.doubleSpinBox_30.setMinimum(0.010000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_30, 0, 1, 1, 1)

        self.doubleSpinBox_33 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_33.setObjectName(u"doubleSpinBox_33")
        self.doubleSpinBox_33.setDecimals(2)
        self.doubleSpinBox_33.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_33.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_33, 4, 1, 1, 1)

        self.doubleSpinBox_29 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_29.setObjectName(u"doubleSpinBox_29")
        self.doubleSpinBox_29.setDecimals(1)
        self.doubleSpinBox_29.setMinimum(0.100000000000000)
        self.doubleSpinBox_29.setMaximum(1.000000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_29, 1, 1, 1, 1)

        self.label_43 = QLabel(self.nc_area_top_page)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_6.addWidget(self.label_43, 5, 0, 1, 1)

        self.doubleSpinBox_35 = QDoubleSpinBox(self.nc_area_top_page)
        self.doubleSpinBox_35.setObjectName(u"doubleSpinBox_35")
        self.doubleSpinBox_35.setDecimals(2)
        self.doubleSpinBox_35.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_35.setMaximum(9999.000000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_35, 6, 1, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_6, 7, 0, 1, 2)

        self.pushButton_5 = QPushButton(self.nc_area_top_page)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_6.addWidget(self.pushButton_5, 8, 0, 1, 2)

        self.jobs_sw.addWidget(self.nc_area_top_page)
        self.nc_area_bottom_page = QWidget()
        self.nc_area_bottom_page.setObjectName(u"nc_area_bottom_page")
        self.gridLayout_7 = QGridLayout(self.nc_area_bottom_page)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_49 = QLabel(self.nc_area_bottom_page)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_7.addWidget(self.label_49, 3, 0, 1, 1)

        self.pushButton_6 = QPushButton(self.nc_area_bottom_page)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout_7.addWidget(self.pushButton_6, 9, 0, 1, 2)

        self.label_46 = QLabel(self.nc_area_bottom_page)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_7.addWidget(self.label_46, 4, 0, 1, 1)

        self.doubleSpinBox_39 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_39.setObjectName(u"doubleSpinBox_39")
        self.doubleSpinBox_39.setMinimum(0.010000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_39, 0, 1, 1, 1)

        self.doubleSpinBox_37 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_37.setObjectName(u"doubleSpinBox_37")
        self.doubleSpinBox_37.setDecimals(1)
        self.doubleSpinBox_37.setMinimum(0.100000000000000)
        self.doubleSpinBox_37.setMaximum(1.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_37, 1, 1, 1, 1)

        self.doubleSpinBox_40 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_40.setObjectName(u"doubleSpinBox_40")
        self.doubleSpinBox_40.setDecimals(2)
        self.doubleSpinBox_40.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_40.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_40, 2, 1, 1, 1)

        self.label_45 = QLabel(self.nc_area_bottom_page)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_7.addWidget(self.label_45, 2, 0, 1, 1)

        self.doubleSpinBox_41 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_41.setObjectName(u"doubleSpinBox_41")
        self.doubleSpinBox_41.setDecimals(2)
        self.doubleSpinBox_41.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_41.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_41, 7, 1, 1, 1)

        self.label_48 = QLabel(self.nc_area_bottom_page)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_7.addWidget(self.label_48, 1, 0, 1, 1)

        self.label_47 = QLabel(self.nc_area_bottom_page)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_7.addWidget(self.label_47, 0, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_7, 8, 0, 1, 2)

        self.doubleSpinBox_36 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_36.setObjectName(u"doubleSpinBox_36")
        self.doubleSpinBox_36.setDecimals(2)
        self.doubleSpinBox_36.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_36.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_36, 4, 1, 1, 1)

        self.doubleSpinBox_38 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_38.setObjectName(u"doubleSpinBox_38")
        self.doubleSpinBox_38.setDecimals(2)
        self.doubleSpinBox_38.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_38.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_38, 3, 1, 1, 1)

        self.doubleSpinBox_42 = QDoubleSpinBox(self.nc_area_bottom_page)
        self.doubleSpinBox_42.setObjectName(u"doubleSpinBox_42")
        self.doubleSpinBox_42.setDecimals(2)
        self.doubleSpinBox_42.setMinimum(-9999.000000000000000)
        self.doubleSpinBox_42.setMaximum(9999.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_42, 6, 1, 1, 1)

        self.label_51 = QLabel(self.nc_area_bottom_page)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_7.addWidget(self.label_51, 7, 0, 1, 1)

        self.label_50 = QLabel(self.nc_area_bottom_page)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_7.addWidget(self.label_50, 6, 0, 1, 1)

        self.jobs_sw.addWidget(self.nc_area_bottom_page)

        self.verticalLayout_8.addWidget(self.jobs_sw)

        self.tabWidget_2.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.tabWidget_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.viewCanvasWidget = VispyCanvas(self.viewTab)
        self.viewCanvasWidget.setObjectName(u"viewCanvasWidget")
        sizePolicy.setHeightForWidth(self.viewCanvasWidget.sizePolicy().hasHeightForWidth())
        self.viewCanvasWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.viewCanvasWidget)


        self.horizontalLayout_8.addLayout(self.horizontalLayout_6)

        self.tabWidget.addTab(self.viewTab, "")
        self.controlTab = QWidget()
        self.controlTab.setObjectName(u"controlTab")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.controlTab.sizePolicy().hasHeightForWidth())
        self.controlTab.setSizePolicy(sizePolicy4)
        self.controlTab.setFont(font)
        self.horizontalLayout_5 = QHBoxLayout(self.controlTab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.controlsVerticalLayout = QVBoxLayout()
        self.controlsVerticalLayout.setObjectName(u"controlsVerticalLayout")
        self.controlsVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.statusLabel = QLabel(self.controlTab)
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
        self.zAxisLabel = QLabel(self.controlTab)
        self.zAxisLabel.setObjectName(u"zAxisLabel")
        sizePolicy5.setHeightForWidth(self.zAxisLabel.sizePolicy().hasHeightForWidth())
        self.zAxisLabel.setSizePolicy(sizePolicy5)
        self.zAxisLabel.setFont(font)
        self.zAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.zAxisLabel.setFrameShape(QFrame.NoFrame)
        self.zAxisLabel.setFrameShadow(QFrame.Plain)
        self.zAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.zAxisLabel, 0, 3, 1, 1)

        self.label_10 = QLabel(self.controlTab)
        self.label_10.setObjectName(u"label_10")
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setFrameShape(QFrame.NoFrame)
        self.label_10.setFrameShadow(QFrame.Plain)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_10, 2, 1, 1, 1)

        self.zero_z_pushButton = QPushButton(self.controlTab)
        self.zero_z_pushButton.setObjectName(u"zero_z_pushButton")
        self.zero_z_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_z_pushButton, 3, 3, 1, 1)

        self.zero_xyz_pushButton = QPushButton(self.controlTab)
        self.zero_xyz_pushButton.setObjectName(u"zero_xyz_pushButton")
        self.zero_xyz_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_xyz_pushButton, 3, 0, 1, 1)

        self.label_9 = QLabel(self.controlTab)
        self.label_9.setObjectName(u"label_9")
        sizePolicy5.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy5)
        self.label_9.setLayoutDirection(Qt.LeftToRight)
        self.label_9.setFrameShape(QFrame.NoFrame)
        self.label_9.setFrameShadow(QFrame.Plain)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.label_11 = QLabel(self.controlTab)
        self.label_11.setObjectName(u"label_11")
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setLayoutDirection(Qt.LeftToRight)
        self.label_11.setFrameShape(QFrame.NoFrame)
        self.label_11.setFrameShadow(QFrame.Plain)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_11, 2, 3, 1, 1)

        self.zero_y_pushButton = QPushButton(self.controlTab)
        self.zero_y_pushButton.setObjectName(u"zero_y_pushButton")
        self.zero_y_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_y_pushButton, 3, 2, 1, 1)

        self.xAxisLabel = QLabel(self.controlTab)
        self.xAxisLabel.setObjectName(u"xAxisLabel")
        sizePolicy5.setHeightForWidth(self.xAxisLabel.sizePolicy().hasHeightForWidth())
        self.xAxisLabel.setSizePolicy(sizePolicy5)
        self.xAxisLabel.setFont(font)
        self.xAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.xAxisLabel.setFrameShape(QFrame.NoFrame)
        self.xAxisLabel.setFrameShadow(QFrame.Plain)
        self.xAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.xAxisLabel, 0, 1, 1, 1)

        self.zero_x_pushButton = QPushButton(self.controlTab)
        self.zero_x_pushButton.setObjectName(u"zero_x_pushButton")
        self.zero_x_pushButton.setFont(font)

        self.droGridLayout.addWidget(self.zero_x_pushButton, 3, 1, 1, 1)

        self.xAxisLabel_2 = QLabel(self.controlTab)
        self.xAxisLabel_2.setObjectName(u"xAxisLabel_2")
        sizePolicy5.setHeightForWidth(self.xAxisLabel_2.sizePolicy().hasHeightForWidth())
        self.xAxisLabel_2.setSizePolicy(sizePolicy5)
        self.xAxisLabel_2.setFont(font)
        self.xAxisLabel_2.setLayoutDirection(Qt.LeftToRight)
        self.xAxisLabel_2.setFrameShape(QFrame.NoFrame)
        self.xAxisLabel_2.setFrameShadow(QFrame.Plain)
        self.xAxisLabel_2.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.xAxisLabel_2, 0, 0, 1, 1)

        self.yAxisLabel = QLabel(self.controlTab)
        self.yAxisLabel.setObjectName(u"yAxisLabel")
        sizePolicy5.setHeightForWidth(self.yAxisLabel.sizePolicy().hasHeightForWidth())
        self.yAxisLabel.setSizePolicy(sizePolicy5)
        self.yAxisLabel.setFont(font)
        self.yAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.yAxisLabel.setFrameShape(QFrame.NoFrame)
        self.yAxisLabel.setFrameShadow(QFrame.Plain)
        self.yAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.yAxisLabel, 0, 2, 1, 1)

        self.label_12 = QLabel(self.controlTab)
        self.label_12.setObjectName(u"label_12")
        sizePolicy5.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy5)
        self.label_12.setFont(font)
        self.label_12.setLayoutDirection(Qt.LeftToRight)
        self.label_12.setFrameShape(QFrame.NoFrame)
        self.label_12.setFrameShadow(QFrame.Plain)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_12, 2, 0, 1, 1)

        self.mpos_y_label = QLabel(self.controlTab)
        self.mpos_y_label.setObjectName(u"mpos_y_label")
        sizePolicy5.setHeightForWidth(self.mpos_y_label.sizePolicy().hasHeightForWidth())
        self.mpos_y_label.setSizePolicy(sizePolicy5)
        self.mpos_y_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_y_label.setFrameShape(QFrame.NoFrame)
        self.mpos_y_label.setFrameShadow(QFrame.Plain)
        self.mpos_y_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_y_label, 1, 2, 1, 1)

        self.mpos_x_label = QLabel(self.controlTab)
        self.mpos_x_label.setObjectName(u"mpos_x_label")
        sizePolicy5.setHeightForWidth(self.mpos_x_label.sizePolicy().hasHeightForWidth())
        self.mpos_x_label.setSizePolicy(sizePolicy5)
        self.mpos_x_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_x_label.setFrameShape(QFrame.NoFrame)
        self.mpos_x_label.setFrameShadow(QFrame.Plain)
        self.mpos_x_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_x_label, 1, 1, 1, 1)

        self.mpos_z_label = QLabel(self.controlTab)
        self.mpos_z_label.setObjectName(u"mpos_z_label")
        sizePolicy5.setHeightForWidth(self.mpos_z_label.sizePolicy().hasHeightForWidth())
        self.mpos_z_label.setSizePolicy(sizePolicy5)
        self.mpos_z_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_z_label.setFrameShape(QFrame.NoFrame)
        self.mpos_z_label.setFrameShadow(QFrame.Plain)
        self.mpos_z_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_z_label, 1, 3, 1, 1)

        self.label_5 = QLabel(self.controlTab)
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
        self.unlockButton = QPushButton(self.controlTab)
        self.unlockButton.setObjectName(u"unlockButton")
        sizePolicy2.setHeightForWidth(self.unlockButton.sizePolicy().hasHeightForWidth())
        self.unlockButton.setSizePolicy(sizePolicy2)
        self.unlockButton.setFont(font)

        self.unlockHomingHorizontalLayout.addWidget(self.unlockButton)

        self.homingButton = QPushButton(self.controlTab)
        self.homingButton.setObjectName(u"homingButton")
        sizePolicy2.setHeightForWidth(self.homingButton.sizePolicy().hasHeightForWidth())
        self.homingButton.setSizePolicy(sizePolicy2)
        self.homingButton.setFont(font)

        self.unlockHomingHorizontalLayout.addWidget(self.homingButton)


        self.controlsVerticalLayout.addLayout(self.unlockHomingHorizontalLayout)

        self.gridLayoutDirections = QGridLayout()
        self.gridLayoutDirections.setObjectName(u"gridLayoutDirections")
        self.gridLayoutDirections.setContentsMargins(5, 5, 5, 5)
        self.xYMinusPlusButton = QPushButton(self.controlTab)
        self.xYMinusPlusButton.setObjectName(u"xYMinusPlusButton")
        sizePolicy2.setHeightForWidth(self.xYMinusPlusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusPlusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.xYMinusPlusButton, 0, 0, 1, 1)

        self.yPlusButton = QPushButton(self.controlTab)
        self.yPlusButton.setObjectName(u"yPlusButton")
        sizePolicy2.setHeightForWidth(self.yPlusButton.sizePolicy().hasHeightForWidth())
        self.yPlusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.yPlusButton, 0, 1, 1, 1)

        self.xYPlusButton = QPushButton(self.controlTab)
        self.xYPlusButton.setObjectName(u"xYPlusButton")
        sizePolicy2.setHeightForWidth(self.xYPlusButton.sizePolicy().hasHeightForWidth())
        self.xYPlusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.xYPlusButton, 0, 2, 1, 1)

        self.xMinusButton = QPushButton(self.controlTab)
        self.xMinusButton.setObjectName(u"xMinusButton")
        sizePolicy2.setHeightForWidth(self.xMinusButton.sizePolicy().hasHeightForWidth())
        self.xMinusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.xMinusButton, 1, 0, 1, 1)

        self.centerButton = QPushButton(self.controlTab)
        self.centerButton.setObjectName(u"centerButton")
        sizePolicy2.setHeightForWidth(self.centerButton.sizePolicy().hasHeightForWidth())
        self.centerButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.centerButton, 1, 1, 1, 1)

        self.xPlusButton = QPushButton(self.controlTab)
        self.xPlusButton.setObjectName(u"xPlusButton")
        sizePolicy2.setHeightForWidth(self.xPlusButton.sizePolicy().hasHeightForWidth())
        self.xPlusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.xPlusButton, 1, 2, 1, 1)

        self.xYMinusButton = QPushButton(self.controlTab)
        self.xYMinusButton.setObjectName(u"xYMinusButton")
        sizePolicy2.setHeightForWidth(self.xYMinusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.xYMinusButton, 2, 0, 1, 1)

        self.yMinusButton = QPushButton(self.controlTab)
        self.yMinusButton.setObjectName(u"yMinusButton")
        sizePolicy2.setHeightForWidth(self.yMinusButton.sizePolicy().hasHeightForWidth())
        self.yMinusButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.yMinusButton, 2, 1, 1, 1)

        self.xYPlusMinuButton = QPushButton(self.controlTab)
        self.xYPlusMinuButton.setObjectName(u"xYPlusMinuButton")
        sizePolicy2.setHeightForWidth(self.xYPlusMinuButton.sizePolicy().hasHeightForWidth())
        self.xYPlusMinuButton.setSizePolicy(sizePolicy2)

        self.gridLayoutDirections.addWidget(self.xYPlusMinuButton, 2, 2, 1, 1)


        self.controlsVerticalLayout.addLayout(self.gridLayoutDirections)

        self.xyzIncrementsHorizontalLayout = QHBoxLayout()
        self.xyzIncrementsHorizontalLayout.setObjectName(u"xyzIncrementsHorizontalLayout")
        self.xyzIncrementsHorizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_3 = QLabel(self.controlTab)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_3, 0, Qt.AlignHCenter)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.controlTab)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy2)

        self.verticalLayout_5.addWidget(self.doubleSpinBox_2, 0, Qt.AlignHCenter)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.controlTab)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_4, 0, Qt.AlignHCenter)

        self.doubleSpinBox = QDoubleSpinBox(self.controlTab)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy2)

        self.verticalLayout_4.addWidget(self.doubleSpinBox, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.zPlusButton = QPushButton(self.controlTab)
        self.zPlusButton.setObjectName(u"zPlusButton")
        sizePolicy2.setHeightForWidth(self.zPlusButton.sizePolicy().hasHeightForWidth())
        self.zPlusButton.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.zPlusButton)

        self.zMinusButton = QPushButton(self.controlTab)
        self.zMinusButton.setObjectName(u"zMinusButton")
        sizePolicy2.setHeightForWidth(self.zMinusButton.sizePolicy().hasHeightForWidth())
        self.zMinusButton.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.zMinusButton)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_3)

        self.xyzIncrementsHorizontalLayout.setStretch(0, 3)
        self.xyzIncrementsHorizontalLayout.setStretch(1, 3)
        self.xyzIncrementsHorizontalLayout.setStretch(2, 1)

        self.controlsVerticalLayout.addLayout(self.xyzIncrementsHorizontalLayout)

        self.terminalVerticalLayout = QVBoxLayout()
        self.terminalVerticalLayout.setObjectName(u"terminalVerticalLayout")
        self.serial_te = QTextEdit(self.controlTab)
        self.serial_te.setObjectName(u"serial_te")
        self.serial_te.setEnabled(True)
        self.serial_te.setFrameShadow(QFrame.Sunken)
        self.serial_te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.terminalVerticalLayout.addWidget(self.serial_te)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.send_text_edit = QLineEdit(self.controlTab)
        self.send_text_edit.setObjectName(u"send_text_edit")

        self.horizontalLayout_2.addWidget(self.send_text_edit)

        self.send_push_button = QPushButton(self.controlTab)
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
        self.serial_ports_cb = QComboBox(self.controlTab)
        self.serial_ports_cb.setObjectName(u"serial_ports_cb")
        sizePolicy3.setHeightForWidth(self.serial_ports_cb.sizePolicy().hasHeightForWidth())
        self.serial_ports_cb.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.serial_ports_cb)

        self.serial_baud_cb = QComboBox(self.controlTab)
        self.serial_baud_cb.setObjectName(u"serial_baud_cb")
        sizePolicy3.setHeightForWidth(self.serial_baud_cb.sizePolicy().hasHeightForWidth())
        self.serial_baud_cb.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.serial_baud_cb)

        self.refresh_button = QPushButton(self.controlTab)
        self.refresh_button.setObjectName(u"refresh_button")
        sizePolicy6.setHeightForWidth(self.refresh_button.sizePolicy().hasHeightForWidth())
        self.refresh_button.setSizePolicy(sizePolicy6)
        self.refresh_button.setFont(font)
        self.refresh_button.setCheckable(False)

        self.horizontalLayout.addWidget(self.refresh_button)


        self.connectVerticalLayout.addLayout(self.horizontalLayout)


        self.terminalVerticalLayout.addLayout(self.connectVerticalLayout)

        self.splitter_2 = QSplitter(self.controlTab)
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
        sizePolicy2.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy2)
        self.connect_button.setFont(font)
        self.splitter_2.addWidget(self.connect_button)

        self.terminalVerticalLayout.addWidget(self.splitter_2)


        self.controlsVerticalLayout.addLayout(self.terminalVerticalLayout)


        self.horizontalLayout_4.addLayout(self.controlsVerticalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.openGLWidget = QOpenGLWidget(self.controlTab)
        self.openGLWidget.setObjectName(u"openGLWidget")
        sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.openGLWidget)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 10)

        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.controlTab, "")
        self.alignTab = QWidget()
        self.alignTab.setObjectName(u"alignTab")
        self.alignTab.setFont(font)
        self.horizontalLayout_7 = QHBoxLayout(self.alignTab)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.openGLWidget_2 = QOpenGLWidget(self.alignTab)
        self.openGLWidget_2.setObjectName(u"openGLWidget_2")

        self.horizontalLayout_7.addWidget(self.openGLWidget_2)

        self.label_2 = QLabel(self.alignTab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.verticalSlider = QSlider(self.alignTab)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMaximum(255)
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.horizontalLayout_7.addWidget(self.verticalSlider)

        self.tabWidget.addTab(self.alignTab, "")

        self.verticalLayout_6.addWidget(self.tabWidget)

        self.logging_plain_text_edit = QPlainTextEdit(self.centralwidget)
        self.logging_plain_text_edit.setObjectName(u"logging_plain_text_edit")
        sizePolicy5.setHeightForWidth(self.logging_plain_text_edit.sizePolicy().hasHeightForWidth())
        self.logging_plain_text_edit.setSizePolicy(sizePolicy5)
        self.logging_plain_text_edit.setMaximumSize(QSize(16777215, 100))
        self.logging_plain_text_edit.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.logging_plain_text_edit)

        MainWindow.setCentralWidget(self.centralwidget)
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

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.jobs_sw.setCurrentIndex(5)


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
        self.no_copper_2_pb.setText(QCoreApplication.translate("MainWindow", u"NO COPPER 2", None))
        self.no_copper_2_chb.setText("")
        self.viewLabel.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.no_copper_1_pb.setText(QCoreApplication.translate("MainWindow", u"NO COPPER 1", None))
        self.bottomViewCheckBox.setText("")
        self.profileLoadButton.setText(QCoreApplication.translate("MainWindow", u"PROFILE", None))
        self.no_copper_1_chb.setText("")
        self.clear_views_push_button.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.drillLoadButton.setText(QCoreApplication.translate("MainWindow", u"DRILL", None))
        self.topLoadButton.setText(QCoreApplication.translate("MainWindow", u"TOP", None))
        self.bottomLoadButton.setText(QCoreApplication.translate("MainWindow", u"BOTTOM", None))
        self.drillViewCheckBox.setText("")
        self.filePathLabel.setText(QCoreApplication.translate("MainWindow", u"File Path", None))
        self.all_view_checkbox.setText("")
        self.profileViewCheckBox.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"LOAD LAYERS", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Number of Passes", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Number of Passes", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Depth per Pass [mm]", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Taps layout", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Margin [mm]", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.checkBox.setText("")
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Multi-depth", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Tap size [mm]", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Bit", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Diameter [mm]", None));
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Milling Tool", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.checkBox_2.setText("")
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Travel Z [mm]", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Generate Job", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Spindle Speed", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Cut Z [mm]", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Tool Diameter [mm]", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Z Feed Rate [mm/min]", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"XY Feed Rate [mm/min]", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"CREATE JOB", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.viewTab), QCoreApplication.translate("MainWindow", u"VIEW", None))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlTab), QCoreApplication.translate("MainWindow", u"CONTROL", None))
        self.label_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.alignTab), QCoreApplication.translate("MainWindow", u"ALIGN", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuConsole.setTitle(QCoreApplication.translate("MainWindow", u"Console", None))
    # retranslateUi

