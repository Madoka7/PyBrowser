#!/usr/bin/env python3
import random
import signal


def random_str(length=8):
    """
    生成随机字符串
    :param length: 字符串长度
    :rtype: str
    """
    string = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.sample(string, length))


def swing(base, max_range, _min=None):
    """
    产生一个 base ± max_range 范围内的随机数
    :param base: 基础数
    :param max_range: 最大摆动范围
    :param _min: 最小值
    :return:
    """
    random_num = random.random() - 0.5
    r = base + max_range * random_num * 2
    if _min is not None and r < _min:
        r = _min
    return r


def run_within_time(func, args: tuple, timeout):
    """
    执行一个函数, 并在timeout后弹出异常
    :param func: 函数
    :param args: 参数
    :param timeout: 超时时间
    :return:
    """

    def handle(signum, frame):
        raise TimeoutError('函数运行超时')

    signal.signal(signal.SIGALRM, handle)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        res = func(*args)
    finally:
        signal.alarm(0)
    return res
