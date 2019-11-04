# Python 命令行之旅：初探 click

## 一、前言

在本系列前面几篇文章中，我们分别介绍了 `argparse` 和 `docopt` 的主要功能和用法。它们各具特色，都能出色地完成命令行任务。`argparse` 是面向过程的，需要先设置解析器，再定义参数，再解析命令行，最后实现业务逻辑。而 `docopt` 先用声明式的语法定义出参数，再过程式地解析命令行和实现业务逻辑。在一些人看来，这些方式都不够优雅。

而今天要介绍的 [click](https://click.palletsprojects.com/) 则是用一种你很熟知的方式来玩转命令行。命令行程序本质上是定义参数和处理参数，而处理参数的逻辑一定是与所定义的参数有关联的。那可不可以用函数和装饰器来实现处理参数逻辑与定义参数的关联呢？而 `click` 正好就是以这种方式来使用的。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、介绍

[click](https://click.palletsprojects.com/) 是一个以尽可能少的代码、以组合的方式创建优美的命令行程序的 Python 包。它有很高的可配置性，同时也能开箱即用。

它旨在让编写命令行工具的过程既快速又有趣，还能防止由于无法实现预期的 CLI API 所产生挫败感。它有如下三个特点：

- 任意嵌套命令
- 自动生成帮助
- 支持运行时延迟加载子命令

## 三、快速开始

### 3.1 业务逻辑

首先定义业务逻辑，是不是感觉到有些难以置信呢？

不论是 `argparse` 还是 `docopt`，业务逻辑都是被放在最后一步，但 `click` 却是放在第一步。细想想 `click` 的这种方式才更符合人的思维吧？不论用什么命令行框架，我们最终关心的就是实现业务逻辑，其他的能省则省。

我们以官方示例为例，来介绍 `click` 的用法和哲学。假设命令行程序的输入是 `name` 和 `count`，功能是打印指定次数的名字。

那么在 `hello.py` 中，很容易写出如下代码：

```python
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)
```

这段代码的逻辑很简单，就是循环 `count` 次，使用 `click.echo` 打印 `name`。其中，`click.echo` 和 `print` 的作用相似，但功能更加强大，能处理好 Unicode 和 二进制数据的情况。

### 3.2 定义参数

很显然，我们需要针对 `count` 和 `name` 来定义它们所对应的参数信息。

- `count` 对应为命令行选项 `--count`，类型为数字，我们希望在不提供参数时，其默认值是 1
- `name` 对应为命令行选项 `--name`，类型为字符串，我们希望在不提供参数时，能给人提示

使用 `click`，就可以写成下面这样：

```python
from click import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    ...
```

在上面的示例中：

- 使用装饰器的方式，即定义了参数，又将之与处理逻辑绑定，这真是优雅。和 `argparse`、`docopt` 比起来，就少了一步绑定过程
- 使用 `click.command` 表示 `hello` 是对命令的处理
- 使用 `click.option` 来定义参数选项
  - 对于 `--count` 来说，使用 `default` 来指定默认值。而由于默认值是数字，进而暗示 `--count` 选项的类型为数字
  - 对于 `--name` 来说，使用 `prompt` 来指定未输入该选项时的提示语
  - 使用 `help` 来指定帮助信息

不论是装饰器的方式、还是各种默认行为，`click` 都是像它的介绍所说的那样，让人尽可能少地编写代码，让整个过程变得快速而有趣。

### 3.3 代码梳理

使用 `click` 的方式非常简单，我们将上文的代码汇总下，以有一个更清晰的认识：

```python
# hello.py
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
    hello()
```

若我们指定次数和名字：

```bash
$ python3 hello.py --count 2 --name Eric
Hello Eric!
Hello Eric!
```

若我们什么都不指定，则会提示输入名字，并默认输出一次：

```bash
$ python3 hello.py
Your name: Eric
Hello Eric!
```

我们还可以通过 `--help` 参数查看自动生成的帮助信息：

```bash
Usage: hello.py [OPTIONS]

  Simple program that greets NAME for a total of COUNT times.

Options:
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
```

## 四、小结

`click` 的思路非常简单，定义处理函数，通过它的装饰器来定义参数。使用装饰器的绝妙之处就在于把定义和绑定这两个步骤合为一个步骤，使得整个过程变得如丝般顺滑。

`click` 除了以 `Pythonic` 的方式让命令行程序的实现变得更加优雅和好用外，还提供了比 `argparse` 和 `docopt` 都要强大的功能。在接下来几节中，我们将会逐步揭开它的面纱。
