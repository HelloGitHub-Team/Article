# Python 命令行之旅：深入 click（一）

## 一、前言

在上一篇文章中，我们初步掌握了 `click` 的简单用法，并了解到它与 `argparse` 和 `docopt` 的不同。接下来，将深入介绍 `click` 的各类用法，以让你能轻松打造复杂的命令行程序。

在概念上， `click` 把命令行分为 3 个组成：参数、选项和命令。

- `参数` 就是跟在命令后的除选项外的内容，比如 `git add a.txt` 中的 `a.txt` 就是表示文件路径的参数
- `选项` 就是以 `-` 或 `--` 开头的参数，比如 `-f`、`--file`
- `命令` 就是命令行的初衷了，比如 `git` 就是命令，而 `git add` 中的 `add` 则是 `git` 的子命令

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、参数

### 2.1 基本参数

`基本参数` 就是通过位置里指定参数值。

比如，我们可以指定两个位置参数 `x` 和 `y` ，先添加的 `x` 位于第一个位置，后加入的 `y` 位于第二个位置。那么在命令行中输入 `1 2`的时候，分别对应到的就是 `x` 和 `y`：

```python
@click.command()
@click.argument('x')
@click.argument('y')
def hello(x, y):
    print(x, y)
```

### 2.2 参数类型

`参数类型` 就是将参数值作为什么类型去解析，默认情况下是字符串类型。我们可以通过 `type` 入参来指定参数类型。

`click` 支持的参数类型多种多样：

- `str` / `click.STRING` 表示字符串类型，这也是默认类型
- `int` / `click.INT` 表示整型
- `float` / `click.FLOAT` 表示浮点型
- `bool` / `click.BOOL` 表示布尔型。很棒之处在于，它会识别表示真/假的字符。对于 `1`、`yes`、`y` 和 `true` 会转化为 `True`；`0`、`no`、`n` 和 `false` 会转化为 `False`
- `click.UUID` 表示 UUID，会自动将参数转换为 `uuid.UUID` 对象
- `click.FILE` 表示文件，会自动将参数转换为文件对象，并在命令行结束时自动关闭文件
- `click.PATH` 表示路径
- `click.Choice` 表示选择选项
- `click.IntRange` 表示范围选项

同 `argparse` 一样，`click` 也支持自定义类型，需要编写 `click.ParamType` 的子类，并重载 `convert` 方法。

官网提供了一个例子，实现了一个整数类型，除了普通整数之外，还接受十六进制和八进制数字， 并将它们转换为常规整数：

```python
class BasedIntParamType(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except TypeError:
            self.fail(
                "expected string for int() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)

BASED_INT = BasedIntParamType()
```

### 2.3 文件参数

在基本参数的基础上，通过指定参数类型，我们就能构建出各类参数。

`文件参数` 是非常常用的一类参数，通过 `type=click.File` 指定，它能正确处理所有 Python 版本的 unicode 和 字节，使得处理文件十分方便。

```python
@click.command()
@click.argument('input', type=click.File('rb'))  # 指定文件为二进制读
@click.argument('output', type=click.File('wb'))  # 指定文件为二进制写
def inout(input, output):
    while True:
        chunk = input.read(1024)  # 此时 input 为文件对象，每次读入 1024 字节
        if not chunk:
            break
        output.write(chunk)  # 此时 output 为文件对象，写入上步读入的内容
```

### 2.4 文件路径参数

`文件路径参数` 用来处理文件路径，可以对路径做是否存在等检查，通过 `type=click.Path` 指定。不论文件名是 unicode 还是字节类型，获取到的参数类型都是 unicode 类型。

```python
@click.command()
@click.argument('filename', type=click.Path(exists=True))  # 要求给定路径存在，否则报错
def hello(filename):
    click.echo(click.format_filename(filename))
```

如果文件名是以 `-` 开头，会被误认为是命令行选项，这个时候需要在参数前加上 `--` 和空格，比如

```bash
$ python hello.py -- -foo.txt
-foo.txt
```

### 2.5 选择项参数

`选择项参数` 用来限定参数内容，通过 `type=click.Choice` 指定。

比如，指定文件读取方式限制为 `read-only` 和 `read-write`：

```python
@click.command()
@click.argument('mode', type=click.Choice(['read-only', 'read-write']))
def hello(mode):
    click.echo(mode)
```

### 2.6 可变参数

`可变参数` 用来定义一个参数可以有多个值，且能通过 `nargs` 来定义值的个数，取得的参数的变量类型为元组。

若 `nargs=N`，`N`为一个数字，则要求该参数提供 N 个值。若 `N` 为 `-1` 则接受提供无数量限制的参数，如:

```python
@click.command()
@click.argument('foo', nargs=-1)
@click.argument('bar', nargs=1)
def hello(foo, bar):
    pass
```

如果要实现 `argparse` 中要求参数数量为 1 个或多个的功能，则指定 `nargs=-1` 且 `required=True` 即可：

```python
@click.command()
@click.argument('foo', nargs=-1, required=True)
def hello(foo, bar):
    pass
```

### 2.7 从环境变量读取参数

通过在 `click.argument` 中指定 `envvar`，则可读取指定名称的环境变量作为参数值，比如：

```python
@click.command()
@click.argument('filename', envvar='FILENAME')
def hello(filename):
    print(filename)
```

执行如下命令查看效果：

```bash
$ FILENAME=hello.txt python3 hello.py
hello.txt
```

而在 `argparse` 中，则需要自己从环境变量中读取。

## 小节

本文讲解了 `click` 中基本参数的用法，在此基础上介绍了各种类型的参数，最后说明了从环境变量中获取参数值的写法。

在下一篇文章中，我们来继续深入了解 `click` 的功能，看看它都支持什么样的“选项”。
