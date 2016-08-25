#!/usr/bin/env python3
from PyBrowser import Browser, Keys

browser = Browser()
browser.get("http://www.baidu.com")
browser.select("#kw").input("Hello world").send(Keys.ENTER)
