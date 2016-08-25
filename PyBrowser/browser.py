#!/usr/bin/env python3
import logging
from PIL import Image
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from io import BytesIO
import time
from PyBrowser.tools import run_within_time, swing
import platform


class Browser(object):
    def __init__(self, virtual=False, v_width=1366, v_height=768, driver=None):
        """
        在虚拟环境中打开一个火狐浏览器
        :param virtual: 是否使用虚拟化图形界面; 该选项可让程序在无图形化环境的服务器系统运行.
        :param v_width: 虚拟图形环境的宽度
        :param v_height: 虚拟图形环境的高度
        :param driver: 自定义webdriver, 留空则默认使用chrome浏览器,请确保path里能找到chrome执行文件
        """
        self.logger = logging.getLogger('PyBrowser')
        # 虚拟图形环境
        self.virtual = virtual
        if virtual:
            self.display = Display(visible=False, size=(v_width, v_height))
            self.display.start()

        # 浏览器初始化
        if not driver:
            self.driver = self.get_driver()

        self.find = self.driver.find_element_by_css_selector  # 函数别名
        self.driver.implicitly_wait(20)  # find的默认超时时间

    def get_driver(self):
        chromedriver_path = './bin/chromedriver.{}'.format(platform.system())
        return webdriver.Chrome(chromedriver_path)

    def get(self, url):
        """
        跳转到给定网址
        """
        self.driver.get(url)

    def quit(self):
        """
        关闭浏览器
        """
        self.driver.quit()

    def run(self, func, *args):
        """
        执行浏览器脚本(一个函数)
        这个脚本函数的定义应为: def foo(this, elem)
        其中, this参数将传入Browser实例,elem参数为一个css路径容器,用以简化代码
        :param func: 脚本函数
        :return: 脚本函数的return
        """
        return func(self, *(ElemPaths(self), *args))

    def wait(self, condition_funcs, max_wait_seconds=60, min_wait_seconds=4, interval=2):
        """
        阻塞进程,不断检测给定的条件函数(集),直至某一给定的条件函数返回值为True.

        :param max_wait_seconds: 最长等待时间
        :param min_wait_seconds: 最小等待时间
        :param interval: 监测间隔. 注意,若条件函数运行时间超过interval, 函数运行将被强制终止
        :param condition_funcs: 条件函数, 可以使用tuple装载多个条件, 也可以只提供一个条件
        该条件的定义应为: def foo(this), 其中,this为Browser实例
        建议使用lambda表达式,例如,一个监测网页中是否出现"验证码错误"的条件函数为:
        `lambda this: "验证码错误" in this.html`
        :return -1: max_wait_seconds时间内, 所有条件函数均检测失败
        :return >=0: 检测成功时,条件函数的索引号
        :rtype: int
        """
        # 参数校正
        assert condition_funcs is not None, 'condition_funcs参数不能为空'
        assert min_wait_seconds < max_wait_seconds, 'min_wait_seconds 应小于 max_wait_seconds'
        if not isinstance(condition_funcs, tuple) and not isinstance(condition_funcs, list):
            condition_funcs = (condition_funcs,)

        # 按interval时间执行条件函数,直至成功
        max_time = time.time() + max_wait_seconds
        min_time = time.time() + min_wait_seconds
        while True:
            now = time.time()
            if now > max_time:  # 超时
                self.logger.debug('[Browser]', 'wait执行超时')
                return -1
            for index, condition_func in enumerate(condition_funcs):  # 条件检测, 返回满足条件的索引
                # 条件函数运行超时检测
                try:
                    res = run_within_time(func=condition_func, args=(self,), timeout=interval)
                except TimeoutError:
                    res = False
                    self.logger.debug('[Browser]', '条件函数运行超时, index={}'.format(index))
                if res and now > min_time:
                    self.logger.debug('[Browser]', '条件函数返回True, index={}'.format(index))
                    return index
            time.sleep(interval)

    def select(self, css):
        """
        通过CSS选择器寻找元素
        :rtype: WebElement
        """
        return WebElement(self, self.driver, self.find(css))

    @property
    def root(self):
        """
        获取根元素
        :rtype: WebElement
        """
        return WebElement(self, self.driver, self.find(':root'))

    @property
    def url(self):
        """
        获取当前url
        :rtype: str
        """
        return self.driver.current_url

    @property
    def html(self):
        """
        获取页面源码
        :rtype: str
        """
        return self.root.html

    def snapshot(self, left=None, upper=None, right=None, lower=None):
        """
        获取指定矩形区域的快照
        :rtype: Image.Image
        :return: PIL.Image.Image对象, 可调用其show()方法显示, save()方法用于保存
        用完记得调用close()关啦~
        """
        # 全屏截图
        img_file = BytesIO(self.driver.get_screenshot_as_png())  # 内存文件
        img = Image.open(img_file, 'r')

        if (upper and right and lower and left) is not None:  # 裁剪
            assert upper <= lower, 'error, top > bottom!'
            assert left <= right, 'error, left > right!'
            img = img.crop(map(int, (left, upper, right, lower)))

        return img


class WebElement(object):
    """
    对网页中的某个元素的操作
    """

    def __init__(self, _browser, _driver, _this):
        self.this = _this  # 原生selenium元素对象
        self.driver = _driver  # 老司机,哈哈;原生webdriver
        self.browser = _browser  # 封装后的webdriver
        self.action = webdriver.ActionChains(self.driver)

    @property
    def html(self):
        """
        得到元素html源码
        :rtype: str
        """
        return self.this.get_attribute('innerHTML')

    def focus(self, x_offset=0, y_offset=0):
        """
        将鼠标移动到这个元素上,并可指定相对偏移量
        :rtype: WebElement
        """
        self.action.move_to_element_with_offset(self.this, x_offset, y_offset).perform()
        return self

    def rclick(self):
        """
        右键单击
        :rtype: WebElement
        """
        self.focus()
        self.action.context_click(self.this).perform()
        return self

    def dclick(self):
        """
        左键双击
        :rtype: WebElement
        """
        self.focus()
        self.action.double_click(self.this).perform()
        return self

    def click(self):
        """
        左键单击
        :rtype: WebElement
        """
        self.focus()
        self.this.click()
        return self

    def submit(self):
        """
        提交
        :rtype: WebElement
        """
        self.focus()
        self.this.submit()
        return self

    def clear(self):
        """
        清空元素内容
        :rtype: WebElement
        """
        self.this.clear()
        return self

    def send(self, value):
        """
        快速输入内容到元素中
        :rtype: WebElement
        """
        self.this.send_keys(value)
        return self

    def input(self, value):
        """
        模拟人的输入, 分为focus,clear,click,send等步骤, 并模拟人的打字速度
        注: 不支持控制键, 仅支持纯文本输入
        :rtype: WebElement
        """
        self.focus().sleep(0.15)
        self.clear().sleep(0.1)
        self.click().sleep(0.2)
        assert isinstance(value, str), '模拟输入仅支持传入字符串'
        for i in value:  # 一个一个地输入
            self.sleep(0.08, 0.25)
            self.this.send_keys(i)
        return self

    def sleep(self, seconds, max_range=None):
        """
        :param seconds: 休眠秒
        :param max_range: 上下浮动范围, 默认为基础数的30%, 不会小于0
        :rtype: WebElement
        """
        if max_range is None:
            max_range = seconds * 0.3
        tmp = swing(seconds, max_range)
        if tmp < 0:
            tmp = 0
        time.sleep(tmp)
        return self

    def snapshot(self):
        """
        获取元素的快照
        :rtype: Image.Image
        :return: PIL.Image.Image对象, 可调用其show()方法显示, save()方法用于保存
        用完记得调用close()关啦~
        """
        # 裁剪
        left = self.location['x']
        upper = self.location['y']
        right = self.location['x'] + self.size['width']
        lower = self.location['y'] + self.size['height']
        return self.browser.snapshot(left, upper, right, lower)

    @property
    def size(self):
        """
        元素尺寸
        :rtype: dict
        :return: size['width'] size['height']
        """
        return self.this.size

    @property
    def location(self):
        """
        元素位置
        :rtype: dict
        :return: location['x'] location['y']
        """
        return self.this.location

    def attr(self, name):
        """
        获取属性
        """
        return self.this.get_attribute(name)


class ElemPaths(dict):
    """
    路径字典, 使用字典映射"元素名" -> "元素css路径"
    """

    def __init__(self, browser: Browser, iterable=None, **kwargs):
        self.browser = browser
        super(ElemPaths, self).__init__(iterable=iterable, **kwargs)

    def __getitem__(self, item):
        """
        :rtype: WebElement
        """
        css = super(ElemPaths, self).__getitem__(item)
        return self.browser.select(css)

    def get(self, item, d=None):
        """
        从字典取值时, 将路径转换为WebElement
        :rtype: str
        """
        return super(ElemPaths, self).__getitem__(item)


if __name__ == '__main__':
    b = Browser()
    b.get('http://www.baidu.com')
    b.select('#kw').input('为什么我有了奥特曼变身器仍然不能变身?').send(Keys.ENTER)
