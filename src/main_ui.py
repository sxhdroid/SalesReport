# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\apple\PycharmProjects\SalesReport\main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 71, 21))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.plateform = QtWidgets.QComboBox(self.centralwidget)
        self.plateform.setGeometry(QtCore.QRect(100, 40, 91, 22))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.plateform.setFont(font)
        self.plateform.setObjectName("plateform")
        self.plateform.addItem("")
        self.plateform.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 71, 21))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.custome_mask = QtWidgets.QLineEdit(self.centralwidget)
        self.custome_mask.setGeometry(QtCore.QRect(290, 40, 113, 20))
        self.custome_mask.setMaxLength(20)
        self.custome_mask.setObjectName("custome_mask")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(20, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.start.setFont(font)
        self.start.setObjectName("start")
        self.log_out = QtWidgets.QTextBrowser(self.centralwidget)
        self.log_out.setGeometry(QtCore.QRect(20, 190, 591, 221))
        self.log_out.setObjectName("log_out")
        self.month = QtWidgets.QComboBox(self.centralwidget)
        self.month.setGeometry(QtCore.QRect(520, 40, 91, 22))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.month.setFont(font)
        self.month.setObjectName("month")
        self.month.addItem("")
        self.month.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 40, 71, 21))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.cancel = QtWidgets.QPushButton(self.centralwidget)
        self.cancel.setGeometry(QtCore.QRect(130, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.groups = QtWidgets.QComboBox(self.centralwidget)
        self.groups.setGeometry(QtCore.QRect(290, 40, 131, 22))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.groups.setFont(font)
        self.groups.setObjectName("groups")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "业绩导出工具"))
        self.label.setText(_translate("MainWindow", "导出平台："))
        self.plateform.setItemText(0, _translate("MainWindow", "阿里分销"))
        self.plateform.setItemText(1, _translate("MainWindow", "优海淘"))
        self.label_2.setText(_translate("MainWindow", "客户标签："))
        self.start.setText(_translate("MainWindow", "开始"))
        self.month.setItemText(0, _translate("MainWindow", "上月"))
        self.month.setItemText(1, _translate("MainWindow", "本月"))
        self.label_3.setText(_translate("MainWindow", "导出月份："))
        self.cancel.setText(_translate("MainWindow", "取消"))
