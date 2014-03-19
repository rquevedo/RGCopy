# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RCopy.ui'
#
# Created: Thu Aug 23 11:50:35 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(491, 146)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lbl_source_file = QtGui.QLabel(self.centralwidget)
        self.lbl_source_file.setGeometry(QtCore.QRect(10, 10, 381, 20))
        self.lbl_source_file.setObjectName(_fromUtf8("lbl_source_file"))
        self.lbl_always_ask = QtGui.QLabel(self.centralwidget)
        self.lbl_always_ask.setGeometry(QtCore.QRect(400, 10, 81, 17))
        self.lbl_always_ask.setObjectName(_fromUtf8("lbl_always_ask"))
        self.pb_single_file = QtGui.QProgressBar(self.centralwidget)
        self.pb_single_file.setGeometry(QtCore.QRect(10, 30, 471, 23))
        self.pb_single_file.setProperty("value", 24)
        self.pb_single_file.setObjectName(_fromUtf8("pb_single_file"))
        self.lbl_target_folder = QtGui.QLabel(self.centralwidget)
        self.lbl_target_folder.setGeometry(QtCore.QRect(10, 60, 281, 20))
        self.lbl_target_folder.setObjectName(_fromUtf8("lbl_target_folder"))
        self.lbl_close = QtGui.QLabel(self.centralwidget)
        self.lbl_close.setGeometry(QtCore.QRect(440, 60, 41, 17))
        self.lbl_close.setObjectName(_fromUtf8("lbl_close"))
        self.pb_total_copy = QtGui.QProgressBar(self.centralwidget)
        self.pb_total_copy.setGeometry(QtCore.QRect(10, 80, 471, 23))
        self.pb_total_copy.setProperty("value", 24)
        self.pb_total_copy.setObjectName(_fromUtf8("pb_total_copy"))
        self.btn_more = QtGui.QPushButton(self.centralwidget)
        self.btn_more.setGeometry(QtCore.QRect(10, 110, 91, 27))
        self.btn_more.setObjectName(_fromUtf8("btn_more"))
        self.btn_move_to = QtGui.QPushButton(self.centralwidget)
        self.btn_move_to.setGeometry(QtCore.QRect(180, 110, 98, 27))
        self.btn_move_to.setObjectName(_fromUtf8("btn_move_to"))
        self.btn_copy_to = QtGui.QPushButton(self.centralwidget)
        self.btn_copy_to.setGeometry(QtCore.QRect(280, 110, 98, 27))
        self.btn_copy_to.setObjectName(_fromUtf8("btn_copy_to"))
        self.btn_close = QtGui.QPushButton(self.centralwidget)
        self.btn_close.setGeometry(QtCore.QRect(380, 110, 98, 27))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "RCopy", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_source_file.setText(QtGui.QApplication.translate("MainWindow", "No Files", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_always_ask.setText(QtGui.QApplication.translate("MainWindow", "Always Ask", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_target_folder.setText(QtGui.QApplication.translate("MainWindow", "Select Target Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_more.setText(QtGui.QApplication.translate("MainWindow", "More", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_move_to.setText(QtGui.QApplication.translate("MainWindow", "Move To", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_copy_to.setText(QtGui.QApplication.translate("MainWindow", "Copy To", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))



