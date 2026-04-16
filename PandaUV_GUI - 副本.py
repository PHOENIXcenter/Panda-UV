# PandaUV_GUI.py
# Copyright (C) 2026 PHOENIXcenter
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

#!/usr/bin/env python
# coding: utf-8


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PANDA-UV_param_writerMYcDrw.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
    QRect,
    Qt,
    QCoreApplication,
    QMetaObject,
    QSize,
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QSpinBox,
    QCheckBox,
    QTextBrowser,
    QMenuBar,
    QStatusBar,
    QFileDialog,
    QRadioButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QGroupBox,
)


import yaml
import sys
import os


from PandaUV_core import main, Param

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 950)
        MainWindow.setMinimumSize(QSize(1300, 950))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QGridLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        param_file_layout = QHBoxLayout()
        param_file_layout.setSpacing(5)
        self.pushButton_load_param = QPushButton()
        self.pushButton_load_param.setObjectName("pushButton_load_param")
        self.lineEdit_param_file_dir = QLineEdit()
        self.lineEdit_param_file_dir.setObjectName("lineEdit_param_file_dir")
        param_file_layout.addWidget(self.pushButton_load_param)
        param_file_layout.addWidget(self.lineEdit_param_file_dir)
        left_layout.addLayout(param_file_layout)

        scan_layout = QVBoxLayout()
        scan_layout.setSpacing(5)
        self.label = QLabel()
        self.label.setObjectName("label")
        self.label.setText("Scan-Sequence:")
        scan_table_layout = QHBoxLayout()
        scan_table_layout.setSpacing(5)
        self.tableWidget_sequence = QTableWidget()
        self.tableWidget_sequence.setObjectName("tableWidget_sequence")
        self.tableWidget_sequence.setColumnCount(2)
        self.tableWidget_sequence.setHorizontalHeaderLabels(["Scan", "Sequence"])
        self.tableWidget_sequence.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.tableWidget_sequence.setRowCount(0)
        self.tableWidget_sequence.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        scan_btn_layout = QVBoxLayout()
        scan_btn_layout.setSpacing(5)
        self.pushButton_add_scan = QPushButton()
        self.pushButton_add_scan.setObjectName("pushButton_add_scan")
        self.pushButton_add_scan.setText("+")
        self.pushButton_remove_scan = QPushButton()
        self.pushButton_remove_scan.setObjectName("pushButton_remove_scan")
        self.pushButton_remove_scan.setText("-")
        scan_btn_layout.addWidget(self.pushButton_add_scan)
        scan_btn_layout.addWidget(self.pushButton_remove_scan)
        scan_table_layout.addWidget(self.tableWidget_sequence)
        scan_table_layout.addLayout(scan_btn_layout)
        scan_layout.addWidget(self.label)
        scan_layout.addLayout(scan_table_layout)
        left_layout.addLayout(scan_layout)

        msalign_layout = QHBoxLayout()
        msalign_layout.setSpacing(5)
        self.label_4 = QLabel()
        self.label_4.setObjectName("label_4")
        self.label_4.setText("MSAlign file:")
        self.label_4.setFixedWidth(100)
        self.lineEdit_msalign_file_dir = QLineEdit()
        self.lineEdit_msalign_file_dir.setObjectName("lineEdit_msalign_file_dir")
        msalign_layout.addWidget(self.label_4)
        msalign_layout.addWidget(self.lineEdit_msalign_file_dir)
        left_layout.addLayout(msalign_layout)

        fixed_mod_layout = QVBoxLayout()
        fixed_mod_layout.setSpacing(5)
        self.label_3 = QLabel()
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Fixed mod:")
        fixed_mod_table_layout = QHBoxLayout()
        fixed_mod_table_layout.setSpacing(5)
        self.tableWidget_fixed_mod = QTableWidget()
        self.tableWidget_fixed_mod.setObjectName("tableWidget_fixed_mod")
        self.tableWidget_fixed_mod.setColumnCount(4)
        self.tableWidget_fixed_mod.setHorizontalHeaderLabels(
            ["Scan", "name", "formula", "loc"]
        )
        self.tableWidget_fixed_mod.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.tableWidget_fixed_mod.setRowCount(0)
        self.tableWidget_fixed_mod.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        fixed_mod_btn_layout = QVBoxLayout()
        fixed_mod_btn_layout.setSpacing(5)
        self.pushButton_add_fixed_mod = QPushButton()
        self.pushButton_add_fixed_mod.setObjectName("pushButton_add_fixed_mod")
        self.pushButton_add_fixed_mod.setText("+")
        self.pushButton_remove_fixed_mod = QPushButton()
        self.pushButton_remove_fixed_mod.setObjectName("pushButton_remove_fixed_mod")
        self.pushButton_remove_fixed_mod.setText("-")
        fixed_mod_btn_layout.addWidget(self.pushButton_add_fixed_mod)
        fixed_mod_btn_layout.addWidget(self.pushButton_remove_fixed_mod)
        fixed_mod_table_layout.addWidget(self.tableWidget_fixed_mod)
        fixed_mod_table_layout.addLayout(fixed_mod_btn_layout)
        fixed_mod_layout.addWidget(self.label_3)
        fixed_mod_layout.addLayout(fixed_mod_table_layout)
        left_layout.addLayout(fixed_mod_layout)

        unloc_mod_layout = QVBoxLayout()
        unloc_mod_layout.setSpacing(5)
        self.label_unloc = QLabel()
        self.label_unloc.setObjectName("label_unloc")
        self.label_unloc.setText("Unlocalized mod:")
        unloc_mod_table_layout = QHBoxLayout()
        unloc_mod_table_layout.setSpacing(5)
        self.tableWidget_unloc_mod = QTableWidget()
        self.tableWidget_unloc_mod.setObjectName("tableWidget_unloc_mod")
        self.tableWidget_unloc_mod.setColumnCount(6)
        self.tableWidget_unloc_mod.setHorizontalHeaderLabels(
            ["Scan", "name", "formula", "start_loc", "end_loc", "ion type"]
        )
        self.tableWidget_unloc_mod.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.tableWidget_unloc_mod.setRowCount(0)
        self.tableWidget_unloc_mod.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        unloc_mod_btn_layout = QVBoxLayout()
        unloc_mod_btn_layout.setSpacing(5)
        self.pushButton_add_unloc_mod = QPushButton()
        self.pushButton_add_unloc_mod.setObjectName("pushButton_add_unloc_mod")
        self.pushButton_add_unloc_mod.setText("+")
        self.pushButton_remove_unloc_mod = QPushButton()
        self.pushButton_remove_unloc_mod.setObjectName("pushButton_remove_unloc_mod")
        self.pushButton_remove_unloc_mod.setText("-")
        unloc_mod_btn_layout.addWidget(self.pushButton_add_unloc_mod)
        unloc_mod_btn_layout.addWidget(self.pushButton_remove_unloc_mod)
        unloc_mod_table_layout.addWidget(self.tableWidget_unloc_mod)
        unloc_mod_table_layout.addLayout(unloc_mod_btn_layout)
        unloc_mod_layout.addWidget(self.label_unloc)
        unloc_mod_layout.addLayout(unloc_mod_table_layout)
        left_layout.addLayout(unloc_mod_layout)

        prsm_id_layout = QVBoxLayout()
        prsm_id_layout.setSpacing(5)
        self.label_prsm_id = QLabel()
        self.label_prsm_id.setObjectName("label_prsm_id")
        self.label_prsm_id.setText("PRSM ID:")
        prsm_id_table_layout = QHBoxLayout()
        prsm_id_table_layout.setSpacing(5)
        self.tableWidget_prsm_id = QTableWidget()
        self.tableWidget_prsm_id.setObjectName("tableWidget_prsm_id")
        self.tableWidget_prsm_id.setColumnCount(2)
        self.tableWidget_prsm_id.setHorizontalHeaderLabels(["Scan", "prsm_id"])
        self.tableWidget_prsm_id.setRowCount(0)
        self.tableWidget_prsm_id.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        prsm_id_btn_layout = QVBoxLayout()
        prsm_id_btn_layout.setSpacing(5)
        self.pushButton_add_prsm_id = QPushButton()
        self.pushButton_add_prsm_id.setObjectName("pushButton_add_prsm_id")
        self.pushButton_add_prsm_id.setText("+")
        self.pushButton_remove_prsm_id = QPushButton()
        self.pushButton_remove_prsm_id.setObjectName("pushButton_remove_prsm_id")
        self.pushButton_remove_prsm_id.setText("-")
        prsm_id_btn_layout.addWidget(self.pushButton_add_prsm_id)
        prsm_id_btn_layout.addWidget(self.pushButton_remove_prsm_id)
        prsm_id_table_layout.addWidget(self.tableWidget_prsm_id)
        prsm_id_table_layout.addLayout(prsm_id_btn_layout)
        prsm_id_layout.addWidget(self.label_prsm_id)
        prsm_id_layout.addLayout(prsm_id_table_layout)
        left_layout.addLayout(prsm_id_layout)

        mzml_layout = QHBoxLayout()
        mzml_layout.setSpacing(5)
        self.label_15 = QLabel()
        self.label_15.setObjectName("label_15")
        self.label_15.setText("mzML dir:")
        self.label_15.setFixedWidth(100)
        self.lineEdit_mzml_file_dir = QLineEdit()
        self.lineEdit_mzml_file_dir.setObjectName("lineEdit_mzml_file_dir")
        mzml_layout.addWidget(self.label_15)
        mzml_layout.addWidget(self.lineEdit_mzml_file_dir)
        left_layout.addLayout(mzml_layout)

        r_env_layout = QHBoxLayout()
        r_env_layout.setSpacing(5)
        self.label_7 = QLabel()
        self.label_7.setObjectName("label_7")
        self.label_7.setText("R env dir:")
        self.label_7.setFixedWidth(100)
        self.lineEdit_r_env_dir = QLineEdit()
        self.lineEdit_r_env_dir.setObjectName("lineEdit_r_env_dir")
        r_env_layout.addWidget(self.label_7)
        r_env_layout.addWidget(self.lineEdit_r_env_dir)
        left_layout.addLayout(r_env_layout)

        workplace_layout = QHBoxLayout()
        workplace_layout.setSpacing(5)
        self.label_8 = QLabel()
        self.label_8.setObjectName("label_8")
        self.label_8.setText("Workplace dir:")
        self.label_8.setFixedWidth(100)
        self.lineEdit_workplace_dir = QLineEdit()
        self.lineEdit_workplace_dir.setObjectName("lineEdit_workplace_dir")
        workplace_layout.addWidget(self.label_8)
        workplace_layout.addWidget(self.lineEdit_workplace_dir)
        left_layout.addLayout(workplace_layout)

        left_layout.addStretch()

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        calibration_group = QGroupBox()
        calibration_layout = QVBoxLayout(calibration_group)
        calibration_layout.setSpacing(5)
        self.checkBox_mass_calibration = QCheckBox()
        self.checkBox_mass_calibration.setObjectName("checkBox_mass_calibration")
        self.checkBox_mass_calibration.setText("Mass Calibration")
        self.checkBox_mass_calibration.setChecked(False)
        self.checkBox_ms_calibration = QCheckBox()
        self.checkBox_ms_calibration.setObjectName("checkBox_ms_calibration")
        self.checkBox_ms_calibration.setText("MS Calibration")
        calibration_layout.addWidget(self.checkBox_mass_calibration)
        calibration_layout.addWidget(self.checkBox_ms_calibration)
        right_layout.addWidget(calibration_group)

        mass_mode_layout = QHBoxLayout()
        self.label_5 = QLabel()
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Mass Mode")
        self.radioButton_M_mode = QRadioButton()
        self.radioButton_M_mode.setObjectName("radioButton_M_mode")
        self.radioButton_M_mode.setText("M")
        self.radioButton_M_add_H_mode = QRadioButton()
        self.radioButton_M_add_H_mode.setObjectName("radioButton_M_add_H_mode")
        self.radioButton_M_add_H_mode.setText("MH+")
        mass_mode_layout.addWidget(self.label_5)
        mass_mode_layout.addWidget(self.radioButton_M_mode)
        mass_mode_layout.addWidget(self.radioButton_M_add_H_mode)
        mass_mode_layout.addStretch()
        right_layout.addLayout(mass_mode_layout)

        error_group = QGroupBox()
        error_layout = QVBoxLayout(error_group)
        error_layout.setSpacing(5)

        terminal_error_layout = QHBoxLayout()
        self.label_10 = QLabel()
        self.label_10.setObjectName("label_10")
        self.label_10.setText("Terminal mass error (ppm)")
        self.spinBox_terminal_mass_error = QSpinBox()
        self.spinBox_terminal_mass_error.setObjectName("spinBox_terminal_mass_error")
        self.spinBox_terminal_mass_error.setRange(1, 100)
        self.spinBox_terminal_mass_error.setValue(10)
        terminal_error_layout.addWidget(self.label_10)
        terminal_error_layout.addWidget(self.spinBox_terminal_mass_error)
        terminal_error_layout.addStretch()
        error_layout.addLayout(terminal_error_layout)

        internal_error_layout = QHBoxLayout()
        self.label_13 = QLabel()
        self.label_13.setObjectName("label_13")
        self.label_13.setText("Internal mass error (ppm)")
        self.spinBox_internal_mass_error = QSpinBox()
        self.spinBox_internal_mass_error.setObjectName("spinBox_internal_mass_error")
        self.spinBox_internal_mass_error.setRange(1, 100)
        self.spinBox_internal_mass_error.setValue(10)
        internal_error_layout.addWidget(self.label_13)
        internal_error_layout.addWidget(self.spinBox_internal_mass_error)
        internal_error_layout.addStretch()
        error_layout.addLayout(internal_error_layout)

        peak_error_layout = QHBoxLayout()
        self.label_11 = QLabel()
        self.label_11.setObjectName("label_11")
        self.label_11.setText("Peak match error (ppm)")
        self.spinBox_peak_match_error = QSpinBox()
        self.spinBox_peak_match_error.setObjectName("spinBox_peak_match_error")
        self.spinBox_peak_match_error.setRange(1, 100)
        self.spinBox_peak_match_error.setValue(10)
        peak_error_layout.addWidget(self.label_11)
        peak_error_layout.addWidget(self.spinBox_peak_match_error)
        peak_error_layout.addStretch()
        error_layout.addLayout(peak_error_layout)
        right_layout.addWidget(error_group)

        n_terminal_group = QGroupBox()
        n_terminal_layout = QVBoxLayout(n_terminal_group)
        self.label_9 = QLabel()
        self.label_9.setObjectName("label_9")
        self.label_9.setText("N-Terminal Frag Type:")
        n_terminal_layout.addWidget(self.label_9)
        self._create_ion_checkboxes_n_terminal_layout(n_terminal_layout)
        right_layout.addWidget(n_terminal_group)

        c_terminal_group = QGroupBox()
        c_terminal_layout = QVBoxLayout(c_terminal_group)
        self.label_14 = QLabel()
        self.label_14.setObjectName("label_14")
        self.label_14.setText("C-Terminal Frag Type:")
        c_terminal_layout.addWidget(self.label_14)
        self._create_ion_checkboxes_c_terminal_layout(c_terminal_layout)
        right_layout.addWidget(c_terminal_group)

        internal_group = QGroupBox()
        internal_frag_layout = QVBoxLayout(internal_group)
        self.label_12 = QLabel()
        self.label_12.setObjectName("label_12")
        self.label_12.setText("Internal Frag Type:")
        internal_frag_layout.addWidget(self.label_12)
        self._create_ion_checkboxes_internal_layout(internal_frag_layout)
        right_layout.addWidget(internal_group)

        right_layout.addStretch()

        bottom_left_widget = QWidget()
        bottom_left_layout = QVBoxLayout(bottom_left_widget)
        bottom_left_layout.setContentsMargins(0, 0, 0, 0)
        bottom_left_layout.setSpacing(5)
        self.textBrowser_process_info = QTextBrowser()
        self.textBrowser_process_info.setObjectName("textBrowser_process_info")
        self.textBrowser_process_info.setReadOnly(True)
        self.textBrowser_process_info.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        bottom_left_layout.addWidget(self.textBrowser_process_info)

        bottom_right_widget = QWidget()
        bottom_right_layout = QHBoxLayout(bottom_right_widget)
        bottom_right_layout.setContentsMargins(0, 0, 0, 0)
        bottom_right_layout.setSpacing(10)
        self.pushButton_clear_process_info = QPushButton()
        self.pushButton_clear_process_info.setObjectName(
            "pushButton_clear_process_info"
        )
        self.pushButton_save_param = QPushButton()
        self.pushButton_save_param.setObjectName("pushButton_save_param")
        self.pushButton_run = QPushButton()
        self.pushButton_run.setObjectName("pushButton_run")
        self.pushButton_abort = QPushButton()
        self.pushButton_abort.setObjectName("pushButton_abort")
        bottom_right_layout.addWidget(self.pushButton_clear_process_info)
        bottom_right_layout.addWidget(self.pushButton_save_param)
        bottom_right_layout.addWidget(self.pushButton_run)
        bottom_right_layout.addWidget(self.pushButton_abort)

        main_layout.addWidget(left_widget, 0, 0)
        main_layout.addWidget(right_widget, 0, 1)
        main_layout.addWidget(bottom_left_widget, 1, 0)
        main_layout.addWidget(bottom_right_widget, 1, 1)
        main_layout.setRowStretch(0, 3)
        main_layout.setRowStretch(1, 1)
        main_layout.setColumnStretch(0, 3)
        main_layout.setColumnStretch(1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1100, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_load_param.clicked.connect(MainWindow.load_param)
        self.pushButton_save_param.clicked.connect(MainWindow.save_param)
        self.pushButton_run.clicked.connect(MainWindow.run)
        self.pushButton_abort.clicked.connect(MainWindow.abort)
        self.pushButton_clear_process_info.clicked.connect(
            self.textBrowser_process_info.clear
        )
        self.pushButton_add_scan.clicked.connect(MainWindow.add_scan_row)
        self.pushButton_remove_scan.clicked.connect(MainWindow.remove_scan_row)
        self.pushButton_add_fixed_mod.clicked.connect(MainWindow.add_fixed_mod_row)
        self.pushButton_remove_fixed_mod.clicked.connect(
            MainWindow.remove_fixed_mod_row
        )
        self.pushButton_add_unloc_mod.clicked.connect(MainWindow.add_unloc_mod_row)
        self.pushButton_remove_unloc_mod.clicked.connect(
            MainWindow.remove_unloc_mod_row
        )
        self.pushButton_add_prsm_id.clicked.connect(MainWindow.add_prsm_id_row)
        self.pushButton_remove_prsm_id.clicked.connect(MainWindow.remove_prsm_id_row)

        QMetaObject.connectSlotsByName(MainWindow)

    def _create_ion_checkboxes_n_terminal_layout(self, parent_layout):
        n_terminal_ion_layout = QHBoxLayout()
        n_terminal_ion_layout.setSpacing(5)
        self.checkBox_a_ion_type = QCheckBox()
        self.checkBox_a_ion_type.setObjectName("checkBox_a_ion_type")
        self.checkBox_a_ion_type.setText("a")
        self.checkBox_a_add_H_ion_type = QCheckBox()
        self.checkBox_a_add_H_ion_type.setObjectName("checkBox_a_add_H_ion_type")
        self.checkBox_a_add_H_ion_type.setText("a+1")
        self.checkBox_a_sub_H_ion_type = QCheckBox()
        self.checkBox_a_sub_H_ion_type.setObjectName("checkBox_a_sub_H_ion_type")
        self.checkBox_a_sub_H_ion_type.setText("a-1")
        self.checkBox_b_ion_type = QCheckBox()
        self.checkBox_b_ion_type.setObjectName("checkBox_b_ion_type")
        self.checkBox_b_ion_type.setText("b")
        self.checkBox_c_ion_type = QCheckBox()
        self.checkBox_c_ion_type.setObjectName("checkBox_c_ion_type")
        self.checkBox_c_ion_type.setText("c")
        self.checkBox_c_dot_ion_type = QCheckBox()
        self.checkBox_c_dot_ion_type.setObjectName("checkBox_c_dot_ion_type")
        self.checkBox_c_dot_ion_type.setText("c.")
        n_terminal_ion_layout.addWidget(self.checkBox_a_ion_type)
        n_terminal_ion_layout.addWidget(self.checkBox_a_add_H_ion_type)
        n_terminal_ion_layout.addWidget(self.checkBox_a_sub_H_ion_type)
        n_terminal_ion_layout.addWidget(self.checkBox_b_ion_type)
        n_terminal_ion_layout.addWidget(self.checkBox_c_ion_type)
        n_terminal_ion_layout.addWidget(self.checkBox_c_dot_ion_type)
        n_terminal_ion_layout.addStretch()
        parent_layout.addLayout(n_terminal_ion_layout)

    def _create_ion_checkboxes_c_terminal_layout(self, parent_layout):
        c_terminal_ion_layout = QHBoxLayout()
        c_terminal_ion_layout.setSpacing(5)
        self.checkBox_x_ion_type = QCheckBox()
        self.checkBox_x_ion_type.setObjectName("checkBox_x_ion_type")
        self.checkBox_x_ion_type.setText("x")
        self.checkBox_x_add_H_ion_type = QCheckBox()
        self.checkBox_x_add_H_ion_type.setObjectName("checkBox_x_add_H_ion_type")
        self.checkBox_x_add_H_ion_type.setText("x+1")
        self.checkBox_x_sub_H_ion_type = QCheckBox()
        self.checkBox_x_sub_H_ion_type.setObjectName("checkBox_x_sub_H_ion_type")
        self.checkBox_x_sub_H_ion_type.setText("x-1")
        self.checkBox_y_ion_type = QCheckBox()
        self.checkBox_y_ion_type.setObjectName("checkBox_y_ion_type")
        self.checkBox_y_ion_type.setText("y")
        self.checkBox_y_sub_H_ion_type = QCheckBox()
        self.checkBox_y_sub_H_ion_type.setObjectName("checkBox_y_sub_H_ion_type")
        self.checkBox_y_sub_H_ion_type.setText("y-1")
        self.checkBox_y_sub_H2_ion_type = QCheckBox()
        self.checkBox_y_sub_H2_ion_type.setObjectName("checkBox_y_sub_H2_ion_type")
        self.checkBox_y_sub_H2_ion_type.setText("y-2")
        self.checkBox_z_ion_type = QCheckBox()
        self.checkBox_z_ion_type.setObjectName("checkBox_z_ion_type")
        self.checkBox_z_ion_type.setText("z")
        self.checkBox_z_add_H_ion_type = QCheckBox()
        self.checkBox_z_add_H_ion_type.setObjectName("checkBox_z_add_H_ion_type")
        self.checkBox_z_add_H_ion_type.setText("z+1")
        self.checkBox_z_sub_H_ion_type = QCheckBox()
        self.checkBox_z_sub_H_ion_type.setObjectName("checkBox_z_sub_H_ion_type")
        self.checkBox_z_sub_H_ion_type.setText("z-1")
        c_terminal_ion_layout.addWidget(self.checkBox_x_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_x_add_H_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_x_sub_H_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_y_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_y_sub_H_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_y_sub_H2_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_z_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_z_add_H_ion_type)
        c_terminal_ion_layout.addWidget(self.checkBox_z_sub_H_ion_type)
        c_terminal_ion_layout.addStretch()
        parent_layout.addLayout(c_terminal_ion_layout)

    def _create_ion_checkboxes_internal_layout(self, parent_layout):
        internal_ion_layout = QHBoxLayout()
        internal_ion_layout.setSpacing(5)
        self.checkBox_ax_ion_type = QCheckBox()
        self.checkBox_ax_ion_type.setObjectName("checkBox_ax_ion_type")
        self.checkBox_ax_ion_type.setText("ax")
        self.checkBox_ay_ion_type = QCheckBox()
        self.checkBox_ay_ion_type.setObjectName("checkBox_ay_ion_type")
        self.checkBox_ay_ion_type.setText("ay")
        self.checkBox_az_add_H2_ion_type = QCheckBox()
        self.checkBox_az_add_H2_ion_type.setObjectName("checkBox_az_add_H2_ion_type")
        self.checkBox_az_add_H2_ion_type.setText("az+2")
        self.checkBox_bx_ion_type = QCheckBox()
        self.checkBox_bx_ion_type.setObjectName("checkBox_bx_ion_type")
        self.checkBox_bx_ion_type.setText("bx")
        self.checkBox_by_ion_type = QCheckBox()
        self.checkBox_by_ion_type.setObjectName("checkBox_by_ion_type")
        self.checkBox_by_ion_type.setText("by")
        self.checkBox_bz_add_H2_ion_type = QCheckBox()
        self.checkBox_bz_add_H2_ion_type.setObjectName("checkBox_bz_add_H2_ion_type")
        self.checkBox_bz_add_H2_ion_type.setText("bz+2")
        self.checkBox_cx_ion_type = QCheckBox()
        self.checkBox_cx_ion_type.setObjectName("checkBox_cx_ion_type")
        self.checkBox_cx_ion_type.setText("cx")
        self.checkBox_cy_ion_type = QCheckBox()
        self.checkBox_cy_ion_type.setObjectName("checkBox_cy_ion_type")
        self.checkBox_cy_ion_type.setText("cy")
        self.checkBox_cz_ion_type = QCheckBox()
        self.checkBox_cz_ion_type.setObjectName("checkBox_cz_ion_type")
        self.checkBox_cz_ion_type.setText("cz")
        internal_ion_layout.addWidget(self.checkBox_ax_ion_type)
        internal_ion_layout.addWidget(self.checkBox_ay_ion_type)
        internal_ion_layout.addWidget(self.checkBox_az_add_H2_ion_type)
        internal_ion_layout.addWidget(self.checkBox_bx_ion_type)
        internal_ion_layout.addWidget(self.checkBox_by_ion_type)
        internal_ion_layout.addWidget(self.checkBox_bz_add_H2_ion_type)
        internal_ion_layout.addWidget(self.checkBox_cx_ion_type)
        internal_ion_layout.addWidget(self.checkBox_cy_ion_type)
        internal_ion_layout.addWidget(self.checkBox_cz_ion_type)
        internal_ion_layout.addStretch()
        parent_layout.addLayout(internal_ion_layout)

    # setupUi 
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Panda-UV", None)
        )
        self.pushButton_load_param.setText(
            QCoreApplication.translate("MainWindow", "Load param", None)
        )
        self.lineEdit_param_file_dir.setText(
            QCoreApplication.translate("MainWindow", "param_file_dir", None)
        )
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Scan-Sequence:", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("MainWindow", "MSAlign file:", None)
        )
        self.lineEdit_msalign_file_dir.setText(
            QCoreApplication.translate("MainWindow", "msalign_file_dir", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "Fixed mod:", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("MainWindow", "R env dir", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("MainWindow", "Terminal mass error(ppm)", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("MainWindow", "Peak match error(ppm)", None)
        )
        self.checkBox_mass_calibration.setText(
            QCoreApplication.translate("MainWindow", "Mass Calibration", None)
        )
        self.checkBox_ms_calibration.setText(
            QCoreApplication.translate("MainWindow", "MS Calibration", None)
        )
        self.pushButton_save_param.setText(
            QCoreApplication.translate("MainWindow", "Save param", None)
        )
        self.pushButton_run.setText(
            QCoreApplication.translate("MainWindow", "Run", None)
        )
        self.pushButton_abort.setText(
            QCoreApplication.translate("MainWindow", "Abort", None)
        )
        self.textBrowser_process_info.setHtml(
            QCoreApplication.translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Arial'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'SimSun\'; font-size:9pt;">Process info....</span></p></body></html>',
                None,
            )
        )
        self.pushButton_clear_process_info.setText(
            QCoreApplication.translate("MainWindow", "Clear process info ", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("MainWindow", "N-Terminal Frag Type:", None)
        )
        self.label_12.setText(
            QCoreApplication.translate("MainWindow", "Internal Frag Type", None)
        )
        self.checkBox_a_ion_type.setText(
            QCoreApplication.translate("MainWindow", "a", None)
        )
        self.checkBox_a_add_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "a+1", None)
        )
        self.checkBox_b_ion_type.setText(
            QCoreApplication.translate("MainWindow", "b", None)
        )
        self.checkBox_a_sub_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "a-1", None)
        )
        self.checkBox_x_ion_type.setText(
            QCoreApplication.translate("MainWindow", "x", None)
        )
        self.checkBox_x_add_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "x+1", None)
        )
        self.checkBox_c_ion_type.setText(
            QCoreApplication.translate("MainWindow", "c", None)
        )
        self.checkBox_c_dot_ion_type.setText(
            QCoreApplication.translate("MainWindow", "c.", None)
        )
        self.checkBox_z_sub_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "z-1", None)
        )
        self.checkBox_z_add_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "z+1", None)
        )
        self.checkBox_z_ion_type.setText(
            QCoreApplication.translate("MainWindow", "z", None)
        )
        self.checkBox_x_sub_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "x-1", None)
        )
        self.checkBox_y_ion_type.setText(
            QCoreApplication.translate("MainWindow", "y", None)
        )
        self.checkBox_y_sub_H_ion_type.setText(
            QCoreApplication.translate("MainWindow", "y-1", None)
        )
        self.checkBox_bz_add_H2_ion_type.setText(
            QCoreApplication.translate("MainWindow", "bz", None)
        )
        self.checkBox_by_ion_type.setText(
            QCoreApplication.translate("MainWindow", "by", None)
        )
        self.checkBox_bx_ion_type.setText(
            QCoreApplication.translate("MainWindow", "bx", None)
        )
        self.checkBox_ax_ion_type.setText(
            QCoreApplication.translate("MainWindow", "ax", None)
        )
        self.checkBox_ay_ion_type.setText(
            QCoreApplication.translate("MainWindow", "ay", None)
        )
        self.checkBox_az_add_H2_ion_type.setText(
            QCoreApplication.translate("MainWindow", "az", None)
        )
        self.checkBox_cx_ion_type.setText(
            QCoreApplication.translate("MainWindow", "cx", None)
        )
        self.checkBox_cz_ion_type.setText(
            QCoreApplication.translate("MainWindow", "cz", None)
        )
        self.checkBox_cy_ion_type.setText(
            QCoreApplication.translate("MainWindow", "cy", None)
        )
        self.label_13.setText(
            QCoreApplication.translate("MainWindow", "Internal mass error(ppm)", None)
        )
        self.radioButton_M_mode.setText(
            QCoreApplication.translate("MainWindow", "M", None)
        )
        self.radioButton_M_add_H_mode.setText(
            QCoreApplication.translate("MainWindow", "MH+", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Mass Mode", None)
        )
        self.label_14.setText(
            QCoreApplication.translate("MainWindow", "C-Terminal Frag Type:", None)
        )
        self.lineEdit_workplace_dir.setText(
            QCoreApplication.translate("MainWindow", "workplace_dir", None)
        )
        self.label_8.setText(
            QCoreApplication.translate("MainWindow", "Workplace dir", None)
        )
        self.label_15.setText(
            QCoreApplication.translate("MainWindow", "mzML dir", None)
        )
        self.lineEdit_mzml_file_dir.setText(
            QCoreApplication.translate("MainWindow", "mzml_file_dir", None)
        )
        self.checkBox_y_sub_H2_ion_type.setText(
            QCoreApplication.translate("MainWindow", "y-2", None)
        )

    # retranslateUi


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化界面
        self.setupUi(self)
        # 设置图标
        self.setWindowIcon(QIcon(":/Icon.ico"))
        # 初始化param
        self.param = Param()
        # 实例一直保存，方便查看运行状态
        self.main_run = PANDA_UV_main()
        self.main_run.process_info.connect(self.showProcessInfo)
        # 输出重定向到UI
        sys.stdout = self.main_run

    def add_scan_row(self):
        row_count = self.tableWidget_sequence.rowCount()
        self.tableWidget_sequence.insertRow(row_count)

    def remove_scan_row(self):
        current_row = self.tableWidget_sequence.currentRow()
        if current_row >= 0:
            self.tableWidget_sequence.removeRow(current_row)

    def add_fixed_mod_row(self):
        row_count = self.tableWidget_fixed_mod.rowCount()
        self.tableWidget_fixed_mod.insertRow(row_count)

    def remove_fixed_mod_row(self):
        current_row = self.tableWidget_fixed_mod.currentRow()
        if current_row >= 0:
            self.tableWidget_fixed_mod.removeRow(current_row)

    def add_unloc_mod_row(self):
        row_count = self.tableWidget_unloc_mod.rowCount()
        self.tableWidget_unloc_mod.insertRow(row_count)

    def remove_unloc_mod_row(self):
        current_row = self.tableWidget_unloc_mod.currentRow()
        if current_row >= 0:
            self.tableWidget_unloc_mod.removeRow(current_row)

    def add_prsm_id_row(self):
        row_count = self.tableWidget_prsm_id.rowCount()
        self.tableWidget_prsm_id.insertRow(row_count)

    def remove_prsm_id_row(self):
        current_row = self.tableWidget_prsm_id.currentRow()
        if current_row >= 0:
            self.tableWidget_prsm_id.removeRow(current_row)

    # 选择参数文件并加载到界面，初始化参数类
    def load_param(self):
        filename, filetype_str = QFileDialog.getOpenFileName(
            caption="Select a parameter file", filter="Parameter file (*.json *.yaml)"
        )
        if os.path.isfile(filename):
            self.lineEdit_param_file_dir.setText(filename)
            print(f"Open file:{filename}")
            self.param.read_param(filename)
            self.refresh_param()
        else:
            print("Please select a valid parameter file.")

    # 加载配置参数到界面
    def refresh_param(self, param_dict=None):
        if param_dict is None:
            param_dict = dict(self.param)
        else:
            pass

        self._refresh_sequence_table(param_dict)
        self._refresh_ion_type_checkboxes(param_dict)
        self._refresh_fixed_mod_table(param_dict)
        self._refresh_unloc_mod_table(param_dict)
        self._refresh_prsm_id_table(param_dict)

        self.lineEdit_msalign_file_dir.setText(param_dict.get("msalign_file_dir", ""))
        self.lineEdit_r_env_dir.setText(param_dict.get("r_env_dir", ""))
        self.lineEdit_mzml_file_dir.setText(param_dict.get("mzml_file_dir", ""))
        self.lineEdit_workplace_dir.setText(param_dict.get("workplace_dir", ""))
        self.checkBox_mass_calibration.setChecked(
            param_dict.get("mass_calibration", False)
        )
        self.checkBox_ms_calibration.setChecked(param_dict.get("ms_calibration", False))
        mass_mode = param_dict.get("mass_mode", "M")
        if mass_mode == "M":
            self.radioButton_M_mode.setChecked(True)
        else:
            self.radioButton_M_add_H_mode.setChecked(True)
        self.spinBox_terminal_mass_error.setValue(
            param_dict.get("terminal_mass_error", 10)
        )
        self.spinBox_internal_mass_error.setValue(
            param_dict.get("internal_mass_error", 10)
        )
        self.spinBox_peak_match_error.setValue(param_dict.get("peak_match_error", 10))

    def _refresh_sequence_table(self, param_dict):
        self.tableWidget_sequence.setRowCount(0)
        sequence = param_dict.get("sequence", {})
        if isinstance(sequence, dict):
            self.tableWidget_sequence.setRowCount(len(sequence))
            for i, (scan_id, seq) in enumerate(sequence.items()):
                self.tableWidget_sequence.setItem(i, 0, QTableWidgetItem(str(scan_id)))
                self.tableWidget_sequence.setItem(i, 1, QTableWidgetItem(str(seq)))

    def _refresh_ion_type_checkboxes(self, param_dict):
        for cb in [
            self.checkBox_a_ion_type,
            self.checkBox_a_add_H_ion_type,
            self.checkBox_a_sub_H_ion_type,
            self.checkBox_b_ion_type,
            self.checkBox_c_ion_type,
            self.checkBox_c_dot_ion_type,
            self.checkBox_x_ion_type,
            self.checkBox_x_add_H_ion_type,
            self.checkBox_x_sub_H_ion_type,
            self.checkBox_y_ion_type,
            self.checkBox_y_sub_H_ion_type,
            self.checkBox_y_sub_H2_ion_type,
            self.checkBox_z_ion_type,
            self.checkBox_z_add_H_ion_type,
            self.checkBox_z_sub_H_ion_type,
            self.checkBox_ax_ion_type,
            self.checkBox_ay_ion_type,
            self.checkBox_az_add_H2_ion_type,
            self.checkBox_bx_ion_type,
            self.checkBox_by_ion_type,
            self.checkBox_bz_add_H2_ion_type,
            self.checkBox_cx_ion_type,
            self.checkBox_cy_ion_type,
            self.checkBox_cz_ion_type,
        ]:
            cb.setChecked(False)

        ion_map = {
            "a": self.checkBox_a_ion_type,
            "a+1": self.checkBox_a_add_H_ion_type,
            "a-1": self.checkBox_a_sub_H_ion_type,
            "b": self.checkBox_b_ion_type,
            "c": self.checkBox_c_ion_type,
            "c.": self.checkBox_c_dot_ion_type,
            "x": self.checkBox_x_ion_type,
            "x+1": self.checkBox_x_add_H_ion_type,
            "x-1": self.checkBox_x_sub_H_ion_type,
            "y": self.checkBox_y_ion_type,
            "y-1": self.checkBox_y_sub_H_ion_type,
            "y-2": self.checkBox_y_sub_H2_ion_type,
            "z": self.checkBox_z_ion_type,
            "z+1": self.checkBox_z_add_H_ion_type,
            "z-1": self.checkBox_z_sub_H_ion_type,
            "ax": self.checkBox_ax_ion_type,
            "ay": self.checkBox_ay_ion_type,
            "az+2": self.checkBox_az_add_H2_ion_type,
            "bx": self.checkBox_bx_ion_type,
            "by": self.checkBox_by_ion_type,
            "bz+2": self.checkBox_bz_add_H2_ion_type,
            "cx": self.checkBox_cx_ion_type,
            "cy": self.checkBox_cy_ion_type,
            "cz": self.checkBox_cz_ion_type,
        }
        for it in param_dict.get("n_terminal_frag_type", []):
            if it in ion_map:
                ion_map[it].setChecked(True)
        for it in param_dict.get("c_terminal_frag_type", []):
            if it in ion_map:
                ion_map[it].setChecked(True)
        for it in param_dict.get("internal_frag_type", []):
            if it in ion_map:
                ion_map[it].setChecked(True)

    def _refresh_fixed_mod_table(self, param_dict):
        self.tableWidget_fixed_mod.setRowCount(0)
        fixed_mod = param_dict.get("fixed_mod", {})
        header = fixed_mod.get("header", ["name", "formula", "loc"])
        new_header = ["scan"] + header
        self.tableWidget_fixed_mod.setColumnCount(len(new_header))
        self.tableWidget_fixed_mod.setHorizontalHeaderLabels(new_header)

        rows = []
        for scan in sorted(fixed_mod.keys()):
            if scan == "header":
                continue
            scan_data = fixed_mod[scan]
            if isinstance(scan_data, list):
                for row in scan_data:
                    rows.append([scan] + row)
            else:
                rows.append([scan] + scan_data)

        self.tableWidget_fixed_mod.setRowCount(len(rows))
        for i, row_data in enumerate(rows):
            for j, val in enumerate(row_data):
                self.tableWidget_fixed_mod.setItem(i, j, QTableWidgetItem(str(val)))

    def _refresh_unloc_mod_table(self, param_dict):
        self.tableWidget_unloc_mod.setRowCount(0)
        unloc_mod = param_dict.get("unloc_mod", {})
        header = unloc_mod.get(
            "header", ["name", "formula", "start_loc", "end_loc", "ion type"]
        )
        new_header = ["scan"] + header
        self.tableWidget_unloc_mod.setColumnCount(len(new_header))
        self.tableWidget_unloc_mod.setHorizontalHeaderLabels(new_header)

        rows = []
        for scan in sorted(unloc_mod.keys()):
            if scan == "header":
                continue
            scan_data = unloc_mod[scan]
            if isinstance(scan_data, list):
                for row in scan_data:
                    rows.append([scan] + row)
            else:
                rows.append([scan] + scan_data)

        self.tableWidget_unloc_mod.setRowCount(len(rows))
        for i, row_data in enumerate(rows):
            for j, val in enumerate(row_data):
                self.tableWidget_unloc_mod.setItem(i, j, QTableWidgetItem(str(val)))

    def _refresh_prsm_id_table(self, param_dict):
        self.tableWidget_prsm_id.setRowCount(0)
        prsm_id = param_dict.get("prsm_id", {})
        rows = [[k, v] for k, v in sorted(prsm_id.items())]
        self.tableWidget_prsm_id.setRowCount(len(rows))
        for i, (scan, prsm) in enumerate(rows):
            self.tableWidget_prsm_id.setItem(i, 0, QTableWidgetItem(str(scan)))
            self.tableWidget_prsm_id.setItem(i, 1, QTableWidgetItem(str(prsm)))

    # 保存界面输入的参数到param类
    def save_param(self):
        param_dict = dict(self.param)

        self._save_sequence_from_table(param_dict)
        self._save_fixed_mod_from_table(param_dict)
        self._save_unloc_mod_from_table(param_dict)
        self._save_prsm_id_from_table(param_dict)

        param_dict["msalign_file_dir"] = self.lineEdit_msalign_file_dir.text()
        param_dict["r_env_dir"] = self.lineEdit_r_env_dir.text()
        param_dict["mzml_file_dir"] = self.lineEdit_mzml_file_dir.text()
        param_dict["workplace_dir"] = self.lineEdit_workplace_dir.text()
        param_dict["mass_calibration"] = self.checkBox_mass_calibration.isChecked()
        param_dict["ms_calibration"] = self.checkBox_ms_calibration.isChecked()
        param_dict["mass_mode"] = "M" if self.radioButton_M_mode.isChecked() else "MH+"
        param_dict["terminal_mass_error"] = self.spinBox_terminal_mass_error.value()
        param_dict["internal_mass_error"] = self.spinBox_internal_mass_error.value()
        param_dict["peak_match_error"] = self.spinBox_peak_match_error.value()

        n_terminal_list = []
        c_terminal_list = []
        internal_list = []
        if self.checkBox_a_ion_type.isChecked():
            n_terminal_list.append("a")
        if self.checkBox_a_add_H_ion_type.isChecked():
            n_terminal_list.append("a+1")
        if self.checkBox_a_sub_H_ion_type.isChecked():
            n_terminal_list.append("a-1")
        if self.checkBox_b_ion_type.isChecked():
            n_terminal_list.append("b")
        if self.checkBox_c_ion_type.isChecked():
            n_terminal_list.append("c")
        if self.checkBox_c_dot_ion_type.isChecked():
            n_terminal_list.append("c.")
        param_dict["n_terminal_frag_type"] = n_terminal_list

        if self.checkBox_x_ion_type.isChecked():
            c_terminal_list.append("x")
        if self.checkBox_x_add_H_ion_type.isChecked():
            c_terminal_list.append("x+1")
        if self.checkBox_x_sub_H_ion_type.isChecked():
            c_terminal_list.append("x-1")
        if self.checkBox_y_ion_type.isChecked():
            c_terminal_list.append("y")
        if self.checkBox_y_sub_H_ion_type.isChecked():
            c_terminal_list.append("y-1")
        if self.checkBox_y_sub_H2_ion_type.isChecked():
            c_terminal_list.append("y-2")
        if self.checkBox_z_ion_type.isChecked():
            c_terminal_list.append("z")
        if self.checkBox_z_add_H_ion_type.isChecked():
            c_terminal_list.append("z+1")
        if self.checkBox_z_sub_H_ion_type.isChecked():
            c_terminal_list.append("z-1")
        param_dict["c_terminal_frag_type"] = c_terminal_list

        if self.checkBox_ax_ion_type.isChecked():
            internal_list.append("ax")
        if self.checkBox_ay_ion_type.isChecked():
            internal_list.append("ay")
        if self.checkBox_az_add_H2_ion_type.isChecked():
            internal_list.append("az+2")
        if self.checkBox_bx_ion_type.isChecked():
            internal_list.append("bx")
        if self.checkBox_by_ion_type.isChecked():
            internal_list.append("by")
        if self.checkBox_bz_add_H2_ion_type.isChecked():
            internal_list.append("bz+2")
        if self.checkBox_cx_ion_type.isChecked():
            internal_list.append("cx")
        if self.checkBox_cy_ion_type.isChecked():
            internal_list.append("cy")
        if self.checkBox_cz_ion_type.isChecked():
            internal_list.append("cz")
        param_dict["internal_frag_type"] = internal_list

        self.param.update(param_dict)
        self.param.save_param()
        print("Param file saved")

    def _save_sequence_from_table(self, param_dict):
        sequence = {}
        for i in range(self.tableWidget_sequence.rowCount()):
            scan_id_item = self.tableWidget_sequence.item(i, 0)
            seq_item = self.tableWidget_sequence.item(i, 1)
            if scan_id_item and seq_item:
                scan_id = scan_id_item.text().strip()
                seq = seq_item.text().strip()
                if scan_id and seq:
                    sequence[scan_id] = seq
        param_dict["sequence"] = sequence
        param_dict["scans"] = [int(k) for k in sequence.keys()]

    def _save_fixed_mod_from_table(self, param_dict):
        header = ["name", "formula", "loc"]
        fixed_mod = {"header": header}
        scan_data = {}
        for i in range(self.tableWidget_fixed_mod.rowCount()):
            scan = self.tableWidget_fixed_mod.item(i, 0).text().strip()
            row = [
                self.tableWidget_fixed_mod.item(i, j).text().strip()
                for j in range(1, self.tableWidget_fixed_mod.columnCount())
            ]
            if scan and any(row):
                if scan not in scan_data:
                    scan_data[scan] = []
                scan_data[scan].append(row)
        for scan, data in scan_data.items():
            fixed_mod[scan] = data
        param_dict["fixed_mod"] = fixed_mod

    def _save_unloc_mod_from_table(self, param_dict):
        header = ["name", "formula", "start_loc", "end_loc", "ion type"]
        unloc_mod = {"header": header}
        scan_data = {}
        for i in range(self.tableWidget_unloc_mod.rowCount()):
            scan = self.tableWidget_unloc_mod.item(i, 0).text().strip()
            row = [
                self.tableWidget_unloc_mod.item(i, j).text().strip()
                for j in range(1, self.tableWidget_unloc_mod.columnCount())
            ]
            if scan and any(row):
                if scan not in scan_data:
                    scan_data[scan] = []
                scan_data[scan].append(row)
        for scan, data in scan_data.items():
            unloc_mod[scan] = data
        param_dict["unloc_mod"] = unloc_mod

    def _save_prsm_id_from_table(self, param_dict):
        prsm_id = {}
        for i in range(self.tableWidget_prsm_id.rowCount()):
            scan_item = self.tableWidget_prsm_id.item(i, 0)
            prsm_item = self.tableWidget_prsm_id.item(i, 1)
            if scan_item and prsm_item:
                scan = scan_item.text().strip()
                prsm = prsm_item.text().strip()
                if scan and prsm:
                    prsm_id[scan] = int(prsm)
        param_dict["prsm_id"] = prsm_id

    def run(self):
        self.save_param()
        self.param.read_param()
        self.offRunButton()
        self.main_run.param = dict(self.param)
        self.main_run.start()
        self.main_run.finished.connect(self.onRunButton)
        self.main_run.exit()

    def abort(self):
        if self.main_run.isRunning():
            self.main_run.stop()
            self.onRunButton()
        else:
            pass

    # 关闭除了Abort之外的按键
    def offRunButton(self):
        self.pushButton_load_param.setEnabled(False)
        self.pushButton_save_param.setEnabled(False)
        self.pushButton_run.setEnabled(False)
        self.pushButton_clear_process_info.setEnabled(False)

    def onRunButton(self):
        self.pushButton_load_param.setEnabled(True)
        self.pushButton_save_param.setEnabled(True)
        self.pushButton_run.setEnabled(True)
        self.pushButton_clear_process_info.setEnabled(True)
        # print(self.main_run.stackSize())

    def showProcessInfo(self, text):
        self.textBrowser_process_info.append(text)

    # 写write函数，将输出传递到信息框
    def write(self, text):
        self.showProcessInfo(text)
        QApplication.processEvents()

# 一个继承子QThread的类，线程开始时运行PANDA-UV主函数
class PANDA_UV_main(QThread):
    process_info = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 实例化时就设置堆栈数量
        self.setStackSize(4294967295)

    def write(self, text):
        self.process_info.emit(text)

    # def __del__(self):
    #    self.wait()

    # 参数属性在实例化之后添加
    def run(self):
        try:
            main(self.param)
        except Exception as exp:
            print(exp)

    def stop(self):
        print("Aborting....")
        self.terminate()

if __name__ == "__main__":
    app = QApplication([])
    win = MyMainWindow()
    win.show()
    app.exec()
