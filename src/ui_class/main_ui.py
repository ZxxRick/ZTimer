"""
创建时间     : 2022/5/28 12:21
作者   : Zxx
代码概述    :
"""
import datetime
import os
import time
import ctypes

from PyQt5 import QtCore, QtGui
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from src.ui_class.commit_ui import Commit_ui
from src.utils.dataIO import DataIO
from ui.main_ui import Ui_MainWindow


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # 设置液晶屏的刷新
        self.clock_qtimer = QTimer()
        self.clock_qtimer.timeout.connect(self.clock)

        # 计时的开始时间（time类型），以及总时长（int表示秒）
        self.strat_time = 0
        self.total_time = 0
        # 系统是否运行tag
        self.__time_run_tag = False
        # 获取程序运行路径
        self.__root_path = os.getcwd()
        self.__init_Style()
        self.pushButton_finish.setDisabled(True)

        self.dataIO = DataIO()

    def __init_Style(self):

        self.lcdNumber.display("0:00:00")
        # 设置任务栏图标
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.setWindowIcon(QIcon(self.__root_path + "/static/icons/ZTimer.png"))
        self.setStyleSheet(
            # "QPushButton{background:#FFFFFF;border-radius:5px;} "
            # "QPushButton{font-size:35px;font-family:'楷体'}"
            "QLCDNumber{border-radius:5px;}"
        )
        self.pushButton_start.setIcon(QIcon(self.__root_path + "/static/icons/start.png"))
        self.pushButton_finish.setIcon(QIcon(self.__root_path + "/static/icons/finish.png"))

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        开始按钮有两个功能：1是计时开始，2是计时暂停
        :return:
        """
        if self.__time_run_tag:
            self.clock_qtimer.stop()
            self.dataIO.system_pause()
            self.pushButton_start.setIcon(QIcon(self.__root_path + "/static/icons/start.png"))
            self.__time_run_tag = False
        else:
            if self.strat_time == 0:
                # 如果是第一次开始，则需要将开始时间刷新
                self.strat_time = time.time()
                self.dataIO.system_start(self.strat_time)
            # 计时器的函数设置为1秒钟刷新一次
            self.clock_qtimer.start(1000)
            self.dataIO.system_continue()
            self.pushButton_start.setIcon(QIcon(self.__root_path + "/static/icons/pause.png"))
            self.pushButton_finish.setDisabled(False)
            self.__time_run_tag = True

    @pyqtSlot()
    def on_pushButton_finish_clicked(self):
        """
        结束按钮点击
        :return:
        """
        print("on_pushButton_finish_clicked")
        self.clock_qtimer.stop()
        self.__time_run_tag = False
        self.pushButton_start.setIcon(QIcon(self.__root_path + "/static/icons/start.png"))
        self.__commit = Commit_ui(parent=self)
        # 绑定信号槽函数
        self.__commit.commot_text_signal.connect(self.get_commit_text)
        self.__commit.cancel_commit_signal.connect(self.get_cancel_button)

        self.__commit.show()

    def clock(self):
        """
        被QTimer绑定，每秒调用一次
        :return:
        """
        self.total_time += 1
        t = str(datetime.timedelta(seconds=self.total_time))
        self.lcdNumber.display(t)

    def closeEvent(self, event):
        """
        关闭界面触发的事件
        :param event:
        :return:
        """

        if self.total_time != 0:
            # 如果未结束计时则不退出
            QMessageBox.about(self, "提示", "请先提交计时再退出")
            event.ignore()
            # reply = QMessageBox.question(self, "提示", "是否保存并退出", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            # 确认按钮的返回值
            # if reply == 16384:

            # event.accept()
            # else:
            #     event.ignore()
        else:
            pass

    def get_commit_text(self, commit_text):
        """
        获取子界面的提交信息
        """
        self.dataIO.system_finish(total_time=self.total_time, logs_infor=commit_text)
        self.pushButton_finish.setDisabled(True)
        self.strat_time = 0
        self.total_time = 0

    def get_cancel_button(self, tag: bool):
        pass
        # self.dataIO.system_cancel_finish()

    def resizeEvent(self, e):

        pass
        # print(self.height())
        # if self.height() > self.width() * 2.5:
        #     self.setFixedHeight(self.width() * 1.6)
        #     self.setMinimumHeight(300)
        # if self.width() > self.height() * 1.1:
        #     self.setFixedHeight(self.width() * 1.1)
        #     self.setMinimumHeight(300)
        # self.lcdNumber.setFixedHeight(self.pushButton_finish.height()*1.5)
        # self.lcdNumber.setFixedHeight(self.height() / 4)
        # self.pushButton_start.setIconSize(self.pushButton_start.size())
        # self.pushButton_finish.setIconSize(self.pushButton_finish.size())
