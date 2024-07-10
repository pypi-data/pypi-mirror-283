import random

from typing import Union

class ListUtil:

    @staticmethod
    def get_len(s: list) -> int:
        """
        获取列表长度
        :param s:用于获取长度的列表
        :return:成功返回列表长度，类型错误抛出TypeError异常
        """
        return len(s)

    @staticmethod
    def is_empty(s: list) -> bool:
        """
        判断列表是否为空
        :param s:用于判断是否为空的列表
        :return:成功返回True，失败返回False，类型错误抛出TypeError异常
        """
        return s is not None and len(s) > 0

    @staticmethod
    def sort(s: list) -> list:
        """
        将列表内元素正向排序
        :param s:用于排序的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        return sorted(s)

    @staticmethod
    def sort_reverse(s: list) -> list:
        """
        将列表内元素反向排序
        :param s:用于排序的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        return sorted(s, reverse=True)

    @staticmethod
    def shuffle(s: list) -> list:
        """
        将列表内元素随机排序
        :param s:用于排序的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        tmp = list()
        tmp.extend(s)
        random.shuffle(tmp)
        return tmp

    @staticmethod
    def remove_duplicates(s) -> Union[list]:
        """
        删除列表内重复的元素
        :param s:用于删除重复元素的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        if type(s) == list:
            new_s = list(dict.fromkeys(s))
            return new_s
        else:
            raise TypeError("类型不是列表 当前类型为{}".format(type(s)))


class 列表:
    @staticmethod
    def 获取长度(s: list) -> Union[int]:
        """
        获取列表长度
        :param s:用于获取长度的列表
        :return:成功返回列表长度，类型错误抛出TypeError异常
        """
        return ListUtil.get_len(s)

    @staticmethod
    def 是否为空(s) -> Union[int]:
        """
        判断列表是否为空
        :param s:用于判断是否为空的列表
        :return:成功返回True，失败返回False，类型错误抛出TypeError异常
        """
        return ListUtil.is_empty(s)

    @staticmethod
    def 正向排序(s) -> Union[list]:
        """
        将列表内元素正向排序
        :param s:用于排序的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        return ListUtil.sort(s)

    @staticmethod
    def 反向排序(s) -> Union[list]:
        """
        将列表内元素反向排序
        :param s:用于排序的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        return ListUtil.sort_reverse(s)

    @staticmethod
    def 随机排序(s) -> Union[list]:
        """
        将列表内元素随机排序
        :param s:用于排序的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        return ListUtil.shuffle(s)

    @staticmethod
    def 删除重复(s) -> Union[list]:
        """
        删除列表内重复的元素
        :param s:用于删除元素的列表
        :return:成功返回一个新列表，类型错误抛出TypeError异常
        """
        return ListUtil.remove_duplicates(s)
