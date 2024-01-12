#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PANDA-UV_param_writerMYcDrw.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import QThread,pyqtSignal,QRect,Qt,QCoreApplication,QMetaObject
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QPushButton,QLineEdit,QLabel,QSpinBox,QCheckBox,QTextBrowser,QMenuBar,QStatusBar,QFileDialog,QRadioButton


# In[2]:


import yaml
import sys
import os


# In[3]:

# In[4]:


from Panda-UV_main import main


# In[5]:


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1001, 819)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_load_param = QPushButton(self.centralwidget)
        self.pushButton_load_param.setObjectName(u"pushButton_load_param")
        self.pushButton_load_param.setGeometry(QRect(120, 30, 86, 25))
        self.lineEdit_param_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_param_file_dir.setObjectName(u"lineEdit_param_file_dir")
        self.lineEdit_param_file_dir.setGeometry(QRect(310, 30, 271, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 90, 66, 17))
        self.label.setAlignment(Qt.AlignCenter)
        self.lineEdit_seq = QLineEdit(self.centralwidget)
        self.lineEdit_seq.setObjectName(u"lineEdit_seq")
        self.lineEdit_seq.setGeometry(QRect(310, 80, 271, 31))
        self.lineEdit_fixed_mod_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_fixed_mod_file_dir.setObjectName(u"lineEdit_fixed_mod_file_dir")
        self.lineEdit_fixed_mod_file_dir.setGeometry(QRect(310, 180, 271, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 190, 72, 17))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_unlocalized_mod_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_unlocalized_mod_file_dir.setObjectName(u"lineEdit_unlocalized_mod_file_dir")
        self.lineEdit_unlocalized_mod_file_dir.setGeometry(QRect(310, 230, 271, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 240, 108, 17))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(120, 140, 91, 17))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.lineEdit_deconv_mass_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_deconv_mass_file_dir.setObjectName(u"lineEdit_deconv_mass_file_dir")
        self.lineEdit_deconv_mass_file_dir.setGeometry(QRect(310, 130, 271, 31))
        self.lineEdit_r_env_dir = QLineEdit(self.centralwidget)
        self.lineEdit_r_env_dir.setObjectName(u"lineEdit_r_env_dir")
        self.lineEdit_r_env_dir.setGeometry(QRect(310, 280, 271, 31))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(120, 290, 58, 17))
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(640, 220, 191, 31))
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(640, 370, 191, 31))
        self.label_11.setAlignment(Qt.AlignCenter)
        self.spinBox_terminal_mass_error = QSpinBox(self.centralwidget)
        self.spinBox_terminal_mass_error.setObjectName(u"spinBox_terminal_mass_error")
        self.spinBox_terminal_mass_error.setGeometry(QRect(850, 220, 41, 31))
        self.spinBox_peak_match_error = QSpinBox(self.centralwidget)
        self.spinBox_peak_match_error.setObjectName(u"spinBox_peak_match_error")
        self.spinBox_peak_match_error.setGeometry(QRect(850, 370, 41, 31))
        self.checkBox_mass_calibration = QCheckBox(self.centralwidget)
        self.checkBox_mass_calibration.setObjectName(u"checkBox_mass_calibration")
        self.checkBox_mass_calibration.setGeometry(QRect(650, 34, 171, 31))
        self.checkBox_mass_calibration.setChecked(False)
        self.checkBox_ms_calibration = QCheckBox(self.centralwidget)
        self.checkBox_ms_calibration.setObjectName(u"checkBox_ms_calibration")
        self.checkBox_ms_calibration.setGeometry(QRect(650, 74, 171, 31))
        self.pushButton_save_param = QPushButton(self.centralwidget)
        self.pushButton_save_param.setObjectName(u"pushButton_save_param")
        self.pushButton_save_param.setGeometry(QRect(650, 580, 111, 31))
        self.pushButton_run = QPushButton(self.centralwidget)
        self.pushButton_run.setObjectName(u"pushButton_run")
        self.pushButton_run.setGeometry(QRect(650, 620, 111, 31))
        self.pushButton_abort = QPushButton(self.centralwidget)
        self.pushButton_abort.setObjectName(u"pushButton_abort")
        self.pushButton_abort.setGeometry(QRect(650, 660, 111, 31))
        self.textBrowser_process_info = QTextBrowser(self.centralwidget)
        self.textBrowser_process_info.setObjectName(u"textBrowser_process_info")
        self.textBrowser_process_info.setGeometry(QRect(160, 550, 421, 151))
        self.textBrowser_process_info.setReadOnly(True)
        self.pushButton_clear_process_info = QPushButton(self.centralwidget)
        self.pushButton_clear_process_info.setObjectName(u"pushButton_clear_process_info")
        self.pushButton_clear_process_info.setGeometry(QRect(200, 710, 201, 31))
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(120, 420, 161, 31))
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(120, 500, 161, 31))
        self.checkBox_a_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_a_ion_type.setObjectName(u"checkBox_a_ion_type")
        self.checkBox_a_ion_type.setGeometry(QRect(310, 430, 31, 16))
        self.checkBox_a_add_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_a_add_H_ion_type.setObjectName(u"checkBox_a_add_H_ion_type")
        self.checkBox_a_add_H_ion_type.setGeometry(QRect(370, 430, 41, 16))
        self.checkBox_b_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_b_ion_type.setObjectName(u"checkBox_b_ion_type")
        self.checkBox_b_ion_type.setGeometry(QRect(490, 430, 31, 16))
        self.checkBox_a_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_a_sub_H_ion_type.setObjectName(u"checkBox_a_sub_H_ion_type")
        self.checkBox_a_sub_H_ion_type.setGeometry(QRect(430, 430, 41, 16))
        self.checkBox_x_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_x_ion_type.setObjectName(u"checkBox_x_ion_type")
        self.checkBox_x_ion_type.setGeometry(QRect(310, 470, 31, 16))
        self.checkBox_x_add_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_x_add_H_ion_type.setObjectName(u"checkBox_x_add_H_ion_type")
        self.checkBox_x_add_H_ion_type.setGeometry(QRect(370, 470, 41, 16))
        self.checkBox_c_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_c_ion_type.setObjectName(u"checkBox_c_ion_type")
        self.checkBox_c_ion_type.setGeometry(QRect(550, 430, 31, 16))
        self.checkBox_c_dot_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_c_dot_ion_type.setObjectName(u"checkBox_c_dot_ion_type")
        self.checkBox_c_dot_ion_type.setGeometry(QRect(610, 430, 31, 16))
        self.checkBox_z_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_z_sub_H_ion_type.setObjectName(u"checkBox_z_sub_H_ion_type")
        self.checkBox_z_sub_H_ion_type.setGeometry(QRect(790, 470, 41, 16))
        self.checkBox_z_add_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_z_add_H_ion_type.setObjectName(u"checkBox_z_add_H_ion_type")
        self.checkBox_z_add_H_ion_type.setGeometry(QRect(730, 470, 41, 16))
        self.checkBox_z_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_z_ion_type.setObjectName(u"checkBox_z_ion_type")
        self.checkBox_z_ion_type.setGeometry(QRect(670, 470, 31, 16))
        self.checkBox_x_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_x_sub_H_ion_type.setObjectName(u"checkBox_x_sub_H_ion_type")
        self.checkBox_x_sub_H_ion_type.setGeometry(QRect(430, 470, 41, 16))
        self.checkBox_y_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_y_ion_type.setObjectName(u"checkBox_y_ion_type")
        self.checkBox_y_ion_type.setGeometry(QRect(490, 470, 31, 16))
        self.checkBox_y_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_y_sub_H_ion_type.setObjectName(u"checkBox_y_sub_H_ion_type")
        self.checkBox_y_sub_H_ion_type.setGeometry(QRect(550, 470, 41, 16))
        self.checkBox_bz_add_H2_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_bz_add_H2_ion_type.setObjectName(u"checkBox_bz_add_H2_ion_type")
        self.checkBox_bz_add_H2_ion_type.setGeometry(QRect(610, 510, 51, 16))
        self.checkBox_by_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_by_ion_type.setObjectName(u"checkBox_by_ion_type")
        self.checkBox_by_ion_type.setGeometry(QRect(550, 510, 41, 16))
        self.checkBox_bx_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_bx_ion_type.setObjectName(u"checkBox_bx_ion_type")
        self.checkBox_bx_ion_type.setGeometry(QRect(490, 510, 41, 16))
        self.checkBox_ax_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_ax_ion_type.setObjectName(u"checkBox_ax_ion_type")
        self.checkBox_ax_ion_type.setGeometry(QRect(310, 510, 41, 16))
        self.checkBox_ay_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_ay_ion_type.setObjectName(u"checkBox_ay_ion_type")
        self.checkBox_ay_ion_type.setGeometry(QRect(370, 510, 41, 16))
        self.checkBox_az_add_H2_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_az_add_H2_ion_type.setObjectName(u"checkBox_az_add_H2_ion_type")
        self.checkBox_az_add_H2_ion_type.setGeometry(QRect(430, 510, 51, 16))
        self.checkBox_cx_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_cx_ion_type.setObjectName(u"checkBox_cx_ion_type")
        self.checkBox_cx_ion_type.setGeometry(QRect(670, 510, 41, 16))
        self.checkBox_cz_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_cz_ion_type.setObjectName(u"checkBox_cz_ion_type")
        self.checkBox_cz_ion_type.setGeometry(QRect(790, 510, 41, 16))
        self.checkBox_cy_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_cy_ion_type.setObjectName(u"checkBox_cy_ion_type")
        self.checkBox_cy_ion_type.setGeometry(QRect(730, 510, 41, 16))
        self.spinBox_internal_mass_error = QSpinBox(self.centralwidget)
        self.spinBox_internal_mass_error.setObjectName(u"spinBox_internal_mass_error")
        self.spinBox_internal_mass_error.setGeometry(QRect(850, 271, 41, 31))
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(640, 270, 191, 31))
        self.label_13.setAlignment(Qt.AlignCenter)
        self.radioButton_M_mode = QRadioButton(self.centralwidget)
        self.radioButton_M_mode.setObjectName(u"radioButton_M_mode")
        self.radioButton_M_mode.setGeometry(QRect(650, 144, 89, 16))
        self.radioButton_M_add_H_mode = QRadioButton(self.centralwidget)
        self.radioButton_M_add_H_mode.setObjectName(u"radioButton_M_add_H_mode")
        self.radioButton_M_add_H_mode.setGeometry(QRect(650, 174, 71, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(650, 120, 81, 20))
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(120, 460, 161, 31))
        self.lineEdit_workplace_dir = QLineEdit(self.centralwidget)
        self.lineEdit_workplace_dir.setObjectName(u"lineEdit_workplace_dir")
        self.lineEdit_workplace_dir.setGeometry(QRect(310, 380, 271, 31))
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(120, 390, 90, 17))
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(120, 340, 61, 16))
        self.label_15.setAlignment(Qt.AlignCenter)
        self.lineEdit_mzml_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_mzml_file_dir.setObjectName(u"lineEdit_mzml_file_dir")
        self.lineEdit_mzml_file_dir.setGeometry(QRect(310, 330, 271, 31))
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(640, 320, 191, 31))
        self.label_16.setAlignment(Qt.AlignCenter)
        self.spinBox_scan_id = QSpinBox(self.centralwidget)
        self.spinBox_scan_id.setObjectName(u"spinBox_scan_id")
        self.spinBox_scan_id.setGeometry(QRect(850, 321, 41, 31))
        self.checkBox_y_sub_H2_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_y_sub_H2_ion_type.setObjectName(u"checkBox_y_sub_H2_ion_type")
        self.checkBox_y_sub_H2_ion_type.setGeometry(QRect(610, 470, 41, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1001, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_load_param, self.lineEdit_param_file_dir)
        QWidget.setTabOrder(self.lineEdit_param_file_dir, self.lineEdit_seq)
        QWidget.setTabOrder(self.lineEdit_seq, self.lineEdit_fixed_mod_file_dir)
        QWidget.setTabOrder(self.lineEdit_fixed_mod_file_dir, self.lineEdit_unlocalized_mod_file_dir)
        QWidget.setTabOrder(self.lineEdit_unlocalized_mod_file_dir, self.lineEdit_deconv_mass_file_dir)
        QWidget.setTabOrder(self.lineEdit_deconv_mass_file_dir, self.lineEdit_r_env_dir)
        QWidget.setTabOrder(self.lineEdit_r_env_dir, self.checkBox_mass_calibration)
        QWidget.setTabOrder(self.checkBox_mass_calibration, self.checkBox_ms_calibration)
        QWidget.setTabOrder(self.checkBox_ms_calibration, self.spinBox_terminal_mass_error)
        QWidget.setTabOrder(self.spinBox_terminal_mass_error, self.spinBox_peak_match_error)

        self.retranslateUi(MainWindow)
        self.pushButton_load_param.clicked.connect(MainWindow.load_param)
        self.pushButton_save_param.clicked.connect(MainWindow.save_param)
        self.pushButton_run.clicked.connect(MainWindow.run)
        self.pushButton_abort.clicked.connect(MainWindow.abort)
        self.pushButton_clear_process_info.clicked.connect(self.textBrowser_process_info.clear)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Panda-UV-2.0", None))
        self.pushButton_load_param.setText(QCoreApplication.translate("MainWindow", u"Load param", None))
        self.lineEdit_param_file_dir.setText(QCoreApplication.translate("MainWindow", u"param_file_dir", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sequence", None))
        self.lineEdit_seq.setText(QCoreApplication.translate("MainWindow", u"seq", None))
        self.lineEdit_fixed_mod_file_dir.setText(QCoreApplication.translate("MainWindow", u"fixed_mod_file_dir", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fixed mod ", None))
        self.lineEdit_unlocalized_mod_file_dir.setText(QCoreApplication.translate("MainWindow", u"unlocalized_mod_file_dir", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Unlocalized mod", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Deconv mass", None))
        self.lineEdit_deconv_mass_file_dir.setText(QCoreApplication.translate("MainWindow", u"deconv_mass_file_dir", None))
        self.lineEdit_r_env_dir.setText(QCoreApplication.translate("MainWindow", u"r_env_dir", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"R env dir", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Terminal mass error(ppm)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Peak match error(ppm)", None))
        self.checkBox_mass_calibration.setText(QCoreApplication.translate("MainWindow", u"Mass Calibration", None))
        self.checkBox_ms_calibration.setText(QCoreApplication.translate("MainWindow", u"MS Calibration", None))
        self.pushButton_save_param.setText(QCoreApplication.translate("MainWindow", u"Save param", None))
        self.pushButton_run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.pushButton_abort.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.textBrowser_process_info.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'SimSun'; font-size:9pt;\">Process info....</span></p></body></html>", None))
        self.pushButton_clear_process_info.setText(QCoreApplication.translate("MainWindow", u"Clear process info ", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"N-Terminal Frag Type:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Internal Frag Type", None))
        self.checkBox_a_ion_type.setText(QCoreApplication.translate("MainWindow", u"a", None))
        self.checkBox_a_add_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"a+1", None))
        self.checkBox_b_ion_type.setText(QCoreApplication.translate("MainWindow", u"b", None))
        self.checkBox_a_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"a-1", None))
        self.checkBox_x_ion_type.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.checkBox_x_add_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"x+1", None))
        self.checkBox_c_ion_type.setText(QCoreApplication.translate("MainWindow", u"c", None))
        self.checkBox_c_dot_ion_type.setText(QCoreApplication.translate("MainWindow", u"c.", None))
        self.checkBox_z_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"z-1", None))
        self.checkBox_z_add_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"z+1", None))
        self.checkBox_z_ion_type.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.checkBox_x_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"x-1", None))
        self.checkBox_y_ion_type.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.checkBox_y_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"y-1", None))
        self.checkBox_bz_add_H2_ion_type.setText(QCoreApplication.translate("MainWindow", u"bz+2", None))
        self.checkBox_by_ion_type.setText(QCoreApplication.translate("MainWindow", u"by", None))
        self.checkBox_bx_ion_type.setText(QCoreApplication.translate("MainWindow", u"bx", None))
        self.checkBox_ax_ion_type.setText(QCoreApplication.translate("MainWindow", u"ax", None))
        self.checkBox_ay_ion_type.setText(QCoreApplication.translate("MainWindow", u"ay", None))
        self.checkBox_az_add_H2_ion_type.setText(QCoreApplication.translate("MainWindow", u"az+2", None))
        self.checkBox_cx_ion_type.setText(QCoreApplication.translate("MainWindow", u"cx", None))
        self.checkBox_cz_ion_type.setText(QCoreApplication.translate("MainWindow", u"cz", None))
        self.checkBox_cy_ion_type.setText(QCoreApplication.translate("MainWindow", u"cy", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Internal mass error(ppm)", None))
        self.radioButton_M_mode.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.radioButton_M_add_H_mode.setText(QCoreApplication.translate("MainWindow", u"MH+", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Mass Mode", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"C-Terminal Frag Type:", None))
        self.lineEdit_workplace_dir.setText(QCoreApplication.translate("MainWindow", u"workplace_dir", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Workplace dir", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"mzML dir", None))
        self.lineEdit_mzml_file_dir.setText(QCoreApplication.translate("MainWindow", u"mzml_file_dir", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Scan id", None))
        self.checkBox_y_sub_H2_ion_type.setText(QCoreApplication.translate("MainWindow", u"y-2", None))
    # retranslateUi


# In[5]:


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1001, 819)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_load_param = QPushButton(self.centralwidget)
        self.pushButton_load_param.setObjectName(u"pushButton_load_param")
        self.pushButton_load_param.setGeometry(QRect(120, 30, 86, 25))
        self.lineEdit_param_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_param_file_dir.setObjectName(u"lineEdit_param_file_dir")
        self.lineEdit_param_file_dir.setGeometry(QRect(310, 30, 271, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 90, 66, 17))
        self.label.setAlignment(Qt.AlignCenter)
        self.lineEdit_seq = QLineEdit(self.centralwidget)
        self.lineEdit_seq.setObjectName(u"lineEdit_seq")
        self.lineEdit_seq.setGeometry(QRect(310, 80, 271, 31))
        self.lineEdit_fixed_mod_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_fixed_mod_file_dir.setObjectName(u"lineEdit_fixed_mod_file_dir")
        self.lineEdit_fixed_mod_file_dir.setGeometry(QRect(310, 180, 271, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 190, 72, 17))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_unlocalized_mod_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_unlocalized_mod_file_dir.setObjectName(u"lineEdit_unlocalized_mod_file_dir")
        self.lineEdit_unlocalized_mod_file_dir.setGeometry(QRect(310, 230, 271, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 240, 108, 17))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(120, 140, 91, 17))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.lineEdit_deconv_mass_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_deconv_mass_file_dir.setObjectName(u"lineEdit_deconv_mass_file_dir")
        self.lineEdit_deconv_mass_file_dir.setGeometry(QRect(310, 130, 271, 31))
        self.lineEdit_r_env_dir = QLineEdit(self.centralwidget)
        self.lineEdit_r_env_dir.setObjectName(u"lineEdit_r_env_dir")
        self.lineEdit_r_env_dir.setGeometry(QRect(310, 280, 271, 31))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(120, 290, 58, 17))
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(640, 220, 191, 31))
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(640, 370, 191, 31))
        self.label_11.setAlignment(Qt.AlignCenter)
        self.spinBox_terminal_mass_error = QSpinBox(self.centralwidget)
        self.spinBox_terminal_mass_error.setObjectName(u"spinBox_terminal_mass_error")
        self.spinBox_terminal_mass_error.setGeometry(QRect(850, 220, 41, 31))
        self.spinBox_peak_match_error = QSpinBox(self.centralwidget)
        self.spinBox_peak_match_error.setObjectName(u"spinBox_peak_match_error")
        self.spinBox_peak_match_error.setGeometry(QRect(850, 370, 41, 31))
        self.checkBox_mass_calibration = QCheckBox(self.centralwidget)
        self.checkBox_mass_calibration.setObjectName(u"checkBox_mass_calibration")
        self.checkBox_mass_calibration.setGeometry(QRect(650, 34, 171, 31))
        self.checkBox_mass_calibration.setChecked(False)
        self.checkBox_ms_calibration = QCheckBox(self.centralwidget)
        self.checkBox_ms_calibration.setObjectName(u"checkBox_ms_calibration")
        self.checkBox_ms_calibration.setGeometry(QRect(650, 74, 171, 31))
        self.pushButton_save_param = QPushButton(self.centralwidget)
        self.pushButton_save_param.setObjectName(u"pushButton_save_param")
        self.pushButton_save_param.setGeometry(QRect(650, 580, 111, 31))
        self.pushButton_run = QPushButton(self.centralwidget)
        self.pushButton_run.setObjectName(u"pushButton_run")
        self.pushButton_run.setGeometry(QRect(650, 620, 111, 31))
        self.pushButton_abort = QPushButton(self.centralwidget)
        self.pushButton_abort.setObjectName(u"pushButton_abort")
        self.pushButton_abort.setGeometry(QRect(650, 660, 111, 31))
        self.textBrowser_process_info = QTextBrowser(self.centralwidget)
        self.textBrowser_process_info.setObjectName(u"textBrowser_process_info")
        self.textBrowser_process_info.setGeometry(QRect(160, 550, 421, 151))
        self.textBrowser_process_info.setReadOnly(True)
        self.pushButton_clear_process_info = QPushButton(self.centralwidget)
        self.pushButton_clear_process_info.setObjectName(u"pushButton_clear_process_info")
        self.pushButton_clear_process_info.setGeometry(QRect(200, 710, 201, 31))
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(120, 420, 161, 31))
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(120, 500, 161, 31))
        self.checkBox_a_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_a_ion_type.setObjectName(u"checkBox_a_ion_type")
        self.checkBox_a_ion_type.setGeometry(QRect(310, 430, 31, 16))
        self.checkBox_a_add_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_a_add_H_ion_type.setObjectName(u"checkBox_a_add_H_ion_type")
        self.checkBox_a_add_H_ion_type.setGeometry(QRect(370, 430, 41, 16))
        self.checkBox_b_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_b_ion_type.setObjectName(u"checkBox_b_ion_type")
        self.checkBox_b_ion_type.setGeometry(QRect(490, 430, 31, 16))
        self.checkBox_a_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_a_sub_H_ion_type.setObjectName(u"checkBox_a_sub_H_ion_type")
        self.checkBox_a_sub_H_ion_type.setGeometry(QRect(430, 430, 41, 16))
        self.checkBox_x_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_x_ion_type.setObjectName(u"checkBox_x_ion_type")
        self.checkBox_x_ion_type.setGeometry(QRect(310, 470, 31, 16))
        self.checkBox_x_add_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_x_add_H_ion_type.setObjectName(u"checkBox_x_add_H_ion_type")
        self.checkBox_x_add_H_ion_type.setGeometry(QRect(370, 470, 41, 16))
        self.checkBox_c_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_c_ion_type.setObjectName(u"checkBox_c_ion_type")
        self.checkBox_c_ion_type.setGeometry(QRect(550, 430, 31, 16))
        self.checkBox_c_dot_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_c_dot_ion_type.setObjectName(u"checkBox_c_dot_ion_type")
        self.checkBox_c_dot_ion_type.setGeometry(QRect(610, 430, 31, 16))
        self.checkBox_z_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_z_sub_H_ion_type.setObjectName(u"checkBox_z_sub_H_ion_type")
        self.checkBox_z_sub_H_ion_type.setGeometry(QRect(790, 470, 41, 16))
        self.checkBox_z_add_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_z_add_H_ion_type.setObjectName(u"checkBox_z_add_H_ion_type")
        self.checkBox_z_add_H_ion_type.setGeometry(QRect(730, 470, 41, 16))
        self.checkBox_z_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_z_ion_type.setObjectName(u"checkBox_z_ion_type")
        self.checkBox_z_ion_type.setGeometry(QRect(670, 470, 31, 16))
        self.checkBox_x_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_x_sub_H_ion_type.setObjectName(u"checkBox_x_sub_H_ion_type")
        self.checkBox_x_sub_H_ion_type.setGeometry(QRect(430, 470, 41, 16))
        self.checkBox_y_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_y_ion_type.setObjectName(u"checkBox_y_ion_type")
        self.checkBox_y_ion_type.setGeometry(QRect(490, 470, 31, 16))
        self.checkBox_y_sub_H_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_y_sub_H_ion_type.setObjectName(u"checkBox_y_sub_H_ion_type")
        self.checkBox_y_sub_H_ion_type.setGeometry(QRect(550, 470, 41, 16))
        self.checkBox_bz_add_H2_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_bz_add_H2_ion_type.setObjectName(u"checkBox_bz_add_H2_ion_type")
        self.checkBox_bz_add_H2_ion_type.setGeometry(QRect(610, 510, 51, 16))
        self.checkBox_by_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_by_ion_type.setObjectName(u"checkBox_by_ion_type")
        self.checkBox_by_ion_type.setGeometry(QRect(550, 510, 41, 16))
        self.checkBox_bx_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_bx_ion_type.setObjectName(u"checkBox_bx_ion_type")
        self.checkBox_bx_ion_type.setGeometry(QRect(490, 510, 41, 16))
        self.checkBox_ax_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_ax_ion_type.setObjectName(u"checkBox_ax_ion_type")
        self.checkBox_ax_ion_type.setGeometry(QRect(310, 510, 41, 16))
        self.checkBox_ay_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_ay_ion_type.setObjectName(u"checkBox_ay_ion_type")
        self.checkBox_ay_ion_type.setGeometry(QRect(370, 510, 41, 16))
        self.checkBox_az_add_H2_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_az_add_H2_ion_type.setObjectName(u"checkBox_az_add_H2_ion_type")
        self.checkBox_az_add_H2_ion_type.setGeometry(QRect(430, 510, 51, 16))
        self.checkBox_cx_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_cx_ion_type.setObjectName(u"checkBox_cx_ion_type")
        self.checkBox_cx_ion_type.setGeometry(QRect(670, 510, 41, 16))
        self.checkBox_cz_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_cz_ion_type.setObjectName(u"checkBox_cz_ion_type")
        self.checkBox_cz_ion_type.setGeometry(QRect(790, 510, 41, 16))
        self.checkBox_cy_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_cy_ion_type.setObjectName(u"checkBox_cy_ion_type")
        self.checkBox_cy_ion_type.setGeometry(QRect(730, 510, 41, 16))
        self.spinBox_internal_mass_error = QSpinBox(self.centralwidget)
        self.spinBox_internal_mass_error.setObjectName(u"spinBox_internal_mass_error")
        self.spinBox_internal_mass_error.setGeometry(QRect(850, 271, 41, 31))
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(640, 270, 191, 31))
        self.label_13.setAlignment(Qt.AlignCenter)
        self.radioButton_M_mode = QRadioButton(self.centralwidget)
        self.radioButton_M_mode.setObjectName(u"radioButton_M_mode")
        self.radioButton_M_mode.setGeometry(QRect(650, 144, 89, 16))
        self.radioButton_M_add_H_mode = QRadioButton(self.centralwidget)
        self.radioButton_M_add_H_mode.setObjectName(u"radioButton_M_add_H_mode")
        self.radioButton_M_add_H_mode.setGeometry(QRect(650, 174, 71, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(650, 120, 81, 20))
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(120, 460, 161, 31))
        self.lineEdit_workplace_dir = QLineEdit(self.centralwidget)
        self.lineEdit_workplace_dir.setObjectName(u"lineEdit_workplace_dir")
        self.lineEdit_workplace_dir.setGeometry(QRect(310, 380, 271, 31))
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(120, 390, 90, 17))
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(120, 340, 61, 16))
        self.label_15.setAlignment(Qt.AlignCenter)
        self.lineEdit_mzml_file_dir = QLineEdit(self.centralwidget)
        self.lineEdit_mzml_file_dir.setObjectName(u"lineEdit_mzml_file_dir")
        self.lineEdit_mzml_file_dir.setGeometry(QRect(310, 330, 271, 31))
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(640, 320, 191, 31))
        self.label_16.setAlignment(Qt.AlignCenter)
        self.spinBox_scan_id = QSpinBox(self.centralwidget)
        self.spinBox_scan_id.setObjectName(u"spinBox_scan_id")
        self.spinBox_scan_id.setGeometry(QRect(850, 321, 41, 31))
        self.checkBox_y_sub_H2_ion_type = QCheckBox(self.centralwidget)
        self.checkBox_y_sub_H2_ion_type.setObjectName(u"checkBox_y_sub_H2_ion_type")
        self.checkBox_y_sub_H2_ion_type.setGeometry(QRect(610, 470, 41, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1001, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_load_param, self.lineEdit_param_file_dir)
        QWidget.setTabOrder(self.lineEdit_param_file_dir, self.lineEdit_seq)
        QWidget.setTabOrder(self.lineEdit_seq, self.lineEdit_fixed_mod_file_dir)
        QWidget.setTabOrder(self.lineEdit_fixed_mod_file_dir, self.lineEdit_unlocalized_mod_file_dir)
        QWidget.setTabOrder(self.lineEdit_unlocalized_mod_file_dir, self.lineEdit_deconv_mass_file_dir)
        QWidget.setTabOrder(self.lineEdit_deconv_mass_file_dir, self.lineEdit_r_env_dir)
        QWidget.setTabOrder(self.lineEdit_r_env_dir, self.checkBox_mass_calibration)
        QWidget.setTabOrder(self.checkBox_mass_calibration, self.checkBox_ms_calibration)
        QWidget.setTabOrder(self.checkBox_ms_calibration, self.spinBox_terminal_mass_error)
        QWidget.setTabOrder(self.spinBox_terminal_mass_error, self.spinBox_peak_match_error)

        self.retranslateUi(MainWindow)
        self.pushButton_load_param.clicked.connect(MainWindow.load_param)
        self.pushButton_save_param.clicked.connect(MainWindow.save_param)
        self.pushButton_run.clicked.connect(MainWindow.run)
        self.pushButton_abort.clicked.connect(MainWindow.abort)
        self.pushButton_clear_process_info.clicked.connect(self.textBrowser_process_info.clear)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Panda-UV-2.0", None))
        self.pushButton_load_param.setText(QCoreApplication.translate("MainWindow", u"Load param", None))
        self.lineEdit_param_file_dir.setText(QCoreApplication.translate("MainWindow", u"param_file_dir", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sequence", None))
        self.lineEdit_seq.setText(QCoreApplication.translate("MainWindow", u"seq", None))
        self.lineEdit_fixed_mod_file_dir.setText(QCoreApplication.translate("MainWindow", u"fixed_mod_file_dir", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fixed mod ", None))
        self.lineEdit_unlocalized_mod_file_dir.setText(QCoreApplication.translate("MainWindow", u"unlocalized_mod_file_dir", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Unlocalized mod", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Deconv mass", None))
        self.lineEdit_deconv_mass_file_dir.setText(QCoreApplication.translate("MainWindow", u"deconv_mass_file_dir", None))
        self.lineEdit_r_env_dir.setText(QCoreApplication.translate("MainWindow", u"r_env_dir", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"R env dir", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Terminal mass error(ppm)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Peak match error(ppm)", None))
        self.checkBox_mass_calibration.setText(QCoreApplication.translate("MainWindow", u"Mass Calibration", None))
        self.checkBox_ms_calibration.setText(QCoreApplication.translate("MainWindow", u"MS Calibration", None))
        self.pushButton_save_param.setText(QCoreApplication.translate("MainWindow", u"Save param", None))
        self.pushButton_run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.pushButton_abort.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.textBrowser_process_info.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'SimSun'; font-size:9pt;\">Process info....</span></p></body></html>", None))
        self.pushButton_clear_process_info.setText(QCoreApplication.translate("MainWindow", u"Clear process info ", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"N-Terminal Frag Type:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Internal Frag Type", None))
        self.checkBox_a_ion_type.setText(QCoreApplication.translate("MainWindow", u"a", None))
        self.checkBox_a_add_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"a+1", None))
        self.checkBox_b_ion_type.setText(QCoreApplication.translate("MainWindow", u"b", None))
        self.checkBox_a_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"a-1", None))
        self.checkBox_x_ion_type.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.checkBox_x_add_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"x+1", None))
        self.checkBox_c_ion_type.setText(QCoreApplication.translate("MainWindow", u"c", None))
        self.checkBox_c_dot_ion_type.setText(QCoreApplication.translate("MainWindow", u"c.", None))
        self.checkBox_z_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"z-1", None))
        self.checkBox_z_add_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"z+1", None))
        self.checkBox_z_ion_type.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.checkBox_x_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"x-1", None))
        self.checkBox_y_ion_type.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.checkBox_y_sub_H_ion_type.setText(QCoreApplication.translate("MainWindow", u"y-1", None))
        self.checkBox_bz_add_H2_ion_type.setText(QCoreApplication.translate("MainWindow", u"bz", None))
        self.checkBox_by_ion_type.setText(QCoreApplication.translate("MainWindow", u"by", None))
        self.checkBox_bx_ion_type.setText(QCoreApplication.translate("MainWindow", u"bx", None))
        self.checkBox_ax_ion_type.setText(QCoreApplication.translate("MainWindow", u"ax", None))
        self.checkBox_ay_ion_type.setText(QCoreApplication.translate("MainWindow", u"ay", None))
        self.checkBox_az_add_H2_ion_type.setText(QCoreApplication.translate("MainWindow", u"az", None))
        self.checkBox_cx_ion_type.setText(QCoreApplication.translate("MainWindow", u"cx", None))
        self.checkBox_cz_ion_type.setText(QCoreApplication.translate("MainWindow", u"cz", None))
        self.checkBox_cy_ion_type.setText(QCoreApplication.translate("MainWindow", u"cy", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Internal mass error(ppm)", None))
        self.radioButton_M_mode.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.radioButton_M_add_H_mode.setText(QCoreApplication.translate("MainWindow", u"MH+", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Mass Mode", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"C-Terminal Frag Type:", None))
        self.lineEdit_workplace_dir.setText(QCoreApplication.translate("MainWindow", u"workplace_dir", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Workplace dir", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"mzML dir", None))
        self.lineEdit_mzml_file_dir.setText(QCoreApplication.translate("MainWindow", u"mzml_file_dir", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Scan id", None))
        self.checkBox_y_sub_H2_ion_type.setText(QCoreApplication.translate("MainWindow", u"y-2", None))
    # retranslateUi


# In[6]:


class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        #初始化界面
        self.setupUi(self)
        #设置图标
        self.setWindowIcon(QIcon(r'C:\Users\zhu\Desktop\Panda-UV初稿及图表\AI绘图汇总\Icon.png'))
        #初始化param
        self.param = paramClass()
        #实例一直保存，方便查看运行状态
        self.main_run = PANDA_UV_main()
        self.main_run.process_info.connect(self.showProcessInfo)
        #输出重定向到UI
        sys.stdout = self.main_run
        
    #选择参数文件并加载到界面，初始化参数类
    def load_param(self):
        filename,filetype_str = QFileDialog.getOpenFileName()
        self.lineEdit_param_file_dir.setText(filename)
        print(f"Open file:{filename}")
        #读取配置文件并更新param
        self.param.read_param(filename)
        self.refresh_param()
    
    #加载配置参数到界面
    def refresh_param(self,param_dict=None):
        if param_dict is None:
            param_dict = self.param.param_dict
        else:
            pass
        
        self.lineEdit_seq.setText(param_dict["sequence"])
        self.lineEdit_deconv_mass_file_dir.setText(param_dict["deconv_mass_file_dir"])
        self.lineEdit_fixed_mod_file_dir.setText(param_dict["fixed_mod_file_dir"])
        self.lineEdit_unlocalized_mod_file_dir.setText(param_dict["unlocalized_mod_file_dir"])
        self.lineEdit_r_env_dir.setText(param_dict["r_env_dir"])
        self.lineEdit_mzml_file_dir.setText(param_dict["mzml_file_dir"])
        self.lineEdit_workplace_dir.setText(param_dict["workplace_dir"])
        self.checkBox_mass_calibration.setChecked(param_dict["mass_calibration"])
        self.checkBox_ms_calibration.setChecked(param_dict["ms_calibration"])
        mass_mode = param_dict["mass_mode"]
        if mass_mode == 'M':
            self.radioButton_M_mode.setChecked(True)
        else:
            self.radioButton_M_add_H_mode.setChecked(True)
        self.spinBox_terminal_mass_error.setValue(param_dict["terminal_mass_error"])
        self.spinBox_internal_mass_error.setValue(param_dict["internal_mass_error"])
        self.spinBox_scan_id.setValue(param_dict["scan_id"])
        self.spinBox_peak_match_error.setValue(param_dict["peak_match_error"])
        
        valid_n_terminal_ion_type_list = ["a","a+1","a-1","b","c","c."]
        valid_c_terminal_ion_type_list = ["x","x+1","x-1","y","y-1","y-2","z","z+1","z-1"]
        valid_internal_ion_type_list = ["ax","ay","az+2","bx","by","bz+2","cx","cy","cz"]
        valid_ion_type_list = valid_n_terminal_ion_type_list+valid_c_terminal_ion_type_list+valid_internal_ion_type_list
        n_terminal_frag_type = param_dict["n_terminal_frag_type"]
        for n_ion_type in n_terminal_frag_type:
            if n_ion_type=="a":
                self.checkBox_a_ion_type.setChecked(True)
            elif n_ion_type=="a+1":
                self.checkBox_a_add_H_ion_type.setChecked(True)
            elif n_ion_type=="a-1":
                self.checkBox_a_sub_H_ion_type.setChecked(True)
            elif n_ion_type=="b":
                self.checkBox_b_ion_type.setChecked(True)
            elif n_ion_type=="c":
                self.checkBox_c_ion_type.setChecked(True)
            elif n_ion_type=="c.":
                self.checkBox_c_dot_ion_type.setChecked(True)
            else:
                pass
        c_terminal_frag_type = param_dict["c_terminal_frag_type"]
        for c_ion_type in c_terminal_frag_type:
            if c_ion_type=="x":
                self.checkBox_x_ion_type.setChecked(True)
            elif c_ion_type=="x+1":
                self.checkBox_x_add_H_ion_type.setChecked(True)
            elif c_ion_type=="x-1":
                self.checkBox_x_sub_H_ion_type.setChecked(True)
            elif c_ion_type=="y":
                self.checkBox_y_ion_type.setChecked(True)
            elif c_ion_type=="y-1":
                self.checkBox_y_sub_H_ion_type.setChecked(True)
            elif c_ion_type=="y-2":
                self.checkBox_y_sub_H2_ion_type.setChecked(True)
            elif c_ion_type=="z":
                self.checkBox_z_ion_type.setChecked(True)
            elif c_ion_type=="z+1":
                self.checkBox_z_add_H_ion_type.setChecked(True)
            elif c_ion_type=="z-1":
                self.checkBox_z_sub_H_ion_type.setChecked(True)
            else:
                pass
        internal_frag_type_list = param_dict["internal_frag_type"]
        for internal_frag_type in internal_frag_type_list:
            if internal_frag_type=="ax":
                self.checkBox_ax_ion_type.setChecked(True)
            elif internal_frag_type=="ay":
                self.checkBox_ay_ion_type.setChecked(True)
            elif internal_frag_type=="az+2":
                self.checkBox_az_add_H2_ion_type.setChecked(True)
            elif internal_frag_type=="bx":
                self.checkBox_bx_ion_type.setChecked(True)
            elif internal_frag_type=="by":
                self.checkBox_by_ion_type.setChecked(True)
            elif internal_frag_type=="bz+2":
                self.checkBox_bz_add_H2_ion_type.setChecked(True)
            elif internal_frag_type=="cx":
                self.checkBox_cx_ion_type.setChecked(True)
            elif internal_frag_type=="cy":
                self.checkBox_cy_ion_type.setChecked(True)
            elif internal_frag_type=="cz":
                self.checkBox_cz_ion_type.setChecked(True)
            else:
                pass
            
    #保存界面输入的参数到param类
    def save_param(self):
        param_dict = self.param.param_dict
        
        param_dict["sequence"] = self.lineEdit_seq.text()
        param_dict["deconv_mass_file_dir"] = self.lineEdit_deconv_mass_file_dir.text()
        param_dict["fixed_mod_file_dir"] = self.lineEdit_fixed_mod_file_dir.text()
        param_dict["unlocalized_mod_file_dir"] = self.lineEdit_unlocalized_mod_file_dir.text()
        param_dict["r_env_dir"] = self.lineEdit_r_env_dir.text()
        param_dict["mzml_file_dir"] = self.lineEdit_mzml_file_dir.text()
        param_dict["workplace_dir"] = self.lineEdit_workplace_dir.text()
        param_dict["mass_calibration"] = self.checkBox_mass_calibration.isChecked()
        param_dict["ms_calibration"] = self.checkBox_ms_calibration.isChecked()
        if self.radioButton_M_mode.isChecked():
            param_dict["mass_mode"] = 'M'
        else:
            param_dict["mass_mode"] = 'MH+'
        param_dict["terminal_mass_error"] = self.spinBox_terminal_mass_error.value()
        param_dict["internal_mass_error"] = self.spinBox_internal_mass_error.value()
        param_dict["scan_id"] = self.spinBox_scan_id.value()
        param_dict["peak_match_error"] = self.spinBox_peak_match_error.value()
        
        n_terminal_ion_type_list = []
        c_terminal_ion_type_list = []
        internal_ion_type_list = []
        if self.checkBox_a_ion_type.isChecked():
            n_terminal_ion_type_list.append("a")
        if self.checkBox_a_add_H_ion_type.isChecked():
            n_terminal_ion_type_list.append("a+1")
        if self.checkBox_a_sub_H_ion_type.isChecked():
            n_terminal_ion_type_list.append("a-1")
        if self.checkBox_b_ion_type.isChecked():
            n_terminal_ion_type_list.append("b")
        if self.checkBox_c_ion_type.isChecked():
            n_terminal_ion_type_list.append("c")
        if self.checkBox_c_dot_ion_type.isChecked():
            n_terminal_ion_type_list.append("c.")
        param_dict["n_terminal_frag_type"] = n_terminal_ion_type_list
        
        if self.checkBox_x_ion_type.isChecked():
            c_terminal_ion_type_list.append("x")
        if self.checkBox_x_add_H_ion_type.isChecked():
            c_terminal_ion_type_list.append("x+1")
        if self.checkBox_x_sub_H_ion_type.isChecked():
            c_terminal_ion_type_list.append("x-1")
        if self.checkBox_y_ion_type.isChecked():
            c_terminal_ion_type_list.append("y")
        if self.checkBox_y_sub_H_ion_type.isChecked():
            c_terminal_ion_type_list.append("y-1")
        if self.checkBox_y_sub_H2_ion_type.isChecked():
            c_terminal_ion_type_list.append("y-2")
        if self.checkBox_z_ion_type.isChecked():
            c_terminal_ion_type_list.append("z")
        if self.checkBox_z_add_H_ion_type.isChecked():
            c_terminal_ion_type_list.append("z+1")
        if self.checkBox_z_sub_H_ion_type.isChecked():
            c_terminal_ion_type_list.append("z-1")
        param_dict["c_terminal_frag_type"] = c_terminal_ion_type_list
        
        if self.checkBox_ax_ion_type.isChecked():
            internal_ion_type_list.append("ax")
        if self.checkBox_ay_ion_type.isChecked():
            internal_ion_type_list.append("ay")
        if self.checkBox_az_add_H2_ion_type.isChecked():
            internal_ion_type_list.append("az+2")
        if self.checkBox_bx_ion_type.isChecked():
            internal_ion_type_list.append("bx")
        if self.checkBox_by_ion_type.isChecked():
            internal_ion_type_list.append("by")
        if self.checkBox_bz_add_H2_ion_type.isChecked():
            internal_ion_type_list.append("bz+2")
        if self.checkBox_cx_ion_type.isChecked():
            internal_ion_type_list.append("cx")
        if self.checkBox_cy_ion_type.isChecked():
            internal_ion_type_list.append("cy")
        if self.checkBox_cz_ion_type.isChecked():
            internal_ion_type_list.append("cz")
        param_dict["internal_frag_type"] = internal_ion_type_list
        
        self.param.param_dict = param_dict
        self.param.save_param()
        print("已保存参数文件")
        
    def run(self):
        #保存界面参数到参数文件
        self.save_param()
        #从参数文件读入参数并更新参数
        self.param.read_param()
        self.offRunButton()
        #防止程序异常导致按键被锁住
        #添加self保存延长线程的周期，否则会被强制退出。
        #self.main_run = PANDA_UV_main()
        #必须设置堆栈数量，否则重新运行将会失败
        
        #print(self.main_run.stackSize())
        self.main_run.param = self.param.param_dict
        #self.main_run.process_info.connect(self.showProcessInfo)
        
        #sys.stdout = self
        #main(self.param.param_dict)
        #这里开启了一个新进程，主进程会继续执行下去
        self.main_run.start()
        self.main_run.finished.connect(self.onRunButton)
        self.main_run.exit()
    def abort(self):
        pass
    
    #关闭除了Abort之外的按键
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
        #print(self.main_run.stackSize())
    def showProcessInfo(self,text):
        self.textBrowser_process_info.append(text)
    #写write函数，将输出传递到信息框
    def write(self,text):
        self.showProcessInfo(text)
        QApplication.processEvents()


# In[7]:


#一个继承子QThread的类，线程开始时运行PANDA-UV主函数
class PANDA_UV_main(QThread):
    process_info = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        #实例化时就设置堆栈数量
        self.setStackSize(4294967295)
        
    def write(self,text):
        self.process_info.emit(text)
    
    #def __del__(self):
    #    self.wait()
    
    #参数属性在实例化之后添加
    def run(self):
        main(self.param)


# In[8]:


#读写参数的PANDA-UV参数的类
class paramClass:
    def __init__(self):
        #保存参数的路径
        self.dir = "."
        #保存参数的文件名字
        self.filename = "PANDA-UV_param.yaml"
        self.param_output_dir = self.dir+"/"+self.filename
        self.param_dict = self.get_param_template()
        
    #生成一个空白的PANDA-UV配置文件
    def get_param_template(self):
        param_dict = {"sequence":'',"deconv_mass_file_dir":'',"fixed_mod_file_dir":'',"unlocalized_mod_file_dir":'',"r_env_dir":'',
                      "mass_calibration":True,"ms_calibration":True,"mass_mode":'',"terminal_mass_error":10,
                      "internal_mass_error":10,"peak_match_error":10,"n_terminal_frag_type":[],"c_terminal_frag_type":[],
                      "internal_frag_type":[],"workplace_dir":'',"mzml_file_dir":''}
        return param_dict
    
    #输入python数据结构对象，保存到当前目录的默认参数文件夹中
    def save_param(self,param_dict=None,param_output_dir=None):
        #如果没有输入参数，则默认保存模板
        if param_dict is None:
            param_dict = self.param_dict
        else:
            pass
        
        if param_output_dir is None:
            param_output_dir = self.param_output_dir
        else:
            pass
        
        with open(self.param_output_dir,encoding="utf-8",mode="w") as f:
            yaml.dump(param_dict,f)
    
    def read_param(self,param_input_dir=None):
        #没有输入路径时默认读取模板
        if param_input_dir is None:
            param_input_dir = self.param_output_dir
        else:
            pass
        
        with open(param_input_dir,mode="r",encoding="utf-8") as f:
            yamlConf = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.param_dict = yamlConf
        #return yamlConf
    
    #设置param_dict属性
    def set_param(self,param_dict):
        self.param_dict = param_dict


# In[ ]:


if __name__ == "__main__":
    app =  QApplication([])
    win = MyMainWindow()
    win.show()
    app.exec()


# In[ ]:




