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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.controlTab = QWidget()
        self.controlTab.setObjectName(u"controlTab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.controlTab.sizePolicy().hasHeightForWidth())
        self.controlTab.setSizePolicy(sizePolicy1)
        self.horizontalLayout_5 = QHBoxLayout(self.controlTab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.controlsVerticalLayout = QVBoxLayout()
        self.controlsVerticalLayout.setObjectName(u"controlsVerticalLayout")
        self.controlsVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.statusLabel = QLabel(self.controlTab)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.statusLabel.setFont(font)
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.controlsVerticalLayout.addWidget(self.statusLabel)

        self.droGridLayout = QGridLayout()
        self.droGridLayout.setObjectName(u"droGridLayout")
        self.droGridLayout.setHorizontalSpacing(0)
        self.droGridLayout.setVerticalSpacing(6)
        self.zAxisLabel = QLabel(self.controlTab)
        self.zAxisLabel.setObjectName(u"zAxisLabel")
        sizePolicy2.setHeightForWidth(self.zAxisLabel.sizePolicy().hasHeightForWidth())
        self.zAxisLabel.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setBold(True)
        font1.setWeight(75)
        self.zAxisLabel.setFont(font1)
        self.zAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.zAxisLabel.setFrameShape(QFrame.NoFrame)
        self.zAxisLabel.setFrameShadow(QFrame.Plain)
        self.zAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.zAxisLabel, 0, 3, 1, 1)

        self.label_10 = QLabel(self.controlTab)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setFrameShape(QFrame.NoFrame)
        self.label_10.setFrameShadow(QFrame.Plain)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_10, 2, 1, 1, 1)

        self.zero_z_pushButton = QPushButton(self.controlTab)
        self.zero_z_pushButton.setObjectName(u"zero_z_pushButton")
        self.zero_z_pushButton.setFont(font1)

        self.droGridLayout.addWidget(self.zero_z_pushButton, 3, 3, 1, 1)

        self.zero_xyz_pushButton = QPushButton(self.controlTab)
        self.zero_xyz_pushButton.setObjectName(u"zero_xyz_pushButton")
        self.zero_xyz_pushButton.setFont(font1)

        self.droGridLayout.addWidget(self.zero_xyz_pushButton, 3, 0, 1, 1)

        self.label_9 = QLabel(self.controlTab)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setLayoutDirection(Qt.LeftToRight)
        self.label_9.setFrameShape(QFrame.NoFrame)
        self.label_9.setFrameShadow(QFrame.Plain)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.label_11 = QLabel(self.controlTab)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        self.label_11.setLayoutDirection(Qt.LeftToRight)
        self.label_11.setFrameShape(QFrame.NoFrame)
        self.label_11.setFrameShadow(QFrame.Plain)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_11, 2, 3, 1, 1)

        self.zero_y_pushButton = QPushButton(self.controlTab)
        self.zero_y_pushButton.setObjectName(u"zero_y_pushButton")
        self.zero_y_pushButton.setFont(font1)

        self.droGridLayout.addWidget(self.zero_y_pushButton, 3, 2, 1, 1)

        self.xAxisLabel = QLabel(self.controlTab)
        self.xAxisLabel.setObjectName(u"xAxisLabel")
        sizePolicy2.setHeightForWidth(self.xAxisLabel.sizePolicy().hasHeightForWidth())
        self.xAxisLabel.setSizePolicy(sizePolicy2)
        self.xAxisLabel.setFont(font1)
        self.xAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.xAxisLabel.setFrameShape(QFrame.NoFrame)
        self.xAxisLabel.setFrameShadow(QFrame.Plain)
        self.xAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.xAxisLabel, 0, 1, 1, 1)

        self.zero_x_pushButton = QPushButton(self.controlTab)
        self.zero_x_pushButton.setObjectName(u"zero_x_pushButton")
        self.zero_x_pushButton.setFont(font1)

        self.droGridLayout.addWidget(self.zero_x_pushButton, 3, 1, 1, 1)

        self.xAxisLabel_2 = QLabel(self.controlTab)
        self.xAxisLabel_2.setObjectName(u"xAxisLabel_2")
        sizePolicy2.setHeightForWidth(self.xAxisLabel_2.sizePolicy().hasHeightForWidth())
        self.xAxisLabel_2.setSizePolicy(sizePolicy2)
        self.xAxisLabel_2.setFont(font1)
        self.xAxisLabel_2.setLayoutDirection(Qt.LeftToRight)
        self.xAxisLabel_2.setFrameShape(QFrame.NoFrame)
        self.xAxisLabel_2.setFrameShadow(QFrame.Plain)
        self.xAxisLabel_2.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.xAxisLabel_2, 0, 0, 1, 1)

        self.yAxisLabel = QLabel(self.controlTab)
        self.yAxisLabel.setObjectName(u"yAxisLabel")
        sizePolicy2.setHeightForWidth(self.yAxisLabel.sizePolicy().hasHeightForWidth())
        self.yAxisLabel.setSizePolicy(sizePolicy2)
        self.yAxisLabel.setFont(font1)
        self.yAxisLabel.setLayoutDirection(Qt.LeftToRight)
        self.yAxisLabel.setFrameShape(QFrame.NoFrame)
        self.yAxisLabel.setFrameShadow(QFrame.Plain)
        self.yAxisLabel.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.yAxisLabel, 0, 2, 1, 1)

        self.label_12 = QLabel(self.controlTab)
        self.label_12.setObjectName(u"label_12")
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)
        self.label_12.setFont(font1)
        self.label_12.setLayoutDirection(Qt.LeftToRight)
        self.label_12.setFrameShape(QFrame.NoFrame)
        self.label_12.setFrameShadow(QFrame.Plain)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.label_12, 2, 0, 1, 1)

        self.mpos_y_label = QLabel(self.controlTab)
        self.mpos_y_label.setObjectName(u"mpos_y_label")
        sizePolicy2.setHeightForWidth(self.mpos_y_label.sizePolicy().hasHeightForWidth())
        self.mpos_y_label.setSizePolicy(sizePolicy2)
        self.mpos_y_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_y_label.setFrameShape(QFrame.NoFrame)
        self.mpos_y_label.setFrameShadow(QFrame.Plain)
        self.mpos_y_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_y_label, 1, 2, 1, 1)

        self.mpos_x_label = QLabel(self.controlTab)
        self.mpos_x_label.setObjectName(u"mpos_x_label")
        sizePolicy2.setHeightForWidth(self.mpos_x_label.sizePolicy().hasHeightForWidth())
        self.mpos_x_label.setSizePolicy(sizePolicy2)
        self.mpos_x_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_x_label.setFrameShape(QFrame.NoFrame)
        self.mpos_x_label.setFrameShadow(QFrame.Plain)
        self.mpos_x_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_x_label, 1, 1, 1, 1)

        self.mpos_z_label = QLabel(self.controlTab)
        self.mpos_z_label.setObjectName(u"mpos_z_label")
        sizePolicy2.setHeightForWidth(self.mpos_z_label.sizePolicy().hasHeightForWidth())
        self.mpos_z_label.setSizePolicy(sizePolicy2)
        self.mpos_z_label.setLayoutDirection(Qt.LeftToRight)
        self.mpos_z_label.setFrameShape(QFrame.NoFrame)
        self.mpos_z_label.setFrameShadow(QFrame.Plain)
        self.mpos_z_label.setAlignment(Qt.AlignCenter)

        self.droGridLayout.addWidget(self.mpos_z_label, 1, 3, 1, 1)

        self.label_5 = QLabel(self.controlTab)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)
        self.label_5.setFont(font1)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.unlockButton.sizePolicy().hasHeightForWidth())
        self.unlockButton.setSizePolicy(sizePolicy3)
        self.unlockButton.setFont(font1)

        self.unlockHomingHorizontalLayout.addWidget(self.unlockButton)

        self.homingButton = QPushButton(self.controlTab)
        self.homingButton.setObjectName(u"homingButton")
        sizePolicy3.setHeightForWidth(self.homingButton.sizePolicy().hasHeightForWidth())
        self.homingButton.setSizePolicy(sizePolicy3)
        self.homingButton.setFont(font1)

        self.unlockHomingHorizontalLayout.addWidget(self.homingButton)


        self.controlsVerticalLayout.addLayout(self.unlockHomingHorizontalLayout)

        self.gridLayoutDirections = QGridLayout()
        self.gridLayoutDirections.setObjectName(u"gridLayoutDirections")
        self.gridLayoutDirections.setContentsMargins(5, 5, 5, 5)
        self.xYMinusPlusButton = QPushButton(self.controlTab)
        self.xYMinusPlusButton.setObjectName(u"xYMinusPlusButton")
        sizePolicy3.setHeightForWidth(self.xYMinusPlusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYMinusPlusButton, 0, 0, 1, 1)

        self.yPlusButton = QPushButton(self.controlTab)
        self.yPlusButton.setObjectName(u"yPlusButton")
        sizePolicy3.setHeightForWidth(self.yPlusButton.sizePolicy().hasHeightForWidth())
        self.yPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.yPlusButton, 0, 1, 1, 1)

        self.xYPlusButton = QPushButton(self.controlTab)
        self.xYPlusButton.setObjectName(u"xYPlusButton")
        sizePolicy3.setHeightForWidth(self.xYPlusButton.sizePolicy().hasHeightForWidth())
        self.xYPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYPlusButton, 0, 2, 1, 1)

        self.xMinusButton = QPushButton(self.controlTab)
        self.xMinusButton.setObjectName(u"xMinusButton")
        sizePolicy3.setHeightForWidth(self.xMinusButton.sizePolicy().hasHeightForWidth())
        self.xMinusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xMinusButton, 1, 0, 1, 1)

        self.centerButton = QPushButton(self.controlTab)
        self.centerButton.setObjectName(u"centerButton")
        sizePolicy3.setHeightForWidth(self.centerButton.sizePolicy().hasHeightForWidth())
        self.centerButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.centerButton, 1, 1, 1, 1)

        self.xPlusButton = QPushButton(self.controlTab)
        self.xPlusButton.setObjectName(u"xPlusButton")
        sizePolicy3.setHeightForWidth(self.xPlusButton.sizePolicy().hasHeightForWidth())
        self.xPlusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xPlusButton, 1, 2, 1, 1)

        self.xYMinusButton = QPushButton(self.controlTab)
        self.xYMinusButton.setObjectName(u"xYMinusButton")
        sizePolicy3.setHeightForWidth(self.xYMinusButton.sizePolicy().hasHeightForWidth())
        self.xYMinusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.xYMinusButton, 2, 0, 1, 1)

        self.yMinusButton = QPushButton(self.controlTab)
        self.yMinusButton.setObjectName(u"yMinusButton")
        sizePolicy3.setHeightForWidth(self.yMinusButton.sizePolicy().hasHeightForWidth())
        self.yMinusButton.setSizePolicy(sizePolicy3)

        self.gridLayoutDirections.addWidget(self.yMinusButton, 2, 1, 1, 1)

        self.xYPlusMinuButton = QPushButton(self.controlTab)
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
        self.label_3 = QLabel(self.controlTab)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_3)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.controlTab)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy3.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy3)

        self.verticalLayout_5.addWidget(self.doubleSpinBox_2)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.controlTab)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_4)

        self.doubleSpinBox = QDoubleSpinBox(self.controlTab)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        sizePolicy3.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.doubleSpinBox)


        self.xyzIncrementsHorizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.zPlusButton = QPushButton(self.controlTab)
        self.zPlusButton.setObjectName(u"zPlusButton")
        sizePolicy3.setHeightForWidth(self.zPlusButton.sizePolicy().hasHeightForWidth())
        self.zPlusButton.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.zPlusButton)

        self.zMinusButton = QPushButton(self.controlTab)
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
        self.textEdit = QTextEdit(self.controlTab)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.terminalVerticalLayout.addWidget(self.textEdit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.send_text_edit = QLineEdit(self.controlTab)
        self.send_text_edit.setObjectName(u"send_text_edit")

        self.horizontalLayout_2.addWidget(self.send_text_edit)

        self.send_push_button = QPushButton(self.controlTab)
        self.send_push_button.setObjectName(u"send_push_button")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.send_push_button.sizePolicy().hasHeightForWidth())
        self.send_push_button.setSizePolicy(sizePolicy4)
        self.send_push_button.setFont(font1)

        self.horizontalLayout_2.addWidget(self.send_push_button)


        self.terminalVerticalLayout.addLayout(self.horizontalLayout_2)

        self.connectVerticalLayout = QVBoxLayout()
        self.connectVerticalLayout.setSpacing(6)
        self.connectVerticalLayout.setObjectName(u"connectVerticalLayout")
        self.connectVerticalLayout.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serialPortsComboBox = QComboBox(self.controlTab)
        self.serialPortsComboBox.setObjectName(u"serialPortsComboBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.serialPortsComboBox.sizePolicy().hasHeightForWidth())
        self.serialPortsComboBox.setSizePolicy(sizePolicy5)

        self.horizontalLayout.addWidget(self.serialPortsComboBox)

        self.refreshButton = QPushButton(self.controlTab)
        self.refreshButton.setObjectName(u"refreshButton")
        sizePolicy4.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy4)
        self.refreshButton.setFont(font1)
        self.refreshButton.setCheckable(False)

        self.horizontalLayout.addWidget(self.refreshButton)


        self.connectVerticalLayout.addLayout(self.horizontalLayout)


        self.terminalVerticalLayout.addLayout(self.connectVerticalLayout)

        self.splitter_2 = QSplitter(self.controlTab)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.checkBox = QCheckBox(self.splitter_2)
        self.checkBox.setObjectName(u"checkBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy6)
        self.checkBox.setFont(font1)
        self.checkBox.setChecked(True)
        self.splitter_2.addWidget(self.checkBox)
        self.clearTerminalButton = QPushButton(self.splitter_2)
        self.clearTerminalButton.setObjectName(u"clearTerminalButton")
        self.clearTerminalButton.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.clearTerminalButton.sizePolicy().hasHeightForWidth())
        self.clearTerminalButton.setSizePolicy(sizePolicy6)
        self.clearTerminalButton.setFont(font1)
        self.splitter_2.addWidget(self.clearTerminalButton)
        self.connectButton = QPushButton(self.splitter_2)
        self.connectButton.setObjectName(u"connectButton")
        sizePolicy3.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy3)
        self.connectButton.setFont(font1)
        self.splitter_2.addWidget(self.connectButton)

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
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.openGLWidget_2 = QOpenGLWidget(self.tab_2)
        self.openGLWidget_2.setObjectName(u"openGLWidget_2")

        self.horizontalLayout_7.addWidget(self.openGLWidget_2)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.verticalSlider = QSlider(self.tab_2)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMaximum(255)
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.horizontalLayout_7.addWidget(self.verticalSlider)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1039, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"newCNC", None))
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
        self.refreshButton.setToolTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.refreshButton.setStatusTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(statustip)
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"Serial Port Refresh", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Autoscroll", None))
        self.clearTerminalButton.setText(QCoreApplication.translate("MainWindow", u"Clear Terminal", None))
#if QT_CONFIG(tooltip)
        self.connectButton.setToolTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.connectButton.setStatusTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(statustip)
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlTab), QCoreApplication.translate("MainWindow", u"CONTROL", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Tab 3", None))
    # retranslateUi

