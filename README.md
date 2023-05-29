# 百度图片批量下载器
百度图片批量下载器.png![image](https://github.com/chunchaowei/Python/assets/60838771/88a974ec-5e65-4f9e-9d99-bfd762e2b185)

使用python3 + pyqt5 + eric7 + pyinstaller5 完成，

# 文件含义
```
|--__pycache__：python缓存文件内容
|
|--_eric7project：eric6项目文件内容
|
|--build：pyinstaller打包内容
|
|--dist：pyinstaller打包生成的可执行文件
|
|--BaiduImageDownloader.e4p：eric6项目文件
|
|--BaiduImageDownloader.png：界面截图
|
|--DownloadEngine.py：python3多线程下载类
|
|--Ui_main.py：qt5界面布局代码
|
|--__init__.py：自动生成的文件，空
|
|--main.py：项目主流程
|
|--main.ui：qt gui界面文件
```
# 使用方法
#### 程序猿：

依次安装[python-3.8.5](https://www.python.org/downloads/release/python-385/)、
[PyQt5-5.15.9](https://pypi.org/project/PyQt5/)、
[eric7-23.5.tar.gz](https://eric-ide.python-projects.org/eric-download.html)。


1. 下载该项目所有代码，在当前路径执行`python main.py`
2. 下载该项目所有代码，导入eric7，选中main.py，Start -> Run Script 执行

#### 人类：
MacOS ARM 13用户下载后运行main.app，在dist文件目录，双击运行。

# 已知问题
下载页数最大90.

