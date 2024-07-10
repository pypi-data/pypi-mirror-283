# encoding:utf-8
import time

from typing import Union

class TimeUtil:

    @staticmethod
    def timestamp():
        """
        获取当前时间的时间戳
        :return:返回当前时间的时间戳
        """
        return time.time()

    @staticmethod
    def time_difference(time1, time2) -> Union[int, float]:
        """
        计算两个时间戳之间的时间差
        :return:返回时间差值
        """
        if (type(time1) == int or type(time1) == float) and (type(time2) == int or type(time2) == float):
            difference_seconds = abs(float(time2) - float(time1))
            return int(difference_seconds)
        else:
            raise TypeError("类型错误 当前类型为 参数1{} 参数2{}".format(type(time1), type(time2)))


class 时间(TimeUtil):
    @staticmethod
    def 获取当前时间戳():
        """
        获取当前时间的时间戳
        :return:返回当前时间的时间戳
        """
        return TimeUtil.timestamp()

    @staticmethod
    def 时间差(time1, time2) -> Union[int, float]:
        """
        计算两个时间戳之间的时间差
        :return:返回时间差值
        """
        return TimeUtil.time_difference(time1, time2)
