"""
创建时间     : 2022/5/29 12:03
作者   : Zxx
代码概述    :结束计时时需要输入当前的学习日志页面
"""
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox

from src.utils.dataIO import DataIO
from ui.commit_ui import Ui_commit


class Commit_ui(QDialog, Ui_commit):
    # 向父界面传递数据的信号槽
    commot_text_signal = QtCore.pyqtSignal(str)
    cancel_commit_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.__init_style()

    @pyqtSlot()
    def on_pushButton_commit_clicked(self):
        commit_text = self.textEdit_commit.toPlainText()
        if commit_text == "":
            QMessageBox.about(self, "提示", "提交日志写点啥（除非你摸鱼了）")
            return

        self.commot_text_signal.emit(commit_text)
        self.close()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.cancel_commit_signal.emit(False)
        self.close()

    def closeEvent(self, event):
        # self.NewProjectSignal.emit("close")

        pass

    def __init_style(self):
        # self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        self.setWindowModality(Qt.ApplicationModal)  # 设置其他界面不可点击
        self.setStyleSheet(
            "QPushButton{background:#FFFFFF;border-radius:5px;} "
            ""
        )

        self.textEdit_commit.setStyleSheet(
            "QTextEdit{border-radius: 26px}"
            "QTextEdit{font-size:20px;font-family:'楷体'}")
