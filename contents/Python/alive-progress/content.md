# 快来给你的程序换上好看的进度条吧！

> 本文适合有 Python 基础的朋友

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，本期介绍基于 Python 的开源进度条模块——**alive-progress**，一个可以让你快速拥有完美进度条的 Python 模块。

> 项目地址：https://github.com/rsalmei/alive-progress

不知你是否有过这样的经历：你写了一个程序，每次运行都会耗费很长时间。在等待程序运行期间你一次次的按下回车防止程序卡死。亦或者你的任务需要实时掌握程序运行进度但你根本不知道程序执行到了哪里... ...

现在，alive-progress 来了，它是一个 Python 下的进度条库，不仅使用方便而且支持多种炫酷显示效果！

## 一、安装

在 Python 下使用 pip 进行安装：

```shell
pip install alive-progress
```

## 二、快速入门

### 1. 循环中使用

在循环中使用 alive-progress 最常见的用法，假设我们需要遍历一个数组，脚本可以这样写：

```python
# 导入 alive-progress 库
from alive_progress import alive_bar
import time

# arr 是我们需要遍历的数组
arr = [1,3,5,7,9,11]

# 使用 with 语句创建一个 进度条 对象，
# 方便使用后自动释放相关资源
with alive_bar(len(arr)) as bar:	# 需要给 alive_bar 传入进度条总数目（这里是 6）
    for item in arr:
        # 等待 1s
        time.sleep(1)
        #更新进度条，进度 +1
        bar()
```

运行以上代码我们可以看到在终端中出现了一个还算华丽的动态进度条

![code-1](E:\Article\contents\Python\alive-progress\images\1.png)

> 需要注意的是，alive-progress 并不像 tqdm 等进度条库一样会自动更新，只有我们程序调用了 alive_bar 对象才会让进度条 +1

