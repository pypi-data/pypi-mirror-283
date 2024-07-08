# 判断类型
class TypeUtil:

    @staticmethod
    def judgement_type(s):
        """
        判断类型
        :param s:判断该参数的类型
        :return:返回类型
        """
        return type(s)

    @staticmethod
    def judgement_boolean(s):
        """
        判断是否为布尔类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(s) == bool:
            return True
        else:
            return False

    @staticmethod
    def judgement_num(num):
        """
        判断是否为数字类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(num) == int or type(num) == float:
            return True
        else:
            return False

    @staticmethod
    def judgement_int(num):
        """
        判断是否为整数类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(num) == int:
            return True
        else:
            return False

    @staticmethod
    def judgement_float(num):
        """
        判断是否为小数类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(num) == float:
            return True
        else:
            return False

    @staticmethod
    def judgement_str(s):
        """
        判断是否为字符串类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(s) == str:
            return True
        else:
            return False

    @staticmethod
    def judgement_list(s):
        """
        判断是否为列表类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(s) == list:
            return True
        else:
            return False

    @staticmethod
    def judgement_dict(s):
        """
        判断是否为字典类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        if type(s) == dict:
            return True
        else:
            return False


class 类型(TypeUtil):
    @staticmethod
    def 判断类型(text):
        """
        判断类型
        :param s:判断该参数的类型
        :return:返回类型
        """
        return TypeUtil.judgement_type(text)

    @staticmethod
    def 是否布尔(s):
        """
        判断是否为布尔类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_boolean(s)

    @staticmethod
    def 是否数字(num):
        """
        判断是否为数字类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_num(num)

    @staticmethod
    def 是否整数(num):
        """
        判断是否为整数类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_int(num)

    @staticmethod
    def 是否小数(num):
        """
        判断是否为小数类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_float(num)

    @staticmethod
    def 是否字符(s):
        """
        判断是否为字符串类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_str(s)

    @staticmethod
    def 是否列表(s):
        """
        判断是否为列表类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_list(s)

    @staticmethod
    def 是否字典(s):
        """
        判断是否为字典类型
        :param s:判断该参数的类型
        :return:是返回True，否返回False
        """
        return TypeUtil.judgement_dict(s)
