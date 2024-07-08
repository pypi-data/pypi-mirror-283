# encoding:utf-8
import random

import time

from typing import TypeVar

from ..base.BaseProperties import AScriptQueryElement, CommonResult

from ...common.Logger import log_ld

class Method:

    def __init__(self, target, *args, **kwargs):
        self.ref = None
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        if self.ref is None:
            return self.target(*self.args, **self.kwargs)
        else:
            return getattr(self.ref, self.target.__name__)(*self.args, **self.kwargs)


CommonActionType = TypeVar('CommonActionType', bound='CommonAction | None')


class CommonAction:

    def __init__(self, selector: AScriptQueryElement, eleName, framework):
        # 查询对象
        self._selector: AScriptQueryElement = selector
        # 对框架本身的引用，只要被实例化就绝对不可能为空
        self._framework = framework
        # 当前查询元素的特征信息
        self._eleName = eleName
        # 用来存放操作的链
        self._chain: list[Method] = []
        # 查询元素以后的返回值
        self._ele_target: CommonResult | None = None
        self._chain.append(Method(self._find))

    def _find(self):
        start_time = time.time()
        ele_target = getattr(self._selector, "_find_element")(self._eleName)
        end_time = "%.3f" % (time.time() - start_time)
        if ele_target:
            log_ld.info(
                f"查询元素{self._eleName}成功，耗时：{end_time}，返回值：{ele_target.rect.__dict__}")
            log_ld.debug(f"查询元素{self._eleName}成功，原始返回值：{ele_target.target}")
            self._ele_target = ele_target
            return self
        log_ld.warning(f"查询元素{self._eleName}失败，耗时：{end_time}，请检查屏幕是否存在该元素")
        return False

    def execute(self, sleep=0.5, loop=1):
        """
        执行动作链
        :param sleep: 执行一次延迟时间，单位（秒）
        :param loop:执行次数
        """
        log_ld.debug(f"方法链长度：{len(self._chain)}")
        new_obj_method = ["_element", "_wait_element"]
        for i in range(loop):
            obj_ref = None
            execute_chain = self._chain[::-1]
            while execute_chain:
                method = execute_chain.pop()
                execute_method_name = method.target.__name__
                if execute_method_name in new_obj_method:
                    obj_ref = method.execute()
                    if obj_ref is False:
                        # 如果是等待元素之类的任务，需要有元素才可以继续
                        break
                    execute_chain.append(Method(self._find))
                    continue
                method.ref = obj_ref
                result = method.execute()
                log_ld.debug(
                    f"方法 {method.target.__name__} 执行成功，是否继续执行：{False if result == False else True}")
                if result is False:
                    break
            time.sleep(sleep)

    def 执行(self, sleep=0.5, loop=1) -> CommonActionType:
        return self.execute(sleep, loop)

    def element(self, *args: str) -> CommonActionType:
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        self._chain.append(Method(self._element, *args))
        return self

    def 元素_操作(self, *args: str) -> CommonActionType:
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        return self.element(*args)

    def _element(self, *args: str) -> CommonActionType:
        return self._framework.element(*args)

    def sleep(self, second) -> CommonActionType:
        """
        延迟
        :param second:延迟时间，单位秒
        """
        self._chain.append(Method(self._sleep, second))
        return self

    def 延迟(self, second) -> CommonActionType:
        """
        延迟
        :param second:延迟时间，单位秒
        """
        return self.sleep(second)

    def ramdom_sleep(self, second, float_tame=0.3) -> CommonActionType:
        """
        随机延迟时间范围，从(second - float_tame) ~ (second + float_tame)范围内随机延迟
        :param second:延迟时间，单位秒
        :param float_tame:浮动时间
        """
        self._chain.append(Method(self._ramdom_sleep, second, float_tame))
        return self

    def 随机_延迟(self, second, float_tame=0.3) -> CommonActionType:
        """
        随机延迟时间范围，从(second - float_tame) ~ (second + float_tame)范围内随机延迟

        :param second:延迟时间，单位秒
        :param float_tame:浮动时间
        """
        return self.ramdom_sleep(second, float_tame)

    def _sleep(self, second) -> CommonActionType:
        time.sleep(second)
        return self

    def _ramdom_sleep(self, second, float_tame=0.3) -> CommonActionType:
        time.sleep(random.uniform(second - float_tame, second + float_tame))
        return self

    def assert_element(self, condition) -> CommonActionType:
        """
        断言
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda，如果返回False，则不执行后面的链
        """
        self._chain.append(Method(self._assert_element, condition))
        return self

    def 断言_元素(self, condition) -> CommonActionType:
        """
        断言
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda，如果返回False，则不执行后面的链
        """
        return self.assert_element(condition)

    def _assert_element(self, condition) -> bool:
        return condition(self._ele_target)

    def execute_method(self, method) -> CommonActionType:
        """
        执行一个方法，如果方法返回False，则不继续执行后面的链
        :param method:需要执行的方法
        """
        self._chain.append(Method(self._execute_method, method))
        return self

    def 执行_方法(self, method) -> CommonActionType:
        """
        执行一个方法，如果方法返回False，则不继续执行后面的链
        :param method:需要执行的方法
        """
        return self.execute_method(method)

    @staticmethod
    def _execute_method(method) -> bool:
        return method()

    def click(self, x=None, y=None, r=5, rx: int = 0, ry: int = 0):
        """
        点击某个坐标，如果不穿参数，则是点击找到元素的位置
        :param x:屏幕的绝对x坐标，和y一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param y:屏幕的绝对y坐标，和x一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param r:随机偏移坐标，以x,y为中心，点击的时候偏移r个像素
        :param rx:相对坐标x，以x（不管是元素的还是传入的）为中心加上rx作为点击的偏移像素
        :param ry:相对坐标y，以y（不管是元素的还是传入的）为中心加上ry作为点击的偏移像素
        """
        self._chain.append(Method(self._click, x, y, r, rx, ry))
        return self

    def 点击_坐标(self, x=None, y=None, r=5, rx: int = 0, ry: int = 0) -> CommonActionType:
        """
        点击某个坐标，如果不穿参数，则是点击找到元素的位置
        :param x:屏幕的绝对x坐标，和y一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param y:屏幕的绝对y坐标，和x一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param r:随机偏移坐标，以x,y为中心，点击的时候偏移r个像素
        :param rx:相对坐标x，以x（不管是元素的还是传入的）为中心加上rx作为点击的偏移像素
        :param ry:相对坐标y，以y（不管是元素的还是传入的）为中心加上ry作为点击的偏移像素
        """
        return self.click(x, y, r, rx, ry)

    def _click(self, x, y, r, rx=0, ry=0):
        if x is not None and y is not None:
            self._framework.click(x + rx, y + ry, r)
            return
        if self._ele_target.rect is None:
            log_ld.warning(f"点击坐标失败，没有可点击元素{self._eleName}")
            return False
        else:
            self._framework.click(self._ele_target.rect.centerX + rx, self._ele_target.rect.centerY + ry, r)
        return self

    def click_element(self, r=5):
        """
        如果是节点，该方法是点击节点，如果是其他元素，则是坐标，偏移参数对点击节点无效
        :param r: 偏移像素
        """
        self._chain.append(Method(self._click_element, r))
        return self

    def 点击_元素(self, r=5) -> CommonActionType:
        """
        如果是节点，该方法是点击节点，如果是其他元素，则是坐标，偏移参数对点击节点无效
        :param r: 偏移像素
        """
        return self.click_element(r)

    def _click_element(self, r=5):
        if self._ele_target is not None:
            self._framework.click(self._ele_target.rect.centerX, self._ele_target.rect.centerY, r)
        return self

    def wait_element(self, element: list, timeout=3) -> CommonActionType:
        self._chain.append(Method(self._wait_element, element, timeout))
        return self

    def 元素_等待(self, element: list, timeout=3) -> CommonActionType:
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        return self.wait_element(element, timeout)

    def _wait_element(self, element: list, timeout=3):
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        log_ld.debug(f"开始等待元素:{element},{time.time()},  timout:{timeout}")

        def tmp():
            tmp_ele = self._framework.element_exist(*element)
            if tmp_ele:
                return tmp_ele

        ele = self._framework.execute_with_timeout(timeout, tmp)
        log_ld.debug(f"等待元素结束:{element},返回值：{ele}")
        if ele is None:
            return False
        return ele

    def swipe(self, from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False):
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间，单位(秒)
        :param will_continue: 结束时候是否抬起手指
        """
        self._chain.append(Method(self._swipe, from_point, to_point, timeout, will_continue))
        return self

    def 滑动(self, from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False) -> CommonActionType:
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间
        :param will_continue: 结束时候是否抬起手指
        """
        return self.swipe(from_point, to_point, timeout, will_continue)

    def _swipe(self, from_point, to_point, timeout=1, will_continue=True):
        self._framework.swipe(from_point, to_point, timeout, will_continue)

    def compare_color(self, *args):
        self._chain.append(Method(self._compare_color, *args))
        return self

    def 比色(self, *args):
        return self.compare_color(*args)

    def _compare_color(self, *args):
        return self._framework.compare_color(*args)
