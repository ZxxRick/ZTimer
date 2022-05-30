"""
创建时间     : 2022/5/28 12:18
作者   : Zxx
代码概述    :项目主函数
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

from src.ui_class.commit_ui import Commit_ui
from src.ui_class.main_ui import MainUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainUI()
    # myapp =Commit_ui()
    myapp.show()


    sys.exit(app.exec_())
