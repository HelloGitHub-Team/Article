# Python 命令行之旅：初探 fire

## 一、前言

在本系列前面所有文章中，我们分别介绍了 `argparse`、`docopt` 和 `click` 的主要功能和用法。它们各具特色，都能出色地完成命令行任务。`argparse` 是面向过程的，需要先设置解析器，再定义参数，再解析命令行，最后实现业务逻辑。`docopt` 先用声明式的语法定义出参数，再过程式地解析命令行和实现业务逻辑。`click` 则是用装饰器的方式进一步简化显式的命令调用逻辑，但仍然不够面向对象。

而今天要介绍的 [fire](https://github.com/google/python-fire) 则是用一种面向广义对象的方式来玩转命令行，这种对象可以是类、函数、字典、列表等，它更加灵活，也更加简单。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、介绍

[fire](https://github.com/google/python-fire) 可以根据任何 Python 对象自动生成命令行接口。它有如下特性：

- 能以简单的方式生成 CLI
- 是一个开发和调试 Python 代码的实用工具
- 能将现存代码或别人的代码转换为 CLI
- 使得在 Bash 和 Python 间的转换变得更容易
- 通过预先为 REPL 设置所需的模块和变量，使得实用 REPL 更加容易

通过如下命令可快速安装 `fire` 库：

```bash
pip install fire
```

## 三、快速开始

回忆下使用 `argparse`、`docopt` 和 `click` 实现命令行程序的步骤：

- 对于 `argparse` 来说，要先设置解析器，再定义参数，再解析命令行，最后实现业务逻辑（四步）
- 对于 `docopt` 来说，要先定义定义接口描述，再解析命令行，最后实现业务逻辑（三步）
- 对于 `click` 来说，就是实现业务逻辑和通过装饰器的方式定义参数（两步）

它们的实现步骤越来越简单，从四步简化到了两步。而今天的主角 `fire` **只需一步，写业务逻辑就够了。**

这简直简单的不可思议，为什么这样做就够了？我们不妨考虑下 Python 中的函数，函数是不是可以对应一个命令行程序，而函数的参数可以对应命令行程序的参数和选项呢？再看看 Python 中的类，一个类是不是可以对应一个命令行程序，而类中的每个实例方法就可以对应子命令，实例方法中的参数就是对应子命令的参数和选项。

这么一想，理论上确实是可以实现的，我们不妨通过下面的示例来看看 `fire` 是如何让我们通过简单的方式实现命令行程序。

### 3.1 使用函数

来看这么一个例子：

```python
import fire

def hello(name="World"):
  return 'Hello {name}!'.format(name=name)

if __name__ == '__main__':
  fire.Fire(hello)
```

在上述例子中定义一个 `hello` 函数，它接受 `name` 参数，并且有默认值 "World"。使用 `fire.Fire(hello)` 即可非常简单快速地实现命令功能，这个命令行就接受 `--name` 选项，不提供时使用默认值 "World"，提供时就按提供的值来。

可在命令行中执行下列命令：

```bash
$ python hello.py
Hello World!
$ python hello.py --name=Prodesire
Hello Prodesire!
$ python hello.py --help
INFO: Showing help with the command 'hello.py -- --help'.

NAME
    hello.py

SYNOPSIS
    hello.py <flags>

FLAGS
    --name=NAME
```

### 3.2 使用类

使用函数是最简单的方式，如果我们想以更有组织的方式来实现，比如使用类，`fire` 也是支持的。

```python
import fire

class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

  def triple(self, number):
    return 3 * number

if __name__ == '__main__':
  fire.Fire(Calculator)
```

在上述例子中定义一个 `Calculator` 类，它有两个实例方法 `double` 和 `triple`，并且都接受 `number` 参数，没有默认值。使用 `fire.Fire(Calculator)` 即可非常简单快速地实现命令功能，这个命令行支持两个子命令 `double` 和 `triple`，位置参数 `NUMBER` 或选项参数 `--number`

可在命令行中执行下列命令：

```bash
$ python calculator.py double 10
20
$ python calculator.py triple --number=15
45
$ python calculator.py double --help
INFO: Showing help with the command 'calculator.py double -- --help'.

NAME
    calculator.py double

SYNOPSIS
    calculator.py double NUMBER

POSITIONAL ARGUMENTS
    NUMBER

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

## 四、小结

`fire` 的使用方式非常简单，定一个 Python 对象，剩下的就交给 `fire` 来处理，可谓是非常的 Pythonic，这也是它会如此受欢迎的原因。

除了上面展示的内容，`fire` 还支持更多种类的 Python 对象，也拥有很多强大的功能，我们将在接下来几节中逐步走近它。
