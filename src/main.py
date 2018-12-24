#!/usr/bin/env python
# coding=utf-8

"""
__title__ = 'main'
__author__ = 'apple'
__mtime__ = '2018/12/12'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from src.main_ui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from src.mmzl_proteams import build_achievement, get_team_groups
from threading import Thread
import sys


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    currentMonth = 0
    currentPlatform = 0
    group_info = None

    def __init__(self):
        super(App, self).__init__()
        self.isSetGroup = False
        self.setupUi(self)
        self.readSettings()
        self.start.clicked.connect(self.start_export)
        self.plateform.currentIndexChanged.connect(self.plateformChanged)
        self.month.currentIndexChanged.connect(self.monthChanged)
        self.cancel.clicked.connect(self.cancel_export)
        self.cancel.hide()
        self.groups.hide()
        self.log_out.setText("选择导出%s平台%s业绩" % (self.plateform.currentText(), self.month.currentText()))

    def readSettings(self):
        """
        读配置
        :return:
        """
        settings = QtCore.QSettings('./.sale.ini', QtCore.QSettings.IniFormat)
        settings.beginGroup("config")
        mark = settings.value("remark")
        settings.endGroup()
        self.custome_mask.setText(mark)

    def writeSettings(self):
        """
        写配置
        :return:
        """
        settings = QtCore.QSettings('./.sale.ini', QtCore.QSettings.IniFormat)
        # 将信息写入配置文件
        settings.beginGroup("config")
        settings.setValue("remark", self.custome_mask.text())
        settings.endGroup()

    def start_export(self):

        if self.currentPlatform == 0:
            remark = self.custome_mask.text()
            if len(remark) == 0:
                self.log_out.setText("请输入维护客户的标签！")
                return
            from src.alifenxiao_proteams import start
            # start(self.currentMonth, remark=remark, cb_log=self.show_log)
            t = Thread(target=start, args=(self.currentMonth, remark, self.show_log), daemon=True)
            t.start()
        else:
            remark = self.group_info[0]
            # build_achievement(self.currentMonth, cb_log=self.show_log, remark=remark)
            Thread(target=build_achievement, args=(self.currentMonth, self.show_log, remark), daemon=True).start()
        self.writeSettings()
        self.log_out.setText("开始导出%s平台%s业绩" % (self.plateform.currentText(), self.month.currentText()))

    def cancel_export(self):
        print('取消')

    def monthChanged(self, item):
        self.currentMonth = item
        self.log_out.setText("选择导出%s业绩" % self.month.currentText())

    def plateformChanged(self, item):
        self.currentPlatform = item
        self.log_out.append("选择导出%s平台业绩" % self.plateform.currentText())
        if item == 0:
            self.label_2.setText('客户标签：')
            self.groups.hide()  # 隐藏团队选择下拉框
            self.custome_mask.show()  # 显示客户标签输入框
        elif item == 1:
            self.label_2.setText('我的团队：')
            self.groups.show()  # 显示团队选择下拉框
            self.custome_mask.hide()  # 隐藏客户标签输入框
            if not self.isSetGroup:
                self.group_info = get_team_groups(self.show_log)
                if self.group_info is None or len(self.group_info) == 0:
                    self.plateform.setCurrentIndex(0)
                    return
                self.groups.addItem(self.group_info[1])
                self.isSetGroup = True

    def show_log(self, msg):
        self.log_out.append(msg)
        self.log_out.moveCursor(QtGui.QTextCursor.End)

    def closeEvent(self, *args, **kwargs):
        print('close')
        from src.alifenxiao_proteams import stop
        stop()
        from src.mmzl_proteams import stop_mmzl
        stop_mmzl()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())


