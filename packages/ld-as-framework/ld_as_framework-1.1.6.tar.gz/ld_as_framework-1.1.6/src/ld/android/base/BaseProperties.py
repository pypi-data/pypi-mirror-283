# encoding:utf-8
from ..environment.Device import DeviceOperation

class Rect:

    """
    获取控件在屏幕中的位置

    left x坐标

    top y坐标

    width 控件的宽度

    height 控件的高度

    centerX 控件的中心坐标X

    centerY 控件的中心坐标Y
    """

    def __init__(self, left=None, top=None, width=None, height=None, centerX=None, centerY=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY


class CommonResult:
    """
    查询元素的公共返回体
    """

    def __init__(self, source_target, rect: Rect):
        """
        调用获取元素方法后拿到的返回结果，经过统一包装
        :param source_target: 查询后的源对象
        :param rect: 查询后得到的坐标信息对象，要自行包装
        """
        self.target = source_target
        self.rect: Rect = rect


class AScriptQueryElement:
    """
    AS元素查询父类，所有的元素查询都需要继承该类
    """

    def __init__(self):
        screen_info = DeviceOperation.get_device_display()  # 获取屏幕宽度w 高度h
        self._w, self._h = screen_info.width, screen_info.height
        self._rects = {
            1: [0, 0, int(self._w * 0.5), int(self._h * 0.5)],  # 左上角
            2: [int(self._w * 0.5), 0, int(self._w), int(self._h * 0.5)],  # 右上角
            3: [0, int(self._h * 0.5), int(self._w * 0.5), int(self._h)],  # 左下角
            4: [int(self._w * 0.5), int(self._h * 0.5), self._w, self._h],  # 右下角
            5: [0, 0, int(self._w), int(self._h * 0.5)],  # 上半截
            6: [0, int(self._h * 0.5), int(self._w), int(self._h)],  # 下半截
            7: [0, 0, int(self._w * 0.5), int(self._h)],  # 左半截
            8: [int(self._w * 0.5), 0, int(self._w), int(self._h)],  # 右半截
            9: [int(self._w * 0.2), int(self._h * 0.1), int(self._w * 0.9), int(self._h * 0.7)],  # 中间
        }
        self.properties = dict()
        self.properties['rect'] = []

    def rect_left_top(self):
        """
        获取左上角范围
        :return:
        """
        self.properties['rect'] = self._rects[1]
        return self

    def rect_right_top(self):
        """
        获取右上角范围
        :return:
        """
        self.properties['rect'] = self._rects[2]
        return self

    def rect_left_bottom(self):
        """
        获取左下角范围
        :return:
        """
        self.properties['rect'] = self._rects[3]
        return self

    def rect_right_bottom(self):
        """
        获取右下角范围
        :return:
        """
        self.properties['rect'] = self._rects[4]
        return self

    def rect_half_top(self):
        """
        获取上半屏范围
        :return:
        """
        self.properties['rect'] = self._rects[5]
        return self

    def rect_half_bottom(self):
        """
        获取下半屏范围
        :return:
        """
        self.properties['rect'] = self._rects[6]
        return self

    def rect_half_left(self):
        """
        获取左半屏范围
        :return:
        """
        self.properties['rect'] = self._rects[7]
        return self

    def rect_half_right(self):
        """
        获取右半屏范围
        :return:
        """
        self.properties['rect'] = self._rects[8]
        return self

    def rect_center(self):
        """
        获取中间范围
        :return:
        """
        self.properties['rect'] = self._rects[9]
        return self

    def _find_element(self, eleName) -> CommonResult:
        pass

    def _find_all_element(self, eleName) -> list:
        pass
