## 安装
1. 确保chrome执行文件能在$PATH里找到
    + 若没有chrome, 推荐安装chromium:
    ```
    sudo apt-get install chromium-browser
    ```

2. 下载对应版本的[chromedriver](http://chromedriver.storage.googleapis.com/index.html), 解压后放在$PATH路径里;
    + ubuntu下还可以通过apt来安装:
    ```    
    sudo apt-get install chromium-chromedriver
    sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
    ```

3. 安装依赖:
    ```
    pip3 install pyvirtualdisplay selenium
    sudo apt-get install python3-setuptools xvfb
    ```

4. 安装PyBrowser:
    ```
    python3 setup.py install
    ```

## Hello World!
```python
from PyBrowser import Browser, Keys

browser = Browser()
browser.get("http://www.baidu.com")
browser.select("#kw").input("Hello world").send(Keys.ENTER)
```

## 百度搜索
```python
from PyBrowser import Browser

def baidu_search(this, path, s):
    this.get("http://www.baidu.com")
    path['输入框'] = "#kw"
    path['百度一下'] = '#su'
    path['结果数量'] = '.nums'

    path['输入框'].input(s)
    path['百度一下'].click().sleep(2)

    return path['结果数量'].html

if __name__ == '__main__':
    browser = Browser()
    baidu_res = browser.run(baidu_search, "为什么我有了奥特曼变身器仍然不能变身?")
    print(baidu_res, "\n按下任意键退出")
    input()
    browser.quit()
```
