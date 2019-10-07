# Python 命令行之旅：初探 docopt

## 前言

在本系列前面四篇文章中，我们介绍了 `argparse` 的方方面面。它无疑是强大的，但使用方式上略显麻烦。需要先设置解析器，再定义参数，再解析命令行，最后实现业务逻辑。

而今天要介绍的 [docopt](http://docopt.org/) 则是站在一个全新的视角来审视命令行。你可曾想过，一个命令行程序的帮助信息其实已然包含了这个命令行的完整元信息，那么是否可以通过定义帮助信息来定义命令行呢？`docopt` 就是基于这样的想法去设计的。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 介绍

[docopt](http://docopt.org/) 基于长久以来在帮助信息和手册中描述程序接口的约定，其接口描述是形式化的帮助信息。它能够根据命令行程序中定义的接口描述，来自动生成解析器。

## 快速开始

### 定义接口描述/帮助信息

第一步要做的就是命令行程序的定义接口描述或者是帮助信息，这样 `docopt` 就能知道命令行的元信息，从而自动解析。

接口描述通常定义在一个模块的文档字符串中，我们仍然以在 `Python 命令行之旅：初探 argparse` 的例子为例，讲解如何使用 `docopt` 来定义接口描述。

在 `cmd.py` 中，我们定义如下接口描述：

```python
"""Num accumulator.

Usage:
  cmd.py [--sum] <num>...
  cmd.py (-h | --help)

Options:
  -h --help     Show help.
  --sum         Sum the nums (default: find the max).
"""
```

在上面的接口描述中，我们定义了命令行程序 `cmd.py` 接受一个或多个数字 `num`，而 `--sum` 选项则是可选，`-h` 或 `--help` 则输出帮助信息。

若提供 `--sum`，则累加给定的数字；反之，取给定多个数字中最大的一个。这个业务逻辑我们将在后文实现。

### 解析命令行

定义好接口描述后，就可以使用 `docopt` 进行解析，写法非常简单：

```python
from docopt import docopt

arguments = docopt(__doc__, options_first=True)
print(arguments)
```

由于我们之前是将接口描述定义在模块的文档字符串中，那么直接使用 `__doc__` 即可获得接口描述。然后使用 `docopt` 函数即可解析命令行为参数字典。为了支持负数，我们将 `options_first` 设置为 `True`。

当我们执行 `python3 cmd.py --sum 1 2 3` 时，将会得到如下内容：

```bash
{'--help': False,
 '--sum': True,
 '<num>': ['1', '2', '3']}
```

可以看到：

- 没有提供 `-h` 或者 `--help`，所以 `arguments` 中 `--help` 为 `False`
- 提供了 `--sum`，所以 `arguments` 中 `--sum` 为 `True`
- 提供了 `<num>...` 为 `1 2 3`，所以 `arguments` 中 `<num>` 为 `['1', '2', '3']`

### 业务逻辑

获得了解析后的命令行参数，我们就可以根据自己的业务需求做进一步处理了。
在本文示例中，我们希望当用户提供 `--sum` 选项时，是对给定的一组数字求和；反之则是取最大值，那么就可以这么写：

```python
nums = (int(num) for num in arguments['<num>'])

if arguments['--sum']:
    result = sum(nums)
else:
    result = max(nums)

print(result) # 基于上文的 python3 cmd.py --sum 1 2 3 参数，其结果为 6
```

### 代码梳理

使用 `docopt` 的方式非常简单，我们将上文的代码汇总下，以有一个更清晰的认识：

```python
# cmd.py
# 1. 定义接口描述
"""Num accumulator.

Usage:
  cmd.py [--sum] <num>...
  cmd.py (-h | --help)

Options:
  -h --help     Show help.
  --sum         Sum the nums (default: find the max).
"""

from docopt import docopt

# 2. 解析命令行
arguments = docopt(__doc__, options_first=True)

# 3. 业务逻辑
nums = (int(num) for num in arguments['<num>'])

if arguments['--sum']:
    result = sum(nums)
else:
    result = max(nums)

print(result)
```

若我们需要对一组数字求和，只需执行：

```bash
$ python3 cmd.py --sum 1 0 -1
0
```

若我们需要对一组数字求最大值，只需执行：

```bash
$ python3 cmd.py 1 0 -1
1
```

我们还可以通过 `-h` 或 `--help` 参数查看使用说明和帮助，也就是我们定义的接口描述。

## 小节

`docopt` 的思路非常简单，就是定义接口描述，然后帮你解析命令行为参数字典，接下来就根据这个字典来编写业务逻辑。

重点就是在于如何定义接口描述，在下一篇文章中，我们来深入了解下如何定义命令、选项、位置参数等接口描述。
