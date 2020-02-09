# Python 命令行之旅：argparse、docopt、click 和 fire 总结篇

## 一、前言

在近半年的 Python 命令行旅程中，我们依次学习了 `argparse`、`docopt`、`click` 和 `fire` 库的特点和用法，逐步了解到 Python 命令行库的设计哲学与演变。
本文作为本次旅程的终点，希望从一个更高的视角对这些库进行横向对比，总结它们的异同点和使用场景，以期在应对不同场景时能够分析利弊，选择合适的库为己所用。

```plain
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、设计理念

在讨论各个库的设计理念之前，我们先设计一个`计算器程序`，其实这个例子在 `argparse` 库的第一篇讲解中出现过，也就是：

- 命令行程序接受一个位置参数，它能出现多次，且是数字
- 默认情况下，命令行程序会求出给定的一串数字的最大值
- 如果指定了选项参数 `--sum`，那么就会将求出给定的一串数字的和

希望从各个库实现该例子的代码中能进一步体会它们的设计理念。

### 2.1、argparse

`argparse` 的设计理念就是提供给你最细粒度的控制，你需要详细地告诉它参数是选项参数还是位置参数、参数值的类型是什么、该参数的处理动作是怎样的。
总之，它就像是一个没有智能分析能力的初代机器人，你需要告诉它明确的信息，它才会根据给定的信息去帮助你做事情。

以下示例为 `argparse` 实现的 `计算器程序`：

```python
import argparse

# 1. 设置解析器
parser = argparse.ArgumentParser(description='Calculator Program.')

# 2. 定义参数
# 添加位置参数 nums，在帮助信息中显示为 num
# 其类型为 int，且支持输入多个，且至少需要提供一个
parser.add_argument('nums',  metavar='num', type=int, nargs='+',
                    help='a num for the accumulator')
# 添加选项参数 --sum，该参数被 parser 解析后所对应的属性名为 accumulate
# 若不提供 --sum，默认值为 max 函数，否则为 sum 函数
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the nums (default: find the max)')


# 3. 解析参数
args = parser.parse_args(['--sum', '1', '2', '3'])
print(args) # 结果：Namespace(accumulate=<built-in function sum>, nums=[1, 2, 3])

# 4. 业务逻辑
result = args.accumulate(args.nums)
print(result)  # 基于上文的 ['--sum', '1', '2', '3'] 参数，accumulate 为 sum 函数，其结果为 6
```

从上述示例可以看到，我们需要通过 `add_argument` 很明确地告诉 `argparse` 参数长什么样：

- 它是位置参数 `nums`，还是选项参数 `--sum`
- 它的类型是什么，比如 `type=int` 表示类型是 int
- 这个参数能重复出现几次，比如 `nargs='+'` 表示至少提供 1 个
- 参数的是存什么的，比如 `action='store_const'` 表示存常量

然后它才根据给定的这些元信息来解析命令行参数（也就是示例中的 `['--sum', '1', '2', '3']`）。

这是很计算机的思维，虽然冗长，但也带来了灵活性。

### 2.2、docopt

从 `argparse` 的理念可以看出，它是命令式的。这时候 `docopt` 另辟蹊径，声明式是不是也可以？一个命令行程序的帮助信息其实已然包含了这个命令行的完整元信息，那不就可以通过定义帮助信息来定义命令行？`docopt` 就是基于这样的想法去设计的。

声明式的好处在于只要你掌握了声明式的语法，那么定义命令行的元信息就会很简单。

以下示例为 `docopt` 实现的 `计算器程序`：

```python
# 1. 定义接口描述/帮助信息
"""Calculator Program.

Usage:
  calculator.py [--sum] <num>...
  calculator.py (-h | --help)

Options:
  -h --help     Show help.
  --sum         Sum the nums (default: find the max).
"""

from docopt import docopt

# 2. 解析命令行
arguments = docopt(__doc__, options_first=True, argv=['--sum', '1', '2', '3'])
print(arguments) # 结果：{'--help': False, '--sum': True, '<num>': ['1', '2', '3']}

# 3. 业务逻辑
nums = (int(num) for num in arguments['<num>'])

if arguments['--sum']:
    result = sum(nums)
else:
    result = max(nums)

print(result) # 基于上文的 ['--sum', '1', '2', '3'] 参数，处理函数为 sum 函数，其结果为 6
```

从上述示例可以看到，我们通过 `__doc__` 定义了接口描述，这和 `argparse` 中 `add_argument` 是等价的，然后 `docopt` 便会根据这个元信息把命令行参数转换为一个字典。业务逻辑中就需要对这个字典进行处理。

对比与 `argparse`：

- 对于更为复杂的命令程序，元信息的定义上 `docopt` 会更加简单
- 然而在业务逻辑的处理上，由于 `argparse` 在一些简单参数的处理上会更加便捷（比如示例中的情形），相对来说 `docopt` 转换为字典后就把所有处理交给业务逻辑的方式会更加复杂

### 2.3、click

命令行程序本质上是定义参数和处理参数，而处理参数的逻辑一定是与所定义的参数有关联的。那可不可以用函数和装饰器来实现处理参数逻辑与定义参数的关联呢？而 `click` 正好就是以这种使用方式来设计的。

`click` 使用装饰器的好处就在于用装饰器优雅的语法将参数定义和处理逻辑整合在一起，从而暗示了路由关系。相比于 `argparse` 和 `docopt` 需要自行对解析后的参数来做路由关系，简单了不少。

以下示例为 `click` 实现的 `计算器程序`：

```python
import sys
import click

sys.argv = ['calculator.py', '--sum', '1', '2', '3']

# 2. 定义参数
@click.command()
@click.argument('nums', nargs=-1, type=int)
@click.option('--sum', 'use_sum', is_flag=True, help='sum the nums (default: find the max)')
# 1. 业务逻辑
def calculator(nums, use_sum):
    """Calculator Program."""
    print(nums, use_sum) # 输出：(1, 2, 3) True
    if use_sum:
        result = sum(nums)
    else:
        result = max(nums)

    print(result) # 基于上文的 ['--sum', '1', '2', '3'] 参数，处理函数为 sum 函数，其结果为 6

calculator()
```

从上述示例可以看出，参数和对应的处理逻辑非常好地绑定在了一起，看上去就很直观，使得我们可以明确了解参数会怎么处理，这在有大量参数时显得尤为重要，这边是 `click` 相比于 `argparse` 和 `docopt` 最明显的优势。

此外，`click` 还内置了很多实用工具和额外能力，比如说 Bash 补全、颜色、分页支持、进度条等诸多实用功能，可谓是如虎添翼。

### 2.4、fire

`fire` 则是用一种面向广义对象的方式来玩转命令行，这种对象可以是类、函数、字典、列表等，它更加灵活，也更加简单。你都不需要定义参数类型，`fire` 会根据输入和参数默认值来自动判断，这无疑进一步简化了实现过程。

以下示例为 `click` 实现的 `计算器程序`：

```python
import sys
import fire

sys.argv = ['calculator.py', '1', '2', '3', '--sum']

builtin_sum = sum

# 1. 业务逻辑
# sum=False，暗示它是一个选项参数 --sum，不提供的时候为 False
# *nums 暗示它是一个能提供任意数量的位置参数
def calculator(sum=False, *nums):
    """Calculator Program."""
    print(sum, nums) # 输出：True (1, 2, 3)
    if sum:
        result = builtin_sum(nums)
    else:
        result = max(nums)

    print(result) # 基于上文的 ['1', '2', '3', '--sum'] 参数，处理函数为 sum 函数，其结果为 6


fire.Fire(calculator)
```

从上述示例可以看出，`fire` 提供的方式无疑是最简单、并且最 Pythonic 的了。我们只需关注业务逻辑，而命令行参数的定义则和函数参数的定义融为了一体。

不过，有利自然也有弊，比如 `nums` 并没有说是什么类型，也就意味着输入字符串'abc'也是合法的，这就意味着一个严格的命令行程序必须在自己的业务逻辑中来对期望的类型进行约束。

## 三、横向对比

最后，我们横向对比下`argparse`、`docopt`、`click` 和 `fire` 库的各项功能和特点：

|                                                  | argpase                                                      | docopt                                          | click                                             | fire                       |
| ------------------------------------------------ | :----------------------------------------------------------- | :---------------------------------------------- | :------------------------------------------------ | :------------------------- |
| 使用步骤数                                       | 4 步                                                         | 3 步                                            | 2 步                                              | 1 步                       |
| 使用步骤数                                       | 1. 设置解析器<br>2. 定义参数<br>3. 解析命令行<br>4. 业务逻辑 | 1. 定义接口描述<br>2. 解析命令行<br>3. 业务逻辑 | 1. 业务逻辑<br>2. 定义参数                        | 1. 业务逻辑                |
| 选项参数<br>（如 `--sum`）                       | <font color=green>✔</font>                                   | <font color=green>✔</font>                      | <font color=green>✔</font>                        | <font color=green>✔</font> |
| 位置参数<br>（如 `X Y`）                         | <font color=green>✔</font>                                   | <font color=green>✔</font>                      | <font color=green>✔</font>                        | <font color=green>✔</font> |
| 参数默认值<br>                                   | <font color=green>✔</font>                                   | <font color=red>✘</font>                        | <font color=green>✔</font>                        | <font color=green>✔</font> |
| 互斥选项<br>（如 `--car` 和 `--bus` 只能二选一） | <font color=green>✔</font>                                   | <font color=green>✔</font>                      | <font color=yellow>✔</font><br>可通过第三方库支持 | <font color=red>✘</font>   |
| 可变参数<br>（如指定多个 `--file`）              | <font color=green>✔</font>                                   | <font color=green>✔</font>                      | <font color=green>✔</font>                        | <font color=green>✔</font> |
| 嵌套/父子命令<br>                                | <font color=green>✔</font>                                   | <font color=green>✔</font>                      | <font color=green>✔</font>                        | <font color=green>✔</font> |
| 工具箱<br>                                       | <font color=red>✘</font>                                     | <font color=red>✘</font>                        | <font color=green>✔</font>                        | <font color=green>✔</font> |
| 链式命令调用<br>                                 | <font color=red>✘</font>                                     | <font color=red>✘</font>                        | <font color=red>✘</font>                          | <font color=green>✔</font> |
| 类型约束                                         | <font color=green>✔</font>                                   | <font color=red>✘</font>                        | <font color=green>✔</font>                        | <font color=red>✘</font>   |

Python 的命令行库种类繁多、各具特色。结合上面的总结，可以选择出符合使用场景的库，如果几个库都符合，那么就根据你更偏爱的风格来选择。这些库都很优秀，其背后的思想很是值得我们学习和扩展。
