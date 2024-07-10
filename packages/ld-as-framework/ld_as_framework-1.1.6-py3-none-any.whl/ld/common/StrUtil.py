# encoding:utf-8
import re

import random

import string

from typing import Union

class StrUtil:

    @staticmethod
    def remove_whitespace(string) -> Union[str]:
        """
        删除首尾空格
        :param string:要删除首尾空格的字符串
        :return:返回一个新的字符串
        """
        try:
            return string.strip()
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def remove_leading_whitespace(string) -> Union[str]:
        """
        删除头部空格
        :param string:要删除头部空格的字符串
        :return:返回一个新的字符串
        """
        try:
            return string.lstrip()
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def remove_trailing_whitespace(string) -> Union[str]:
        """
        删除尾部空格
        :param string:要删除尾部空格的字符串
        :return:返回一个新的字符串
        """
        try:
            return string.rstrip()
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def remove_all_whitespace(string) -> Union[str]:
        """
        删除全部空格
        :param string:要删除尾部空格的字符串
        :return:返回一个新的字符串
        """
        try:
            return string.replace(" ", "")
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def custom_split(string, delimiter) -> Union[list]:
        """
        分割字符串
        :param string:用于分割的字符串
        :param delimiter:分割符
        :return:返回列表
        """
        try:
            return string.split(delimiter)
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def extract_letters(string) -> Union[str]:
        """
        提取字符串中的全部字母
        :param string:用于提取的字符串
        :return:返回一个新的字符串
        """
        try:
            return ''.join(char for char in string if 'a' <= char <= 'z' or 'A' <= char <= 'Z')
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))
        except TypeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def extract_chinese_characters(string) -> Union[str]:
        """
        提取字符串中的全部汉字
        :param string:用于提取的字符串
        :return:返回一个新的字符串
        """
        try:
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            return ''.join(pattern.findall(string))
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))
        except TypeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def extract_numbers(string) -> Union[str]:
        """
        提取字符串中的全部数字
        :param string:用于提取的字符串
        :return:返回一个新的字符串
        """
        try:
            pattern = re.compile(r'\d+')
            return ''.join(pattern.findall(string))
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))
        except TypeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def replace_text(string, old_text, new_text) -> Union[str]:
        """
        替换文本
        :param string:用于替换的字符串
        :param old_text:被替换的文本
        :param new_text:替换成的文本
        :return:返回一个新的字符串
        """
        try:
            return string.replace(old_text, new_text)
        except AttributeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))
        except TypeError as e:
            raise TypeError("类型错误 当前类型为{}".format(type(string)))

    @staticmethod
    def generate_random_chinese(length) -> Union[str]:
        """
        随机生成汉字
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        chinese_characters = [chr(random.randint(0x4e00, 0x9fa5)) for _ in range(length)]
        return ''.join(chinese_characters)

    @staticmethod
    def generate_random_numbers(length) -> Union[str]:
        """
        随机生成数字
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        numbers = [str(random.randint(0, 9)) for _ in range(length)]
        return ''.join(numbers)

    @staticmethod
    def generate_random_lowercase(length) -> Union[str]:
        """
        随机生成小写字母
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return ''.join(chr(random.randint(97, 122)) for _ in range(length))

    @staticmethod
    def generate_random_uppercase(length) -> Union[str]:
        """
        随机生成大写字母
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return ''.join(chr(random.randint(65, 90)) for _ in range(length))

    # 随机生成混合字符
    @staticmethod
    def generate_random_mixed(length) -> Union[str]:
        """
        随机生成混合字符（大小写字母+数字的组合）
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        characters = list(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        random.shuffle(characters)
        return ''.join(characters[:length])

    @staticmethod
    def count(source_str: str, target_str: str) -> int:
        """
        统计目标字符串出现个数
        :param source_str:原始字符串
        :param target_str:需要统计字符的目标
        :return: 目标字符串出现个数
        """
        return source_str.count(target_str)


class 文本:
    @staticmethod
    def 删除首尾空格(string) -> Union[str]:
        """
        删除首尾空格
        :param string:要删除首尾空格的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.remove_whitespace(string)

    @staticmethod
    def 删除头部空格(string) -> Union[str]:
        """
        删除头部空格
        :param string:要删除头部空格的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.remove_leading_whitespace(string)

    @staticmethod
    def 删除尾部空格(string) -> Union[str]:
        """
        删除尾部空格
        :param string:要删除尾部空格的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.remove_trailing_whitespace(string)

    @staticmethod
    def 删除全部空格(string) -> Union[str]:
        """
        删除全部空格
        :param string:要删除尾部空格的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.remove_all_whitespace(string)

    @staticmethod
    def 分割文本(string, delimiter) -> Union[list]:
        """
        分割字符串
        :param string:用于分割的字符串
        :param delimiter:分割符
        :return:返回列表
        """
        return StrUtil.custom_split(string, delimiter)

    @staticmethod
    def 提取字母(string) -> Union[str]:
        """
        提取字符串中的全部字母
        :param string:用于提取的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.extract_letters(string)

    @staticmethod
    def 提取汉字(string) -> Union[str]:
        """
        提取字符串中的全部汉字
        :param string:用于提取的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.extract_chinese_characters(string)

    @staticmethod
    def 提取数字(string) -> Union[str]:
        """
        提取字符串中的全部数字
        :param string:用于提取的字符串
        :return:返回一个新的字符串
        """
        return StrUtil.extract_numbers(string)

    @staticmethod
    def 替换文本(string, old_text, new_text) -> Union[str]:
        """
        替换文本
        :param string:用于替换的字符串
        :param old_text:被替换的文本
        :param new_text:替换成的文本
        :return:返回一个新的字符串
        """
        return StrUtil.replace_text(string, old_text, new_text)

    @staticmethod
    def 随机生成汉字(length) -> Union[str]:
        """
        随机生成汉字
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return StrUtil.generate_random_chinese(length)

    @staticmethod
    def 随机生成数字(length) -> Union[str]:
        """
        随机生成数字
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return StrUtil.generate_random_numbers(length)

    @staticmethod
    def 随机生成小写字母(length) -> Union[str]:
        """
        随机生成小写字母
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return StrUtil.generate_random_lowercase(length)

    @staticmethod
    def 随机生成大写字母(length) -> Union[str]:
        """
        随机生成大写字母
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return StrUtil.generate_random_uppercase(length)

    @staticmethod
    def 随机生成混合字符(length) -> Union[str]:
        """
        随机生成混合字符（大小写字母+数字的组合）
        :param length:生成的数量，int类型
        :return:返回一个新的字符串
        """
        return StrUtil.generate_random_mixed(length)

    @staticmethod
    def 字符出现次数(source_str: str, target_str: str) -> int:
        """
        统计目标字符串出现个数
        :param source_str:原始字符串
        :param target_str:需要统计字符的目标
        :return: 目标字符串出现个数
        """
        return StrUtil.count(source_str, target_str)
