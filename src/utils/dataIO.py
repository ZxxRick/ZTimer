"""
创建时间     : 2022/5/28 13:05
作者   : Zxx
代码概述    :用于数据的读取和时间的记录
"""
import os
import pandas


class DataIO:
    def __init__(self):
        self.__start_time = None
        self.__finish_time = None
        # 计时中断次数
        self.__interrupt_count = 0
        self.__dir_path = os.getcwd() + "\\data\\"
        self.__data_path = os.getcwd() + "\\data\\data_logs.csv"

        # 初始化的时候需要验证是否有数据记录文件存在
        # 此处的代码有待优化-------------------------------------------->
        if not os.path.exists(self.__dir_path):
            try:
                os.mkdir(self.__dir_path)
            except:
                pass
        if not os.path.exists(self.__data_path):
            try:
                with open(self.__data_path, "w", encoding="utf-8") as f:
                    f.write(",start_time,total_time,interrupt_count,logs_infor\n")
            except:
                pass

    def system_start(self, start_time):
        """
        当系统开始计时的时候被调用，记录开始时间
        :param start_time: time()类型的数据
        :return:
        """
        self.__start_time = start_time

    def system_pause(self):
        """
        每次系统暂停计时会调用
        :return:
        """
        self.__interrupt_count += 1
        pass

    def system_continue(self):
        pass

    def system_cancel_finish(self):
        """
        当按下停止计时键后，如果取消提交日志，则不算一次暂停(暂时未被调用
        :return:
        """
        self.__interrupt_count -= 1

    def system_finish(self, total_time: int, logs_infor: str):
        """

        :param total_time: 计时器所记录的总时间
        :param logs_infor: 提交时需要写自己的学习日志
        :return:
        """
        add_data = {"start_time": [self.__start_time, ], "total_time": [total_time, ], "interrupt_count": [self.__interrupt_count, ], "logs_infor": [logs_infor, ]}

        add_data = pandas.DataFrame(add_data)
        add_data.to_csv(self.__data_path, mode="a", header=False)
