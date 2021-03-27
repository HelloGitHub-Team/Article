# 快来给你的程序换上好看的进度条吧！

> 本文适合有 Python 基础的朋友

![4](images\4.gif)

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，本期介绍基于 Python 的开源进度条模块——**alive-progress**，一个可以让你快速拥有完美进度条的 Python 模块。

> 项目地址：https://github.com/rsalmei/alive-progress

不知你是否有过这样的经历：你写了一个程序，每次运行都会耗费很长时间。在等待程序运行期间你一次次的按下回车防止程序卡死。亦或者你的任务需要实时掌握程序运行进度但你根本不知道程序执行到了哪里......

现在，alive-progress 来了，它是一个 Python 下的进度条库，不仅使用方便而且支持多种炫酷显示效果！让我们先来看看示例效果：

![3](images\2.gif)

![3](images\3.gif)

## 一、安装

在 Python 下使用 pip 进行安装：

```shell
pip install alive-progress
```

## 二、快速入门

### 1. 直接使用

在循环中使用 alive-progress 最常见的用法，假设我们需要遍历一个数组，脚本可以这样写：

```python
# 导入 alive-progress 库
from alive_progress import alive_bar
import time

# arr 是我们需要遍历的数组
arr = [1,3,5,7,9,11]

# 使用 with 语句创建一个进度条
with alive_bar(len(arr)) as bar:	# 给 alive_bar 传入进度条总数目（这里是 6）
    for item in arr:
        # 等待 1s
        time.sleep(1)
        #更新进度条，进度 +1
        bar()
```

> 请注意

运行以上代码我们可以看到在终端中出现了一个还算华丽的动态进度条

![7](images\1.gif)

> 需要注意的是，alive-progress 并不像 tqdm 等进度条库一样会自动更新，只有我们程序调用了 bar 才会让进度条 +1

当然，我们也可以不给进度条传入总数目这个参数，此时进度条将不显示进度，并进入**未定义**模式

![6](images\5.gif)

有时候我们想直接操纵显示的位置，这时候可以设定 ``alive_bar`` 的 ``manual`` 参数为 ``True``：

```python
from alive_progress import alive_bar
import time

total = 100
with alive_bar(total, manual=True) as bar:	# total 可以不指定，这时候只有百分比
    bar(0.5) # 进度到 50%
    time.sleep(0.5)
    bar(0.1) # 进度到 10% 
    time.sleep(0.5)
    bar(0.75) # 进度到 75%
    time.sleep(0.5)
    bar(1.0) # 进度到 100%
    time.sleep(0.5)
    bar(10) # 进度到 1000%
    for i in range(1,101):
        bar(i/100) # 设定进度为 i%
        time.sleep(0.05)
```

![8](images\6.gif)

当然，在运行过程中我们也需要输出一些提示信息，直接使用 ``print`` 可以在不破坏进度条的情况下输出一行提示信息，``text`` 方法则可以在进度条尾部添加后缀字符，而 ``title`` 参数则可以给进度条添加标题（前缀信息），具体使用方法及效果如下：

```python
from alive_progress import alive_bar
import time

# 定义标题（前缀字符）为 HelloGithub
with alive_bar(10, title="HelloGithub") as bar:
    for i in range(10):
        time.sleep(1)

        bar()   # 让进度 +1
        bar.text("Doning Work #%d"%(i+1))   # 更新进度条后缀

        print("Work #%d finished"%i)        # 输出一行信息
```

![1](images\7.gif)

### 2. 添点花样

看多了传统的进度条样式想换换花样？没问题，alive-progress 不仅内置了多种进度条样式，还支持自定义格式。

进度条可以自定义的样式分为两种：``bar`` 和 ``spinner ``，只需要在调用 ``alive_bar`` 的时候传入对应的参数即可

![4](images\4.gif)

以这个进度条为例，中间最长的是 ``bar``，旁边来回晃动的 ``www.HelloGithub.com``是 ``spinner``。

alive-progress 内置了多种 bar 和 spinner 样式，只需要调用 ``show_bars`` 或者 ``show_spinners`` 即可快速预览相应的样式，例如：

```python
from alive_progress import show_bars

show_bars() # 查看内置 bar 样式
```

![3](images\3.gif)

```python
from alive_progress import show_spinners

show_spinners() # 查看内置 spinner 样式
```

![3](images\2.gif)

默认样式使用起来非常简单，例如我想使用 ``bubbles`` 这个 bar 和 ``message_scrolling`` 这个 spinner，直接传入对应名称即可

```python
from alive_progress import alive_bar
import time

# 直接传入对应名字即可
with alive_bar(
            100,
            title="HelloGithub", 
            bar="bubbles", spinner="message_scrolling"
            ) as bar:

    for i in range(100):
        time.sleep(.1)
        bar()
```

![8](images\8.gif)

如果不知道 ``total`` 的数目，可以使用 ``unknown`` 参数（这时候将替换 bar 为 spinner）：

```python
from alive_progress import alive_bar
import time

with alive_bar(
            title="HelloGithub", 
    		# 注意：这里 bar 被换成了unknow，内置样式名称与 spinner 的相同
            unknown="stars", spinner="message_scrolling"
            ) as bar:

    for i in range(100):
        time.sleep(.1)
        bar()
```

![1](images\9.gif)

### 3. 私人定制

或许比起直接使用内置模板你更喜欢自己定制的进度条，对此 alive-progress 也提供了对应方法。

#### 定制 bar

使用 ``standard_bar_factory`` 方法可以快速定制 bar，bar 可以设置的参数有五个：

``chars``：正在执行单元的动画，按照进度依次显示。

 ``borders``：进度条边界，显示在左右两边。

``background``：未执行到单元显示的内容。

``tip``：执行单元的前导符号。

``errors``：出错时（进度未走全，超出 total 值等）时显示的字符。

例如我们想做一个如图所示的 bar：

![1](images\10.gif)

则可以这样来写：

```python
from alive_progress import alive_bar, standard_bar_factory
import time

##-------自定义 bar-------##
my_bar = standard_bar_factory(	# 以下参数均有默认值，不必一次全部修改
                            chars="123456789#", # 加载时根据进度依次显示，长度任意
                            borders="<>",		# bar 两头的边界
                            background=".",		# 未加载部分用 "." 填充
                            tip=">",			# 指示进度方向的引导符号（分割 "#" 与 ".")
    						errors="⚠❌" # 发生错误时显示的内容（未完成，溢出）	
                            )
##-------自定义结束-------##

##--------动画演示-------##
with alive_bar(
            10,
            title="HelloGithub", 
            bar=my_bar, # 这里传入刚刚自定义的 bar
    		spinner="message_scrolling",
            manual=True
            ) as bar:

    for i in range(50):
        time.sleep(.1)
        bar(i/100)
    bar(.5)
    time.sleep(2)
    bar(10)
    print("上溢")
    time.sleep(1)
    bar(1)
    print("100% 完成")
    time.sleep(1)
    bar(.1)
    print("未完成")
```

#### 定制 spinner

对于 spinner，alive-progress 提供了更多种的动画定义方式：

``frame_spinner_factory``：将传入的字符串挨个输出：

```python
from alive_progress import alive_bar, frame_spinner_factory
import time

my_spinner = my_spinner = frame_spinner_factory(
                                r'-----',
                                r'1----',
                                r'-2---',
                                r'--3--',
                                r'---4-',
                                r'----5'
                                )	# 直接传入字符串

with alive_bar(
            title="HelloGithub",
            spinner=my_spinner
            ) as bar:

    while True:
        bar()
        time.sleep(.1)
```

![1](images\11.gif)

可以看到字符串 HelloGithub 挨个循环输出。

``scrolling_spinner_factory``：将字符串滚动播出

```python
from alive_progress import alive_bar, scrolling_spinner_factory
import time

my_spinner = scrolling_spinner_factory(
    								chars="HelloGithub", # 想要播放的字符串
    								length=15,	# spinner 区域宽度
    								blank='.'	# 空白部分填充字符
									)

with alive_bar(
            title="HelloGithub",
            spinner=my_spinner
            ) as bar:

    while True:
        bar()
        time.sleep(.1)
```

![12](images\12.gif)

``bouncing_spinner_factory``：将两个字符串交替滚动播出：

```python
from alive_progress import alive_bar, bouncing_spinner_factory
import time

my_spinner = bouncing_spinner_factory(
                                    right_chars="I love", # 从左边进入的字符串
                                    length=15, # spinner 区域长度
                                    left_chars="HelloGithub", # 从右边进入的字符串
                                    blank='.', 	# 空白区域填充字符
                                    )

with alive_bar(
            title="HelloGithub",
            spinner=my_spinner
            ) as bar:

    while True:
        bar()
        time.sleep(.1)
```

![1](images\13.gif)

> 当然，也可以省略 left_chars 这个参数，其效果相当于 I love 将会像弹球一样左右弹动

## 三、结尾

到这里，相信你已经掌握了 alive_progress 的基本玩法，alive-progress 还提供了一些在不同场合所需的特殊功能，有兴趣的朋友可以通过阅读官方文档或源代码进行更加深入的了解。本次的内容就到这里了，快去创建一个属于自己的进度条吧！

## 四、参考

[alive-progress 官方主页](https://github.com/rsalmei/alive-progress)