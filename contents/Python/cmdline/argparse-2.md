# Python 命令行之旅：深入 argparse （一）

## 前言

在第一篇“初探 argparse”的文章中，我们初步掌握了使用 `argparse` 的四部曲，对它有了一个基本的体感。
但是它具体支持哪些类型的参数？这些参数该如何配置？本文将带你深入了解 `argparse` 的参数们。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 参数动作

你是否还记得？在上一篇四部曲中的第二步是定义参数，在这个步骤中，我们指定了 `action` 入参：

```python
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the nums (default: find the max)')
```

那么这里面的 `action`，也就是 `参数动作`，究竟是用来做什么的呢？

想象一下，当我们在命令行输入一串参数后，对于不同类型的参数是希望做不同的处理的。
那么 `参数动作` 其实就是告诉解析器，我们希望对应的参数该被如何处理。比如，参数值是该被存成一个值呢，还是追加到一个列表中？是当成布尔的 True 呢，还是 False？

`参数动作` 被分成了如下 8 个类别：

- `store` —— 保存参数的值，这是默认的参数动作。它通常用于给一个参数指定值，如指定名字：

```bash
>>> parser.add_argument('--name')
>>> parser.parse_args(['--name', 'Eric'])
Namespace(name='Eric')
```

- `store_const` —— 保存被 `const` 命名的固定值。当我们想通过是否给定参数来起到标志的作用，给定就取某个值，就可以使用该参数动作，如：

```bash
>>> parser.add_argument('--sum', action='store_const', const=sum)
>>> parser.parse_args(['--sum'])
Namespace(sum=<built-in function sum>)
>>> parser.parse_args([])
Namespace(sum=None)
```

- `store_true` 和 `store_false` —— 是 `store_const` 的特殊情况，用来分别保存 True 和 False。如果为指定参数，则其默认值分别为 False 和 True，如：

```bash
>>> parser.add_argument('--use', action='store_true')
>>> parser.add_argument('--nouse', action='store_false')
>>> parser.parse_args(['--use', '--nouse'])
Namespace(nouse=False, use=True)
>>> parser.parse_args([])
Namespace(nouse=True, use=False)
```

- `append` —— 将参数值追加保存到一个列表中。它常常用于命令行中允许多个相同选项，如：

```bash
>>> parser.add_argument('--file', action='append')
>>> parser.parse_args(['--file', 'f1', '--file', 'f2'])
Namespace(file=['f1', 'f2'])
```

- `append_const` —— 将 `const` 命名的固定值追加保存到一个列表中（`const` 的默认值为 `None`）。它常常用于将多个参数所对应的固定值都保存在同一个列表中，相应的需要 `dest` 入参来配合，以放在同一个列表中，如：

不指定 `dest` 入参，则固定值保存在以参数名命名的变量中

```bash
>>> parser.add_argument('--int', action='append_const', const=int)
>>> parser.add_argument('--str', action='append_const', const=str)
>>> parser.parse_args(['--int', '--str'])
Namespace(int=[<class 'int'>], str=[<class 'str'>])
```

指定 `dest` 入参，则固定值保存在 `dest` 命名的变量中

```bash
>>> parser.add_argument('--int', dest='types', action='append_const', const=int)
>>> parser.add_argument('--str', dest='types', action='append_const', const=str)
>>> parser.parse_args(['--int', '--str'])
Namespace(types=[<class 'int'>, <class 'str'>])
```

- `count` —— 计算参数出现次数，如：

```bash
>>> parser.add_argument('--increase', '-i', action='count')
>>> parser.parse_args(['--increas', '--increase'])
Namespace(increase=2)
>>>parser.parse_args(['-iii'])
Namespace(increase=3)
```

- `help` —— 打印解析器中所有选项和参数的完整帮助信息，然后退出。

- `version` —— 打印命令行版本，通过指定 `version` 入参来指定版本，调用后退出。如：

```bash
>>> parser = argparse.ArgumentParser(prog='CMD')
>>> parser.add_argument('--version', action='version', version='%(prog)s 1.0')
>>> parser.parse_args(['--version'])
CMD 1.0
```

## 参数类别

如果说 `参数动作` 定义了解析器在接收到参数后该如何处理参数，那么 `参数类别` 就是告诉解析器这个参数的元信息，也就是参数是什么样的。比如，参数是字符串呢？还是布尔类型呢？参数是在几个值中可选的呢？还是可以给定值，等等。

下面，我们将逐一介绍不同类型的参数。

### 可选参数

`可选参数` 顾名思义就是参数是可以加上，或不加上。默认情况下，通过 `ArgumentParser.add_argument` 添加的参数就是可选参数。

我们可以通过 `-` 来指定短参数，也就是名称短的参数；也可以通过 `--` 来指定长参数，也就是名称长的参数。当然也可以两个都指定。

可选参数通常用于：用户提供一个参数以及对应值，则使用该值；若不提供，则使用默认值。如：

```bash
>>> parser.add_argument('--name', '-n')
>>> parser.parse_args(['--name', 'Eric'])  # 通过长参数指定名称
Namespace(name='Eric')
>>> parser.parse_args(['-n', 'Eric']) # 通过短参数指定名称
Namespace(name='Eric')
>>> parser.parse_args([]) # 不指定则默认为 None
Namespace(name=None)
```

### 参数类型

`参数类型` 就是解析器参数值是要作为什么类型去解析，默认情况下是 `str` 类型。我们可以通过 `type` 入参来指定参数类型。

`argparse` 所支持的参数类型多种多样，可以是 `int`、`float`、`bool`等，比如：

```bash
>>> parser.add_argument('-i', type=int)
>>> parser.add_argument('-f', type=float)
>>> parser.add_argument('-b', type=bool)
>>> parser.parse_args(['-i', '1', '-f', '2.1', '-b', '0'])
Namespace(b=False, f=2.1, i=1)
```

更厉害的是，`type` 入参还可以是可调用(`callable`)对象。这就给了我们很大的想象空间，可以指定 `type=open` 来把参数值作为文件进行处理，也可以指定自定义函数来进行类型检查和类型转换。

作为文件进行处理：

```bash
>>> parser.add_argument('--file', type=open)
>>> parser.parse_args(['--file', 'README.md'])
Namespace(b=None, f=None, file=<_io.TextIOWrapper name='README.md' mode='r' encoding='cp936'>, i=None)
```

使用自定义函数进行处理，入参为参数值，需返回转换后的结果。
比如，对于参数 `--num`，我们希望当其值小于 1 时则返回 1，大于 10 时则返回 10：

```bash
>>> def limit(string):
...   num = int(string)
...   if num < 1:
...     return 1
...   if num > 10:
...     return 10
...   return num
...
>>> parser.add_argument('--num', type=limit)
>>> parser.parse_args(['--num', '-1'])  # num 小于1，则取1
Namespace(num=1)
>>> parser.parse_args(['--num', '15'])  # num 大于10，则取10
Namespace(num=10)
>>> parser.parse_args(['--num', '5'])  # num 在1和10之间，则取原来的值
Namespace(num=5)
```

### 参数默认值

`参数默认值` 用于在命令行中不传参数值的情况下的默认取值，可通过 `default` 来指定。如果不指定该值，则参数默认值为 `None`。

比如：

```bash
>>> parser.add_argument('-i', default=0, type=int)
>>> parser.add_argument('-f', default=3.14, type=float)
>>> parser.add_argument('-b', default=True, type=bool)
>>> parser.parse_args([])
Namespace(b=True, f=3.14, i=0)
```

### 位置参数

`位置参数` 就是通过位置而非是 `-` 或 `--` 开头的参数来指定参数值。

比如，我们可以指定两个位置参数 `x` 和 `y` ，先添加的 `x` 位于第一个位置，后加入的 `y` 位于第二个位置。那么在命令行中输入 `1 2`的时候，分别对应到的就是 `x` 和 `y`：

```bash
>>> parser.add_argument('x')
>>> parser.add_argument('y')
>>> parser.parse_args(['1', '2'])
Namespace(x='1', y='2')
```

### 可选值

`可选值` 就是限定参数值的内容，通过 `choices` 入参指定。

有些情况下，我们可能需要限制用户输入参数的内容，只能在预设的几个值中选一个，那么 `可选值` 就派上了用场。

比如，指定文件读取方式限制为 `read-only` 和 `read-write`：

```bash
>>> parser.add_argument('--mode', choices=('read-only', 'read-write'))
>>> parser.parse_args(['--mode', 'read-only'])
Namespace(mode='read-only')
>>> parser.parse_args(['--mode', 'read'])
usage: [-h] [--mode {read-only,read-write}]
: error: argument --mode: invalid choice: 'read' (choose from 'read-only', 'read-write')
```

### 互斥参数

`互斥参数` 就是多个参数之间彼此互斥，不能同时出现。使用互斥参数首先通过 `ArgumentParser.add_mutually_exclusive_group` 在解析器中添加一个互斥组，然后在这个组里添加参数，那么组内的所有参数都是互斥的。

比如，我们希望通过命令行来告知乘坐的交通工具，要么是汽车，要么是公交，要么是自行车，那么就可以这么写：

```bash
>>> group = parser.add_mutually_exclusive_group()
>>> group.add_argument('--car', action='store_true')
>>> group.add_argument('--bus', action='store_true')
>>> group.add_argument('--bike', action='store_true')
>>> parser.parse_args([])  # 什么都不乘坐
Namespace(bike=False, bus=False, car=False)
>>> parser.parse_args(['--bus'])  # 乘坐公交
Namespace(bike=False, bus=True, car=False)
>>> parser.parse_args(['--bike'])  # 骑自行车
Namespace(bike=True, bus=False, car=False)
>>> parser.parse_args(['--bike', '--car'])  # 又想骑车，又想坐车，那是不行的
usage: [-h] [--car | --bus | --bike]
: error: argument --car: not allowed with argument --bike
```

### 可变参数列表

`可变参数列表` 用来定义一个参数可以有多个值，且能通过 `nargs` 来定义值的个数。

若 `nargs=N`，`N`为一个数字，则要求该参数提供 N 个值，如：

```bash
>>> parser.add_argument('--foo', nargs=2)
>>> print(parser.parse_args(['--foo', 'a', 'b']))
Namespace(foo=['a', 'b'])
>>> print(parser.parse_args(['--foo', 'a', 'b', 'c']))
usage: [-h] [--foo FOO FOO]
: error: unrecognized arguments: c
```

若 `nargs=?`，则要求改参数提供 0 或 1 个值，如：

```bash
>>> parser.add_argument('--foo', nargs='?')
>>> parser.parse_args(['--foo'])
Namespace(foo=None)
>>> parser.parse_args(['--foo', 'a'])
Namespace(foo='a')
>>> parser.parse_args(['--foo', 'a', 'b'])
usage: [-h] [--foo [FOO]]
: error: unrecognized arguments: b
```

若 `nargs=*`，则要求改参数提供 0 或多个值，如：

```bash
>>> parser.add_argument('--foo', nargs='*')
>>> parser.parse_args(['--foo'])
Namespace(foo=[])
>>> parser.parse_args(['--foo', 'a'])
Namespace(foo=['a'])
>>> parser.parse_args(['--foo', 'a', 'b', 'c', 'd', 'e'])
Namespace(foo=['a', 'b', 'c', 'd', 'e'])
```

若 `nargs=?`，则要求改参数至少提供 1 个值，如：

```bash
>>> parser.add_argument('--foo', nargs='+')
>>> parser.parse_args(['--foo', 'a'])
Namespace(foo=['a'])
>>> parser.parse_args(['--foo'])
usage: [-h] [--foo FOO [FOO ...]]
: error: argument --foo: expected at least one argument
```

## 小节

在了解了参数动作和参数类别后，是不是渐渐开始对使用 `argparse` 胸有成竹了呢？至少，用现在学到的知识来完成简单的命令行工具已经不再话下了。

在下一篇文章中，我们来继续深入了解 `argparse` 的功能，如何修改参数前缀，如何定义参数组，如何定义嵌套的解析器，如何编写自定义动作等，让我们拭目以待吧~
