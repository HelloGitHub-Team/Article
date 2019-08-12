# Python 命令行之旅 —— 初探 argparse

## 前言

你是否好奇过在命令行中敲入一段命令后，它是如何被解析执行的？是否考虑过由自己实现一个命令行工具，帮你执行和处理任务？是否了解过陪伴在你身边的 Python 有着丰富的库，来帮你轻松打造命令行工具？

别着急，本文作为 Python 命令行之旅的第一篇将带你逐步揭开命令行解析的面纱，介绍如何使用 Python 内置的 `argparse` 标准库解析命令行，并在后续的系列文章中介绍各具特色的第三方命令行库，讲讲它们的异同，进而全面地体验这次探索的旅程。

```note
本系列文章默认使用 Python 3 作为解释器进行讲解，若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 介绍

`argparse` 作为 Python 内置的标准库，提供了较为简单的方式来编写命令行接口。当你在程序中定义需要哪些参数，`argparse` 便会从 `sys.argv` 中获取命令行输入进行解析，对正确或非法输入做出响应，也可以自动生成帮助信息和使用说明。

## 快速开始

### 设置解析器

第一步要做的就是设置解析器，后续对命令行的解析就依赖于这个解析器，它能够将命令行字符串转换为 Python 对象。
通过实例化 `argparse.ArgumentParser`，给定一些选填参数，我们就可以设置一个解析器：

```python
import argparse
parser = argparse.ArgumentParser(
    description='My Cmd Line Program',
)
```

### 定义参数

通过 `ArgumentParser.add_argument` 方法来为解析器设置参数信息，以告诉解析器命令行字符串中的哪些内容应解析为哪些类型的 Python 对象，如：

```python
# 添加 nums 参数，在使用信息中显示为 num
# 其类型为 int，且支持输入多个，且至少需要提供一个
parser.add_argument('nums',  metavar='num', type=int, nargs='+',
                    help='a num for the accumulator')
# 添加 --sum 参数，该参数被 parser 解析后所对应的属性名为 accumulate
# 若不提供 --sum，默认值为 max 函数，否则为 sum 函数
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the nums (default: find the max)')
```

### 解析命令行

定义好参数后，就可以使用 `ArgumenteParser.parse_args` 方法来解析一组命令行参数字符串了。

默认情况下，参数取自 `sys.argv[1:]`，它就是你在命令行敲入的一段命令（不含文件名）所对应的一个字符串列表。
比如，若你输入 `python3 cmd.py --sum 1 2 3`，那么 `sys.argsv[1:]` 就是 `['--sum', '1', '2', '3']`。

当然，也可以通过 `parse_args` 入参来指定一组命令行参数字符串：

```python
args = parser.parse_args(['--sum', '-1', '0', '1'])
print(args) # 结果：Namespace(accumulate=<built-in function sum>, nums=[-1, 0, 1])
```

### 业务逻辑

解析好命令行后，我们就可以从解析结果中获取每个参数的值，进而根据自己的业务需求做进一步的处理。
比如，对于上文中所定义的 nums 参数，我们可以通过解析后的结果中的 `accumulate` 方法对其进行求最大值或求和（取决于是否提供 `--sum` 参数）。

```python
result = args.accumulate(args.nums)
print(result)  # 基于上文的 ['--sum', '-1', '0', '1'] 参数，accumulate 为 sum 函数，其结果为 0
```

### 代码梳理

通过上文的讲解，完成一个命令行工具的步骤是不是挺简单易懂呢？我们将上文的代码汇总下，以有一个更清晰的认识：

```python
# cmd.py
import argparse

# 1. 设置解析器
parser = argparse.ArgumentParser(
    description='My Cmd Line Program',
)

# 2. 定义参数
parser.add_argument('nums',  metavar='num', type=int, nargs='+',
                    help='a num for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the nums (default: find the max)')

# 3. 解析命令行
args = parser.parse_args()

# 4. 业务逻辑
result = args.accumulate(args.nums)
print(result)
```

若我们需要对一组数字求和，只需执行：

```console
$ python3 cmd.py --sum -1 0 1
0
```

若我们需要对一组数字求最大值，只需执行：

```console
$ python3 cmd.py -1 0 1
1
```

如果给定的参数不是数字，则会报错提示：

```console
$ python3 cmd.py a b c
usage: cmd.py [-h] [--sum] num [num ...]
cmd.py: error: argument num: invalid int value: 'a'
```

我们还可以通过 `-h` 或 `--help` 参数查看其自动生成的使用说明和帮助：

```console
usage: cmd.py [-h] [--sum] num [num ...]

My Cmd Line Program

positional arguments:
  num         a num for the accumulator

optional arguments:
  -h, --help  show this help message and exit
  --sum       sum the nums (default: find the max)
```

## 小结

怎么样？揭开命令行工具的神秘面纱后，是不是发现它并没有想象中的困难？反倒是感受到一种简单而又强大的优雅呢？

不过这还远远不是 `argparse` 的全部面貌。对于一些复杂的情况，比如各种类型参数、参数前缀、参数组、互斥选项、嵌套解析、自定义帮助等等，我们都还没涉及探讨。

在下一篇文章中，让我们来一起深入了解 `argparse`，感受它的魅力吧！
