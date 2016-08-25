#!/usr/bin/env python3
"""
演示使用Browser.run()运行脚本, 使用ElemPaths保存控件位置
"""
from PyBrowser import Browser


def baidu_search(this, path, _keyword):
    this.get("http://www.baidu.com")
    # 录入路径, 方便后面使用. 在控件特别多的情况下很方便
    path['输入框'] = "#kw"
    path['百度一下'] = '#su'
    path['结果数量'] = '.nums'

    path['输入框'].input(_keyword)
    path['百度一下'].click().sleep(2)

    # 返回搜索数量
    return path['结果数量'].html


def bing_search(this, path, _keyword):
    this.get("http://cn.bing.com")
    # 录入路径, 方便后面使用. 在控件特别多的情况下很方便
    path['输入框'] = "#sb_form_q"
    path['按钮'] = '#sb_form_go'
    path['结果数量'] = '.sb_count'

    path['输入框'].input(_keyword)
    path['按钮'].click()

    # 返回搜索数量
    return path['结果数量'].html


if __name__ == '__main__':
    browser = Browser()
    keyword = "为什么我有了奥特曼变身器仍然不能变身?"
    baidu_res = browser.run(baidu_search, keyword)
    bing_res = browser.run(bing_search, keyword)
    print(baidu_res, '\n',
          bing_res, "\n按下任意键退出")
    input()
    browser.quit()
